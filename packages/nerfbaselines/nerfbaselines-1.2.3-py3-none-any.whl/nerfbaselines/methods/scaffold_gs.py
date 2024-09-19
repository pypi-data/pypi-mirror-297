#
# Copyright (C) 2023, Inria
# GRAPHDECO research group, https://team.inria.fr/graphdeco
# All rights reserved.
#
# This software is free for non-commercial, research and evaluation use
# under the terms of the LICENSE.md file.
#
# For inquiries contact  george.drettakis@inria.fr
#

# NOTE: This code modifies ScaffoldGS in several ways:
# - It adds support for cx, cy not in the center of the image
# - It also adds support for sampling masks
# - It fixes bugs with ScaffoldGS saving and restoring
# - It implements functionality to obtain appearance embeddings and render with specifif
#  embeddings
# - Implements functionality to optimize embeddings for a dataset
import math
import dataclasses
import warnings
import hashlib
import itertools
from collections import namedtuple
from argparse import ArgumentParser
import shlex
import logging
import copy
from typing import Optional
import os
import tempfile
import numpy as np
from PIL import Image
from nerfbaselines import (
    Method, MethodInfo, ModelInfo, OptimizeEmbeddingOutput, 
    RenderOutput, Cameras, camera_model_to_int, Dataset
)
from nerfbaselines.utils import convert_image_dtype
import shlex


import torch  # type: ignore
from PIL import Image  # type: ignore
from utils.general_utils import safe_state  # type: ignore
from random import randint  # type: ignore
from utils.loss_utils import l1_loss, ssim  # type: ignore
from gaussian_renderer import prefilter_voxel, render, generate_neural_gaussians  # type: ignore
from scene import Scene, sceneLoadTypeCallbacks, GaussianModel as _old_GaussianModel  # type: ignore
from arguments import ModelParams, PipelineParams, OptimizationParams  # type: ignore
from utils.general_utils import PILtoTorch  # type: ignore
from utils.graphics_utils import fov2focal, focal2fov  # type: ignore
from utils import camera_utils  # type: ignore
from utils.sh_utils import SH2RGB  # type: ignore
import scene.dataset_readers  # type: ignore
from scene.dataset_readers import SceneInfo, getNerfppNorm, focal2fov  # type: ignore
from scene.dataset_readers import CameraInfo as _old_CameraInfo  # type: ignore
from scene.dataset_readers import storePly, fetchPly  # type: ignore
from utils.sh_utils import RGB2SH  # type: ignore



def flatten_hparams(hparams, *, separator: str = "/", _prefix: str = ""):
    flat = {}
    if dataclasses.is_dataclass(hparams):
        hparams = {f.name: getattr(hparams, f.name) for f in dataclasses.fields(hparams)}
    for k, v in hparams.items():
        if _prefix:
            k = f"{_prefix}{separator}{k}"
        if isinstance(v, dict) or dataclasses.is_dataclass(v):
            flat.update(flatten_hparams(v, _prefix=k, separator=separator).items())
        else:
            flat[k] = v
    return flat


def getProjectionMatrixFromOpenCV(w, h, fx, fy, cx, cy, znear, zfar):
    z_sign = 1.0
    P = torch.zeros((4, 4))
    P[0, 0] = 2.0 * fx / w
    P[1, 1] = 2.0 * fy / h
    P[0, 2] = (2.0 * cx - w) / w
    P[1, 2] = (2.0 * cy - h) / h
    P[3, 2] = z_sign
    P[2, 2] = z_sign * zfar / (zfar - znear)
    P[2, 3] = -(zfar * znear) / (zfar - znear)
    return P


