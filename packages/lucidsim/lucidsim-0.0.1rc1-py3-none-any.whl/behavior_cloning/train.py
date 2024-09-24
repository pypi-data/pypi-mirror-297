import h5py
import numpy as np
import os
import random
import torch
import torchvision.transforms.v2 as T
from ml_logger import ML_Logger
from params_proto import ParamsProto, Proto
from torch import nn
from typing import Literal

from behavior_cloning.datasets.loader import DataLoader
from behavior_cloning.datasets.stacked_loader import StackedLoader
from behavior_cloning.go1_model.actor import BasicRGBActor
from behavior_cloning.go1_model.ball_actor import BallRGBActor
from behavior_cloning.model import get_soda_model
from cxx.modules.depth_backbone import RecurrentDepthBackbone
from cxx.modules.parkour_actor import ParkourActor, PolicyArgs

THIGH_IDXS = [1, 4, 7, 10]


class TrainCfg(ParamsProto, prefix="train"):
    datasets: str = Proto(env="$DATASETS/lucidsim")

    # dataset_prefix = "scenes/domain_randomization_v1/extensions_cones_stairs_wh_v1"
    # dataset_prefix = "lucidsim/lucidsim/corl/lucidsim_datasets/extension_stairs_wh_cones_gpt_prompts_v1"
    # dataset_prefix = "scenes/domain_randomization_5_v1/chase_soccer_v1"

    # dataset_prefix = [
    #     "lucidsim/lucidsim/corl/lucidsim_datasets/chase_soccer_ball_grassy_courtyard_prompts_v2",
    #     "lucidsim/lucidsim/corl/lucidsim_datasets/chase_soccer_ball_lab_blue_carpet_prompts_v1",
    #     "lucidsim/lucidsim/corl/lucidsim_datasets/chase_soccer_ball_red_brick_courtyard_prompts_v1",
    # ]

    dataset_prefix = [
        "scenes/depth/chase_soccer_cones_realsense_v1",
    ]

    h5_load = True

    train_split = 0.8

    image_type: Literal["rgb", "depth", "augmented"] = "depth"
    imagenet_pipe = False

    # for any non imagenet pipe
    image_dim = 3

    image_size = (45, 80)
    num_filters = 64
    num_shared_layers = 10

    # crop_image_size = (720, 1280)
    crop_image_size = None
    # crop_w = int(np.tan(np.deg2rad(69.15 / 2)) / np.tan(np.deg2rad(60)) * 160)
    # crop_h = int(np.tan(np.deg2rad(42.61 / 2)) / np.tan(np.deg2rad(45)) * 90)

    # crop_image_size = (crop_h, crop_w)

    # training params
    batch_size = 32
    n_epochs = 500
    shuffle = True  # can't shuffle for recurrent models
    max_grad_norm: float = None  # 1.0
    data_aug = ["crop", "rotate", "color", "perspective"]

    # optimization
    optimizer = "adam"
    lr = 0.00005
    lr_schedule = True

    momentum = 0.9
    weight_decay = 5e-4

    # checkpointing
    checkpoint_interval: int = 50

    normalize_depth = True

    train_yaw = True

    # the older frames will be fed in as differences with the most recent frame
    recurrent = False
    use_stacked_dreams = True
    compute_deltas = False
    drop_last = False
    stack_size = 5

    # system
    seed = 100
    device = "cuda" if torch.cuda.is_available() else "cpu"

    freeze_teacher_modules = False

    gpu_load = True  # whether to load all images into GPU memory

    teacher_checkpoint = "/lucid-sim/lucid-sim/baselines/launch_gains/2024-03-20/04.03.35/go1/300/20/0.5/checkpoints/model_last.pt"

    debug = False  # "pydevd" in sys.modules


print(TrainCfg.datasets, TrainCfg.dataset_prefix)