#
# Patch Gaussian Splatting to include sampling masks
# Also, fix cx, cy (ignored in gaussian-splatting)
#
# Patch loadCam to include sampling mask
_old_loadCam = camera_utils.loadCam
def loadCam(args, id, cam_info, resolution_scale):
    camera = _old_loadCam(args, id, cam_info, resolution_scale)

    sampling_mask = None
    if cam_info.sampling_mask is not None:
        sampling_mask = PILtoTorch(cam_info.sampling_mask, (camera.image_width, camera.image_height))
    setattr(camera, "sampling_mask", sampling_mask)
    setattr(camera, "_patched", True)

    # Fix cx, cy (ignored in gaussian-splatting)
    camera.focal_x = fov2focal(cam_info.FovX, camera.image_width)
    camera.focal_y = fov2focal(cam_info.FovY, camera.image_height)
    camera.cx = cam_info.cx
    camera.cy = cam_info.cy
    camera.projection_matrix = getProjectionMatrixFromOpenCV(
        camera.image_width, 
        camera.image_height, 
        camera.focal_x, 
        camera.focal_y, 
        camera.cx, 
        camera.cy, 
        camera.znear, 
        camera.zfar).transpose(0, 1).cuda()
    camera.full_proj_transform = (camera.world_view_transform.unsqueeze(0).bmm(camera.projection_matrix.unsqueeze(0))).squeeze(0)

    return camera
camera_utils.loadCam = loadCam


# Patch CameraInfo to add sampling mask
class CameraInfo(_old_CameraInfo):
    def __new__(cls, *args, sampling_mask=None, cx, cy, **kwargs):
        self = super(CameraInfo, cls).__new__(cls, *args, **kwargs)
        self.sampling_mask = sampling_mask
        self.cx = cx
        self.cy = cy
        return self
scene.dataset_readers.CameraInfo = CameraInfo


def _load_caminfo(idx, pose, intrinsics, image_name, image_size, image=None, image_path=None, sampling_mask=None, scale_coords=None):
    pose = np.copy(pose)
    pose = np.concatenate([pose, np.array([[0, 0, 0, 1]], dtype=pose.dtype)], axis=0)
    pose = np.linalg.inv(pose)
    R = pose[:3, :3]
    T = pose[:3, 3]
    if scale_coords is not None:
        T = T * scale_coords
    R = np.transpose(R)

    width, height = image_size
    fx, fy, cx, cy = intrinsics
    if image is None:
        image = Image.fromarray(np.zeros((height, width, 3), dtype=np.uint8))
    return CameraInfo(
        uid=idx, R=R, T=T, 
        FovX=focal2fov(float(fx), float(width)),
        FovY=focal2fov(float(fy), float(height)),
        image=image, image_path=image_path, image_name=image_name, 
        width=int(width), height=int(height),
        sampling_mask=sampling_mask,
        cx=cx, cy=cy)


def _config_overrides_to_args_list(args_list, config_overrides):
    for k, v in config_overrides.items():
        if str(v).lower() == "true":
            v = True
        if str(v).lower() == "false":
            v = False
        if isinstance(v, bool):
            if v:
                if f'--no-{k}' in args_list:
                    args_list.remove(f'--no-{k}')
                if f'--{k}' not in args_list:
                    args_list.append(f'--{k}')
            else:
                if f'--{k}' in args_list:
                    args_list.remove(f'--{k}')
                else:
                    args_list.append(f"--no-{k}")
        elif f'--{k}' in args_list:
            args_list[args_list.index(f'--{k}') + 1] = str(v)
        else:
            args_list.append(f"--{k}")
            args_list.append(str(v))