def fetch_dreams():
    from ml_logger import logger

    # todo: make sure normalization is correct
    if TrainCfg.imagenet_pipe:
        pipeline = [
            T.ToImage(),
            T.ToDtype(torch.float32, scale=True),
            T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ]
    else:
        pipeline = [
            T.ToImage(),
            T.ToDtype(torch.float32, scale=False),
            T.Normalize(mean=[127.5] * TrainCfg.image_dim, std=[255] * TrainCfg.image_dim),
        ]

    logger.print(f"Using pipeline {pipeline}")
    augs = {
        "crop": T.RandomCrop(TrainCfg.image_size, padding=4),
        "rotate": T.RandomRotation(degrees=5),
        "color": T.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2, hue=0.1),
        "perspective": T.RandomPerspective(distortion_scale=0.2, p=0.3),
        "blur": T.GaussianBlur(kernel_size=(3, 3), sigma=(0.1, 2.0)),
    }

    aug_pipeline = [augs[aug_name] for aug_name in TrainCfg.data_aug]

    # fmt: off
    transform_train = T.Compose([
        T.Resize(TrainCfg.image_size, interpolation=T.InterpolationMode.BILINEAR),
        *aug_pipeline,
        *pipeline,
    ])

    transform_eval = T.Compose([
        T.Resize(TrainCfg.image_size, interpolation=T.InterpolationMode.BILINEAR),
        *pipeline,
    ])
    # fmt: on

    if TrainCfg.use_stacked_dreams or TrainCfg.recurrent:
        loader_class = StackedLoader
    else:
        loader_class = DataLoader

    train_rollouts = []
    val_rollouts = []

    for dataset_prefix in TrainCfg.dataset_prefix:
        data_path = f"{TrainCfg.datasets}/{dataset_prefix}"

        if os.path.isfile(f"{data_path}.hdf5"):
            rollouts = set()
            file = h5py.File(f"{data_path}.hdf5", "r+")
            rollouts = sorted(set([k.split("_")[0] for k in file.keys()]))
            rollouts = rollouts[: 2 if TrainCfg.debug else None]
        else:
            rollout_logger = ML_Logger(root=TrainCfg.datasets, prefix=dataset_prefix)
            rollouts = rollout_logger.glob("*.pkl")
            rollouts = [r.split("_")[0] for r in rollouts][: 2 if TrainCfg.debug else None]

        print(f"Found {len(rollouts)} rollouts for {dataset_prefix}")

        # split the rollouts into train and validation split -- not for reporting test results.
        random.shuffle(rollouts)

        split = int(TrainCfg.train_split * len(rollouts)) + 1
        train_split = rollouts[:split]
        val_split = rollouts[split:]

        train_rollouts.append(train_split)
        val_rollouts.append(val_split)

    data_roots = [f"{TrainCfg.datasets}/{dataset_prefix}" for dataset_prefix in TrainCfg.dataset_prefix]

    train_loader = loader_class(
        tensor_size=TrainCfg.image_size,
        stack_size=TrainCfg.stack_size,
        logical_imd_dim=TrainCfg.image_dim,
        compute_deltas=TrainCfg.compute_deltas,
        local_dataset_root=data_roots,
        rollouts=train_rollouts,
        image_type=TrainCfg.image_type,
        device=TrainCfg.device,
        transform=transform_train,
        gpu_load=TrainCfg.gpu_load,
        h5_load=True,
        normalize_depth=TrainCfg.normalize_depth,
        crop_image_size=TrainCfg.crop_image_size,
    )

    val_loader = None
    if val_rollouts:
        val_loader = loader_class(
            tensor_size=TrainCfg.image_size,
            stack_size=TrainCfg.stack_size,
            logical_imd_dim=TrainCfg.image_dim,
            compute_deltas=TrainCfg.compute_deltas,
            local_dataset_root=data_roots,
            # specific to eval.
            rollouts=val_rollouts,
            image_type=TrainCfg.image_type,
            device=TrainCfg.device,
            transform=transform_eval,
            gpu_load=TrainCfg.gpu_load,
            h5_load=True,
            normalize_depth=TrainCfg.normalize_depth,
            crop_image_size=TrainCfg.crop_image_size,
        )

    return train_loader, val_loader


def train(train_loader, model, optimizer, teacher_model):
    """Train for one epoch on the training set."""
    from ml_logger import logger

    # switch to train mode
    model.train()

    # delay_mask = torch.ones()

    sampler = train_loader.sample_epoch(TrainCfg.batch_size, shuffle=TrainCfg.shuffle)

    for i, (camera, obs) in enumerate(sampler):
        # form depth buffer
        # TensorType["batch", "buffer", 1, "height", "width"]

        if TrainCfg.use_stacked_dreams:
            batch, stack, channels, height, width = camera.shape

            if TrainCfg.drop_last:
                # drop the most recent frame, and only keep the deltas
                camera = camera[:, :-1, :, :, :]

            camera = camera.reshape(batch, (stack - int(TrainCfg.drop_last)) * channels, height, width)

            obs = obs[:, -1, :]

        with torch.no_grad():
            teacher_actions, _ = teacher_model(None, obs)
            scandots = obs[:, model.n_proprio : model.n_proprio + model.n_scan]
            teacher_scandots_latent = teacher_model.actor.scan_encoder(scandots)
            gt_yaw = obs[:, 6:7]

        # used by cxx; around 0.6 - 0.7 is good
        loss = 0

        if TrainCfg.train_yaw:
            pred_actions, vision_latent, pred_yaw = model(camera, obs)
            yaw_loss = (gt_yaw - pred_yaw).norm(p=2, dim=1).mean()
            loss += yaw_loss
        else:
            pred_actions, vision_latent = model(camera, obs)
            yaw_loss = np.array(0)

        # note: action loss is never used. blows up according to Alan.
        action_loss = (teacher_actions - pred_actions).norm(p=2, dim=1).mean()
        latent_loss = (teacher_scandots_latent - vision_latent).norm(p=2, dim=1).mean()

        loss += latent_loss

        optimizer.zero_grad()
        loss.backward()

        if TrainCfg.max_grad_norm is not None:
            nn.utils.clip_grad_norm_(model.parameters(), TrainCfg.max_grad_norm)

        optimizer.step()

        logger.store_metrics({"train/action_loss": action_loss.item()})
        logger.store_metrics({"train/latent_loss": latent_loss.item()})
        logger.store_metrics({"train/yaw_loss": yaw_loss.item()})


def evaluate(val_loader, model, teacher_model):
    """Perform validation on the validation set."""
    from ml_logger import logger

    with torch.no_grad():
        # switch to evaluate mode
        model.eval()

        sampler = val_loader.sample_epoch(TrainCfg.batch_size, shuffle=TrainCfg.shuffle)

        for i, (camera, obs) in enumerate(sampler):
            if TrainCfg.use_stacked_dreams:
                batch, stack, channels, height, width = camera.shape

                if TrainCfg.drop_last:
                    # drop the most recent frame, and only keep the deltas
                    camera = camera[:, :-1, :, :, :]

                camera = camera.reshape(batch, (stack - int(TrainCfg.drop_last)) * channels, height, width)

                obs = obs[:, -1, :]

            teacher_actions, _ = teacher_model(None, obs)
            scandots = obs[:, model.n_proprio : model.n_proprio + model.n_scan]
            teacher_scandots_latent = teacher_model.actor.scan_encoder(scandots)
            gt_yaw = obs[:, 6:7]

            if TrainCfg.train_yaw:
                pred_actions, vision_latent, pred_yaw = model(camera, obs)
                yaw_loss = (gt_yaw - pred_yaw).norm(p=2, dim=1).mean()
            else:
                pred_actions, vision_latent = model(camera, obs)
                yaw_loss = np.array(0)

            # used by cxx; around 0.6 - 0.7 is good
            action_loss = (teacher_actions - pred_actions).norm(p=2, dim=1).mean()
            latent_loss = (teacher_scandots_latent - vision_latent).norm(p=2, dim=1).mean()

            logger.store_metrics({"eval/action_loss": action_loss.item()})
            logger.store_metrics({"eval/latent_loss": latent_loss.item()})
            logger.store_metrics({"eval/yaw_loss": yaw_loss.item()})