def _convert_dataset_to_gaussian_splatting(dataset: Optional[Dataset], tempdir: str, white_background: bool = False, scale_coords=None):
    if dataset is None:
        return SceneInfo(None, [], [], nerf_normalization=dict(radius=None, translate=None), ply_path=None)
    assert np.all(dataset["cameras"].camera_models == camera_model_to_int("pinhole")), "Only pinhole cameras supported"

    cam_infos = []
    for idx, extr in enumerate(dataset["cameras"].poses):
        del extr
        intrinsics = dataset["cameras"].intrinsics[idx]
        pose = dataset["cameras"].poses[idx]
        image_path = dataset["image_paths"][idx] if dataset["image_paths"] is not None else f"{idx:06d}.png"
        image_name = (
            os.path.relpath(str(dataset["image_paths"][idx]), str(dataset["image_paths_root"])) if dataset["image_paths"] is not None and dataset["image_paths_root"] is not None else os.path.basename(image_path)
        )

        w, h = dataset["cameras"].image_sizes[idx]
        im_data = dataset["images"][idx][:h, :w]
        assert im_data.dtype == np.uint8, "Gaussian Splatting supports images as uint8"
        if white_background and im_data.shape[-1] == 4:
            bg = np.array([1, 1, 1])
            norm_data = im_data / 255.0
            arr = norm_data[:, :, :3] * norm_data[:, :, 3:4] + (1 - norm_data[:, :, 3:4]) * bg
            im_data = np.array(arr * 255.0, dtype=np.uint8)
        if not white_background and dataset["metadata"].get("id") == "blender":
            warnings.warn("Blender scenes are expected to have white background. If the background is not white, please set white_background=True in the dataset loader.")
        elif white_background and dataset["metadata"].get("id") != "blender":
            warnings.warn("white_background=True is set, but the dataset is not a blender scene. The background may not be white.")
        image = Image.fromarray(im_data)
        sampling_mask = None
        if dataset["sampling_masks"] is not None:
            sampling_mask = Image.fromarray((dataset["sampling_masks"][idx] * 255).astype(np.uint8))

        cam_info = _load_caminfo(
            idx, pose, intrinsics, 
            image_name=image_name, 
            image_path=image_path,
            image_size=(w, h),
            image=image,
            sampling_mask=sampling_mask,
            scale_coords=scale_coords,
        )
        cam_infos.append(cam_info)

    cam_infos = sorted(cam_infos.copy(), key=lambda x: x.image_name)
    nerf_normalization = getNerfppNorm(cam_infos)

    points3D_xyz = dataset["points3D_xyz"]
    if scale_coords is not None:
        points3D_xyz = points3D_xyz * scale_coords
    points3D_rgb = dataset["points3D_rgb"]
    if points3D_xyz is None and dataset["metadata"].get("id", None) == "blender":
        # https://github.com/graphdeco-inria/gaussian-splatting/blob/2eee0e26d2d5fd00ec462df47752223952f6bf4e/scene/dataset_readers.py#L221C4-L221C4
        num_pts = 100_000
        logging.info(f"generating random point cloud ({num_pts})...")

        # We create random points inside the bounds of the synthetic Blender scenes
        points3D_xyz = np.random.random((num_pts, 3)) * 2.6 - 1.3
        shs = np.random.random((num_pts, 3)) / 255.0
        points3D_rgb = (SH2RGB(shs) * 255).astype(np.uint8)

    storePly(os.path.join(tempdir, "scene.ply"), points3D_xyz, points3D_rgb)
    pcd = fetchPly(os.path.join(tempdir, "scene.ply"))
    scene_info = SceneInfo(point_cloud=pcd, train_cameras=cam_infos, test_cameras=[], nerf_normalization=nerf_normalization, ply_path=os.path.join(tempdir, "scene.ply"))
    return scene_info


# Patch GaussianModel to be able to render provided embeddings
class GaussianModel(_old_GaussianModel):
    @property
    def get_appearance(self):
        temp_embedding = getattr(self, "_temp_appearance", None)
        if temp_embedding is not None:
            return lambda cams: temp_embedding.expand(*cams.shape, -1)
        return self.embedding_appearance



class ScaffoldGS(Method):
    def __init__(self, *,
                 checkpoint: Optional[str] = None,
                 train_dataset: Optional[Dataset] = None,
                 config_overrides: Optional[dict] = None):
        self.checkpoint = checkpoint
        self.background = None
        self.step = 0

        # Setup parameters
        self._args_list = ["--source_path", "<empty>", "--resolution", "1", "--eval"]
        self._loaded_step = None
        if checkpoint is not None:
            if not os.path.exists(checkpoint):
                raise RuntimeError(f"Model directory {checkpoint} does not exist")
            with open(os.path.join(checkpoint, "args.txt"), "r", encoding="utf8") as f:
                self._args_list = shlex.split(f.read())
            self._loaded_step = sorted(int(x[len("iteration_"):]) for x in os.listdir(os.path.join(str(checkpoint), "point_cloud")) if x.startswith("iteration_"))[-1]

        if self.checkpoint is None and config_overrides is not None:
            _config_overrides_to_args_list(self._args_list, config_overrides)

        self._load_config()
        self._setup(train_dataset)

    def _load_config(self):
        parser = ArgumentParser(description="Training script parameters")
        lp = ModelParams(parser)
        op = OptimizationParams(parser)
        pp = PipelineParams(parser)
        parser.add_argument("--scale_coords", type=float, default=None, help="Scale the coords")
        parser.add_argument("--test_optim_lr", type=float, default=0.1, help="Test-time optimization learning rate")
        parser.add_argument("--test_optim_steps", type=int, default=128, help="Test-time optimization steps")
        args = parser.parse_args(self._args_list)
        self.dataset = lp.extract(args)
        self.dataset.scale_coords = args.scale_coords
        self.opt = op.extract(args)
        self.opt.test_optim_lr = args.test_optim_lr
        self.opt.test_optim_steps = args.test_optim_steps
        self.pipe = pp.extract(args)

    def _setup(self, train_dataset):
        # Initialize system state (RNG)
        safe_state(False)

        # Setup model
        self.gaussians = GaussianModel(self.dataset.feat_dim, 
                                       self.dataset.n_offsets, 
                                       self.dataset.voxel_size, 
                                       self.dataset.update_depth, 
                                       self.dataset.update_init_factor, 
                                       self.dataset.update_hierachy_factor, 
                                       self.dataset.use_feat_bank, 
                                       self.dataset.appearance_dim, 
                                       self.dataset.ratio, 
                                       self.dataset.add_opacity_dist, 
                                       self.dataset.add_cov_dist, 
                                       self.dataset.add_color_dist)
        # Fix bug https://github.com/city-super/Scaffold-GS/issues/43
        self.gaussians._local = None
        self.gaussians.denom = None
        self.scene = self._build_scene(train_dataset)

        if train_dataset is not None:
            self.gaussians.training_setup(self.opt)
        if self.checkpoint is not None:
            info = self.get_info()
            loaded_step = info.get("loaded_step")
            self.step = loaded_step
            assert loaded_step is not None, "Could not infer loaded step"
            if train_dataset is not None:
                warnings.warn(f"Restoring model without the optimizer state. Training should not be resumed.")
            # Fix bug in Scaffold-GS
            # (model_params, self.step) = torch.load(str(self.checkpoint) + f"/chkpnt{loaded_step}.pth")
            # model_params = (None,) + model_params
            # self.gaussians.restore(model_params, self.opt)

        bg_color = [1, 1, 1] if self.dataset.white_background else [0, 0, 0]
        self.background = torch.tensor(bg_color, dtype=torch.float32, device="cuda")
        self._viewpoint_stack = []
        self._input_points = None
        if train_dataset is not None:
            self._input_points = (train_dataset["points3D_xyz"], train_dataset["points3D_rgb"])

    @classmethod
    def get_method_info(cls):
        return MethodInfo(
            method_id="",
            required_features=frozenset(("color", "points3D_xyz")),
            supported_camera_models=frozenset(("pinhole",)),
            supported_outputs=("color",),
        )

    def get_info(self) -> ModelInfo:
        hparams = flatten_hparams(dict(itertools.chain(vars(self.dataset).items(), vars(self.opt).items(), vars(self.pipe).items()))) 
        for k in ("source_path", "resolution", "eval", "images", "model_path", "data_device"):
            hparams.pop(k, None)
        return ModelInfo(
            num_iterations=self.opt.iterations,
            loaded_step=self._loaded_step,
            loaded_checkpoint=self.checkpoint,
            hparams=hparams,
            **self.get_method_info(),
        )

    def _build_scene(self, dataset):
        opt = copy.copy(self.dataset)
        with tempfile.TemporaryDirectory() as td:
            os.mkdir(td + "/sparse")
            opt.source_path = td  # To trigger colmap loader
            opt.model_path = str(self.checkpoint) if self.checkpoint is not None else td
            backup = sceneLoadTypeCallbacks["Colmap"]
            try:
                info = self.get_info()
                def colmap_loader(*args, **kwargs):
                    del args, kwargs
                    return _convert_dataset_to_gaussian_splatting(dataset, td, white_background=self.dataset.white_background, scale_coords=self.dataset.scale_coords)
                sceneLoadTypeCallbacks["Colmap"] = colmap_loader
                loaded_step = info.get("loaded_step")
                scene = Scene(opt, self.gaussians, load_iteration=str(loaded_step) if self.checkpoint is not None else None, shuffle=False)
                return scene
            finally:
                sceneLoadTypeCallbacks["Colmap"] = backup

    def render(self, camera: Cameras, *, options=None) -> RenderOutput:
        camera = camera.item()
        assert camera.camera_models == camera_model_to_int("pinhole"), "Only pinhole cameras supported"

        bg_color = [1,1,1] if self.dataset.white_background else [0, 0, 0]
        background = torch.tensor(bg_color, dtype=torch.float32, device="cuda")

        with torch.no_grad():
            viewpoint_cam = _load_caminfo(0, camera.poses, camera.intrinsics, f"{0:06d}.png", camera.image_sizes, scale_coords=self.dataset.scale_coords)
            viewpoint = loadCam(self.dataset, 0, viewpoint_cam, 1.0)

            embedding = (options or {}).get("embedding", None)
            self.gaussians._temp_appearance = None
            if embedding is not None:
                self.gaussians._temp_appearance = torch.from_numpy(embedding).cuda()

            voxel_visible_mask = prefilter_voxel(viewpoint, self.gaussians, self.pipe, background)
            render_pkg = render(viewpoint, self.gaussians, self.pipe, background, visible_mask=voxel_visible_mask)
            image = torch.clamp(render_pkg["render"], 0.0, 1.0)
            color = image.detach().permute(1, 2, 0).cpu().numpy()
            return {
                "color": color,
            }

    def train_iteration(self, step):
        self.step = step
        iteration = step + 1  # Gaussian Splatting is 1-indexed
        del step

        self.gaussians.update_learning_rate(iteration)

        bg_color = [1, 1, 1] if self.dataset.white_background else [0, 0, 0]
        background = torch.tensor(bg_color, dtype=torch.float32, device="cuda")

        # Pick a random Camera
        if not self._viewpoint_stack:
            loadCam.was_called = False  # type: ignore
            self._viewpoint_stack = self.scene.getTrainCameras().copy()
            if any(not getattr(cam, "_patched", False) for cam in self._viewpoint_stack):
                raise RuntimeError("could not patch loadCam!")
        viewpoint_cam = self._viewpoint_stack.pop(randint(0, len(self._viewpoint_stack) - 1))

        voxel_visible_mask = prefilter_voxel(viewpoint_cam, self.gaussians, self.pipe, background)
        retain_grad = (iteration < self.opt.update_until and iteration >= 0)

        # Reset previous appearance
        self.gaussians._temp_appearance = None
        render_pkg = render(viewpoint_cam, self.gaussians, self.pipe, background, 
                            visible_mask=voxel_visible_mask, retain_grad=retain_grad)
        
        image, viewspace_point_tensor, visibility_filter, offset_selection_mask, radii, scaling, opacity = render_pkg["render"], render_pkg["viewspace_points"], render_pkg["visibility_filter"], render_pkg["selection_mask"], render_pkg["radii"], render_pkg["scaling"], render_pkg["neural_opacity"]
        del radii

        gt_image = viewpoint_cam.original_image.cuda()


        # NOTE: Modified to include sampling mask
        # Apply mask
        sampling_mask = viewpoint_cam.sampling_mask.cuda() if viewpoint_cam.sampling_mask is not None else None
        if sampling_mask is not None:
            image = image * sampling_mask + (1.0 - sampling_mask) * image.detach()

        Ll1 = l1_loss(image, gt_image)

        ssim_loss = (1.0 - ssim(image, gt_image))
        scaling_reg = scaling.prod(dim=1).mean()
        loss = (1.0 - self.opt.lambda_dssim) * Ll1 + self.opt.lambda_dssim * ssim_loss + 0.01*scaling_reg

        loss.backward()
        
        with torch.no_grad():
            # Compute metrics
            psnr_value = 10 * torch.log10(1 / torch.mean((image - gt_image) ** 2))
            metrics = {
                "l1_loss": Ll1.detach().cpu().item(), 
                "loss": loss.detach().cpu().item(), 
                "psnr": psnr_value.detach().cpu().item(),
            }

            # densification
            if iteration < self.opt.update_until and iteration > self.opt.start_stat:
                # add statis
                self.gaussians.training_statis(viewspace_point_tensor, opacity, visibility_filter, offset_selection_mask, voxel_visible_mask)
                
                # densification
                if iteration > self.opt.update_from and iteration % self.opt.update_interval == 0:
                    self.gaussians.adjust_anchor(check_interval=self.opt.update_interval, success_threshold=self.opt.success_threshold, grad_threshold=self.opt.densify_grad_threshold, min_opacity=self.opt.min_opacity)
            elif iteration == self.opt.update_until:
                del self.gaussians.opacity_accum
                del self.gaussians.offset_gradient_accum
                del self.gaussians.offset_denom
                torch.cuda.empty_cache()
                    
            # Optimizer step
            if iteration < self.opt.iterations:
                self.gaussians.optimizer.step()
                self.gaussians.optimizer.zero_grad(set_to_none = True)

        self.step = self.step + 1
        return metrics

    def save(self, path: str):
        os.makedirs(path, exist_ok=True)
        self.gaussians.save_ply(os.path.join(str(path), f"point_cloud/iteration_{self.step}", "point_cloud.ply"))
        self.gaussians.save_mlp_checkpoints(os.path.join(str(path), f"point_cloud/iteration_{self.step}"))
        # We do not save the optim state since the schedulers are not saved in the ScaffoldGS code
        # and training cannot be resumed in either case.
        # torch.save((self.gaussians.capture(), self.step), str(path) + f"/chkpnt{self.step}.pth")
        with open(str(path) + "/args.txt", "w", encoding="utf8") as f:
            f.write(" ".join(shlex.quote(x) for x in self._args_list))

        # Since pt files in point_cloud/iteration_{self.step} contain traced versions of params already in chkpnt,
        # we can ignore them (they have a different binary representation every save so we can't compare them)
        for file in os.listdir(os.path.join(path, "point_cloud", f"iteration_{self.step}")):
            if file.endswith(".pt"):
                with open(os.path.join(path, "point_cloud", f"iteration_{self.step}", file + ".sha256"), "w") as f:
                    f.write(hashlib.sha256(b"").hexdigest())

    def optimize_embedding(self, dataset: Dataset, *, embedding: Optional[np.ndarray] = None) -> OptimizeEmbeddingOutput:
        """
        Optimize embeddings for each image in the dataset.

        Args:
            dataset: Dataset.
            embeddings: Optional initial embeddings.
        """
        camera = dataset["cameras"].item()
        assert camera.camera_models == camera_model_to_int("pinhole"), "Only pinhole cameras supported"

        bg_color = [1,1,1] if self.dataset.white_background else [0, 0, 0]
        background = torch.tensor(bg_color, dtype=torch.float32, device="cuda")

        if embedding is not None:
            embedding_th = torch.from_numpy(embedding)
        else:
            # Get default embedding
            self.gaussians._temp_appearance = None
            embedding_th = self.gaussians.get_appearance.embedding.weight.detach().mean(0).clone()  # type: ignore

        with torch.enable_grad():
            losses, psnrs, mses = [], [], []

            gt_image = torch.tensor(convert_image_dtype(dataset["images"][0], np.float32), dtype=torch.float32).cuda().permute(2, 0, 1)
            gt_mask = torch.tensor(convert_image_dtype(dataset["sampling_masks"][0], np.float32), dtype=torch.float32).cuda()[..., None].permute(2, 0, 1) if dataset["sampling_masks"] is not None else None

            viewpoint_cam = _load_caminfo(0, camera.poses, camera.intrinsics, f"{0:06d}.png", camera.image_sizes, scale_coords=self.dataset.scale_coords)
            viewpoint = loadCam(self.dataset, 0, viewpoint_cam, 1.0)
            voxel_visible_mask = prefilter_voxel(viewpoint, self.gaussians, self.pipe, background)

            embedding_param = torch.nn.Parameter(embedding_th.cuda().requires_grad_())
            optim = torch.optim.Adam([embedding_param], lr=self.opt.test_optim_lr)
            for _ in range(self.opt.test_optim_steps):
                optim.zero_grad()
                self.gaussians._temp_appearance = embedding_param
                render_pkg = render(viewpoint, self.gaussians, self.pipe, background, visible_mask=voxel_visible_mask)
                image = render_pkg["render"]
                if gt_mask is not None:
                    image = image * gt_mask + (1.0 - gt_mask) * image.detach()
                loss = mse = torch.nn.functional.mse_loss(image, gt_image)
                loss.backward()
                optim.step()

                losses.append(loss.detach().cpu().item())
                mses.append(mse.detach().cpu().item())
                psnrs.append(20 * math.log10(1.0) - 10 * torch.log10(mse).detach().cpu().item())

            self.gaussians._temp_appearance = None
            return {
                "embedding": embedding_param.detach().cpu().numpy(),
                "metrics": {
                    "psnr": psnrs,
                    "mse": mses,
                    "loss": losses,
                }
            }

    def get_train_embedding(self, index: int) -> Optional[np.ndarray]:
        """
        Get the embedding for a training image.

        Args:
            index: Index of the image.
        """
        if self.gaussians.appearance_dim > 0:
            self.gaussians._temp_appearance = None
            return self.gaussians.get_appearance(
                torch.tensor(index, dtype=torch.long, device="cuda")).detach().cpu().numpy()
        return None


    def export_demo(self, path: str, *, options=None):
        from nerfbaselines.utils import apply_transform, invert_transform
        from ._gaussian_splatting_demo import export_demo
        os.makedirs(path, exist_ok=True)
        options = (options or {}).copy()
        dataset_metadata = options.get("dataset_metadata") or {}
        logging.warning("Scaffold-GS does not support view-dependent demo. We will bake the appearance of a single appearance embedding and single viewing direction.")

        with torch.no_grad():
            device = torch.device("cuda")
            if "viewer_transform" in dataset_metadata and "viewer_initial_pose" in dataset_metadata:
                viewer_initial_pose_ws = apply_transform(invert_transform(dataset_metadata["viewer_transform"], has_scale=True), dataset_metadata["viewer_initial_pose"])
                camera_center = torch.tensor(viewer_initial_pose_ws[:3, 3], dtype=torch.float32, device=device)
            else:
                camera_center = torch.tensor([1.0, 0.0, 0.0], dtype=torch.float32, device=device)
            viewpoint_cam = namedtuple("Camera", ["camera_center", "uid"])(camera_center=camera_center*(self.dataset.scale_coords or 1), uid=0)
            embedding = options.pop("embedding", None)
            self.gaussians._temp_appearance = None
            if embedding is not None:
                self.gaussians._temp_appearance = torch.from_numpy(embedding).to(device)

            xyz, color, opacity, scaling, rot = generate_neural_gaussians(viewpoint_cam, self.gaussians, visible_mask=None, is_training=False)
            export_demo(path, 
                        options=options,
                        xyz=xyz.detach().cpu().numpy(),
                        scales=scaling.detach().cpu().numpy(),
                        opacities=opacity.detach().cpu().numpy(),
                        quaternions=torch.nn.functional.normalize(rot).detach().cpu().numpy(),
                        spherical_harmonics=RGB2SH(color[..., None]).detach().cpu().numpy())