def main(_deps=None, **deps):
    from ml_logger import logger
    from lucidsim_analysis import RUN
    from behavior_cloning.go1_model.ball_actor import Go1RGBConfig

    print(logger.get_dash_url())

    TrainCfg._update(_deps, **deps)

    try:
        RUN._update(_deps)
        logger.configure(RUN.prefix)
    except KeyError:
        pass

    logger.job_started(TrainCfg=vars(TrainCfg))

    np.random.seed(TrainCfg.seed)
    torch.random.manual_seed(TrainCfg.seed)

    # this is not the bottleneck. Data loading is.
    torch.set_float32_matmul_precision("medium")  # or high
    torch.backends.cuda.matmul.allow_tf32 = True
    torch.backends.cudnn.allow_tf32 = True
    torch.backends.cudnn.benchmark = True

    # fmt: off
    logger.log_text("""
        charts:
        - yKeys: ["train/action_loss/mean", "eval/action_loss/mean"]
          xKey: epoch
        - yKeys: ["train/latent_loss/mean", "eval/latent_loss/mean"]
          xKey: epoch
        - yKeys: ["train/yaw_loss/mean", "eval/yaw_loss/mean"]
          xKey: epoch
        """, dedent=True, filename=".charts.yml", overwrite=True)
    # fmt: on

    logger.print("Loading data...")
    train_loader, val_loader = fetch_dreams()
    logger.print("Loading model...")

    logger.upload_file(__file__)

    # num_channels = 1 if TrainCfg.image_type == "depth" else 3
    num_channels = 3
    if TrainCfg.use_stacked_dreams:
        num_channels *= TrainCfg.stack_size - int(TrainCfg.drop_last)

    if TrainCfg.recurrent:
        raise NotImplementedError
        num_channels = 3

    vision_head = get_soda_model(
        inp_shape=(num_channels, *TrainCfg.image_size),
        num_filters=TrainCfg.num_filters,
        device=TrainCfg.device,
        projection_dim=Go1RGBConfig.scan_encoder_dims[-1],
        num_shared_layers=TrainCfg.num_shared_layers,
        coord_conv=False,
    )

    if TrainCfg.recurrent:
        vision_head = RecurrentDepthBackbone(
            vision_head,
            n_proprio=Go1RGBConfig.n_proprio + Go1RGBConfig.n_priv,
            ignore_yaw=True,
        )

    if TrainCfg.train_yaw:
        model = BallRGBActor(
            **vars(Go1RGBConfig),
            vision_head=vision_head,
            freeze_teacher_modules=TrainCfg.freeze_teacher_modules,
        )

    else:
        model = BasicRGBActor(
            **vars(Go1RGBConfig),
            vision_head=vision_head,
            freeze_teacher_modules=TrainCfg.freeze_teacher_modules,
        )

    model.to(TrainCfg.device)
    model.load_teacher_modules(TrainCfg.teacher_checkpoint, device=TrainCfg.device)

    teacher_model = ParkourActor()
    PolicyArgs.use_camera = False
    teacher_model.load(TrainCfg.teacher_checkpoint)
    teacher_model.to(TrainCfg.device)
    teacher_model.eval()

    logger.print("model has been loaded")
    logger.print(f"Number of parameters: {sum([p.data.nelement() for p in model.parameters()]):d}")

    if TrainCfg.optimizer == "adam":
        optimizer = torch.optim.Adam(
            model.parameters(),
            TrainCfg.lr,
            weight_decay=TrainCfg.weight_decay,
        )
    elif TrainCfg.optimizer == "sgd":
        optimizer = torch.optim.SGD(
            model.parameters(),
            TrainCfg.lr,
            momentum=TrainCfg.momentum,
            weight_decay=TrainCfg.weight_decay,
        )
    else:
        raise NotImplementedError

    if TrainCfg.lr_schedule:
        schedule = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=TrainCfg.n_epochs)

    logger.start("epoch")

    model.to(TrainCfg.device)

    for epoch in range(0, TrainCfg.n_epochs + 1):
        if TrainCfg.lr_schedule:
            schedule.step(epoch)

        if TrainCfg.checkpoint_interval and epoch % TrainCfg.checkpoint_interval == 0:
            logger.print("Saving checkpoints...")
            state_dict = model.state_dict()
            logger.save_torch(state_dict, f"checkpoints/net_{epoch}.pt")
            logger.duplicate(f"checkpoints/net_{epoch}.pt", "checkpoints/net_last.pt")

        train(train_loader, model, optimizer, teacher_model)
        if val_loader:
            evaluate(val_loader, model, teacher_model)

        logger.log_metrics_summary(key_values={"epoch": epoch, "dt_epoch": logger.split("epoch")})


if __name__ == "__main__":
    main()
