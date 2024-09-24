import os
import random
from pathlib import Path
from typing import Literal

import h5py
import numpy as np
import torch
import torchvision.transforms.v2 as T
from ml_logger import ML_Logger
from params_proto import ParamsProto, Proto, Flag
from torch import nn

from behavior_cloning.datasets.stacked_loader import StackedLoader
from behavior_cloning.go1_model.transformers.transformer_policy import TransformerPolicy
from cxx.modules.parkour_actor import ParkourActor, PolicyArgs

THIGH_IDXS = [1, 4, 7, 10]


class TrainCfg(ParamsProto, prefix="train"):
    datasets: str = Proto(env="$LUCIDSIM_DATASETS")

    dataset_prefix = Proto(
        [
            "lucidsim/lucidsim/datasets/unrolls/depth_ge_debug_v1/extensions_cones_gaps_many/expert/collection-00",
        ],
        help="list of folders containing the unroll data collections.",
    )

    teacher_checkpoint = Proto(
        "/lucid-sim/lucid-sim/baselines/launch_gains/2024-03-20/04.03.35/go1/300/20/0.5/checkpoints/model_last.pt",
        help="Path to the teacher model checkpoint. Required.",
    )
    student_checkpoint = Proto(help="Path to the student model checkpoint. Set to None for first unroll.")

    use_batchnorm = Proto(False, help="Not needed for depth student")
    image_type: Literal["rgb", "depth", "augmented", "augmented_7"] = "depth"

    train_split = 0.9
    train_yaw = False

    delay = 0

    yaw_loss_weight = 10.0

    logical_img_dim = 1
    imagenet_pipe = False

    stack_size = 7
    image_latent_dim = 64
    head_dim = 128
    num_layers = 5
    dropout = 0.1
    image_size = (45, 80)
    use_causal_mask: bool = Flag("Use causal mask for transformer", default=False)

    crop_image_size = None

    # training params
    batch_size = 256
    n_epochs = 70
    shuffle = True  # can't shuffle for recurrent models
    max_grad_norm = None # 0.25

    # perspective is often not good.
    data_aug = ("crop", "rotate", "perspective", "color")

    # optimization
    optimizer = "adam"
    lr = 0.0005
    lr_schedule = True

    momentum = 0.9
    weight_decay = 5e-4

    # checkpointing
    checkpoint_interval: int = 10

    # system
    seed = 100
    device = "cuda" if torch.cuda.is_available() else "cpu"

    freeze_teacher_modules = False

    gpu_load = True  # whether to load all images into GPU memory
    h5_load = True

    debug = False  # "pydevd" in sys.modules


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
            T.Normalize(mean=[127.5] * TrainCfg.logical_img_dim, std=[255] * TrainCfg.logical_img_dim),
            # T.Normalize(mean=[123.15, 138.13, 64.05], std=[44, 44, 44]),
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

    # get rollouts
    train_rollouts = []
    val_rollouts = []

    for dataset_prefix in TrainCfg.dataset_prefix:
        data_path = f"{TrainCfg.datasets}/{dataset_prefix}"

        if os.path.isfile(f"{data_path}.hdf5"):
            print("loading hdf5 files")
            file = h5py.File(f"{data_path}.hdf5", "r+")
            rollouts = sorted(set([k.split("_")[0] for k in file.keys()]))
            rollouts = rollouts[: 2 if TrainCfg.debug else None]
        else:
            print("loading pickle files")
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

    train_loader = StackedLoader(
        tensor_size=TrainCfg.image_size,
        stack_size=TrainCfg.stack_size,
        logical_imd_dim=TrainCfg.logical_img_dim,
        local_dataset_root=data_roots,
        rollouts=train_rollouts,
        image_type=TrainCfg.image_type,
        device=TrainCfg.device,
        transform=transform_train,
        gpu_load=TrainCfg.gpu_load,
        h5_load=TrainCfg.h5_load,
        crop_image_size=TrainCfg.crop_image_size,
        delay=TrainCfg.delay,
    )

    val_loader = None
    if val_rollouts and not TrainCfg.debug:
        val_loader = StackedLoader(
            tensor_size=TrainCfg.image_size,
            stack_size=TrainCfg.stack_size,
            logical_imd_dim=TrainCfg.logical_img_dim,
            local_dataset_root=data_roots,
            # specific to eval.
            rollouts=val_rollouts,
            image_type=TrainCfg.image_type,
            device=TrainCfg.device,
            transform=transform_eval,
            gpu_load=TrainCfg.gpu_load,
            h5_load=TrainCfg.h5_load,
            crop_image_size=TrainCfg.crop_image_size,
            delay=TrainCfg.delay,
        )

    return train_loader, val_loader


def train(train_loader, transformer_policy, optimizer, teacher_model):
    """Train for one epoch on the training set."""
    from ml_logger import logger

    # switch to train mode
    transformer_policy.train()

    # delay_mask = torch.ones()
    batch_size = TrainCfg.batch_size if not TrainCfg.debug else 1
    sampler = train_loader.sample_epoch(batch_size, shuffle=TrainCfg.shuffle)

    for i, (frames, obs) in enumerate(sampler):
        batch, stack, channels, height, width = frames.shape

        # pick the current one.
        curr_obs = obs[:, -1, :]
        obs_history = obs[:, :, :53]

        with torch.no_grad():
            teacher_actions, _ = teacher_model(None, curr_obs)
            scandots = curr_obs[:, teacher_model.n_proprio : teacher_model.n_proprio + teacher_model.n_scan]
            teacher_scandots_latent = teacher_model.actor.scan_encoder(scandots)
            gt_yaw = curr_obs[:, 6:8]

        if TrainCfg.train_yaw:
            act_pred, pred_yaw = transformer_policy.forward_yaw(frames, obs_history)
            # pred_actions, vision_latent, pred_yaw = model(frames, curr_obs)
            yaw_loss = (gt_yaw - pred_yaw).norm(p=2, dim=1).mean()
            logger.store_metrics({"train/yaw_loss": yaw_loss.item()})
        else:
            act_pred = transformer_policy(frames, obs_history)
            # pred_actions, vision_latent = model(frames, curr_obs)

        # note: action loss is never used. blows up according to Alan.
        action_loss = (teacher_actions - act_pred).norm(p=2, dim=1).mean()
        logger.store_metrics({"train/action_loss": action_loss.item()})

        # latent_loss = (teacher_scandots_latent - vision_latent).norm(p=2, dim=1).mean()
        # logger.store_metrics({"train/latent_loss": latent_loss.item()})

        loss = action_loss

        if TrainCfg.train_yaw:
            loss += TrainCfg.yaw_loss_weight * yaw_loss

        optimizer.zero_grad()
        loss.backward()

        if TrainCfg.max_grad_norm is not None:
            nn.utils.clip_grad_norm_(transformer_policy.parameters(), TrainCfg.max_grad_norm)

        optimizer.step()


def evaluate(val_loader, transformer_policy, teacher_model):
    """Perform validation on the validation set."""
    from ml_logger import logger

    with torch.no_grad():
        # switch to evaluate mode
        transformer_policy.eval()

        batch_size = TrainCfg.batch_size if not TrainCfg.debug else 1
        sampler = val_loader.sample_epoch(batch_size, shuffle=TrainCfg.shuffle)

        for i, (frames, obs) in enumerate(sampler):
            batch, stack, channels, height, width = frames.shape

            # pick the current one.
            curr_obs = obs[:, -1, :]
            obs_history = obs[:, :, :53]

            teacher_actions, _ = teacher_model(None, curr_obs)
            scandots = curr_obs[:, teacher_model.n_proprio : teacher_model.n_proprio + teacher_model.n_scan]
            teacher_scandots_latent = teacher_model.actor.scan_encoder(scandots)
            gt_yaw = curr_obs[:, 6:8]

            if TrainCfg.train_yaw:
                act_pred, pred_yaw = transformer_policy.forward_yaw(frames, obs_history)
                yaw_loss = (gt_yaw - pred_yaw).norm(p=2, dim=1).mean()
                logger.store_metrics({"eval/yaw_loss": yaw_loss.item()})
            else:
                act_pred = transformer_policy(frames, obs_history)

            # note: action loss is never used. blows up according to Alan.
            action_loss = (teacher_actions - act_pred).norm(p=2, dim=1).mean()

            logger.store_metrics({"eval/action_loss": action_loss.item()})


def main(_deps=None, **deps):
    from ml_logger import logger
    from lucidsim_experiments import RUN

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
          yDomain: [0, 4.5]
        - yKeys: ["train/yaw_loss/mean", "eval/yaw_loss/mean"]
          xKey: epoch
          yDomain: [0, 4.5]
        - yKey: "lr"
          xKey: epoch
          yDomain: [-0.00002, 0.001]
        """, dedent=True, filename=".charts.yml", overwrite=True)
    # fmt: on

    logger.print("Loading data...")
    train_loader, val_loader = fetch_dreams()
    logger.print("Loading model...")

    logger.upload_file(__file__)
    logger.upload_file(f"{Path(__file__).parent / 'go1_model/transformers/transformer_policy.py'}")

    PolicyArgs.use_camera = False
    teacher_model = ParkourActor()
    teacher_model.to(TrainCfg.device)

    teacher_model.load(TrainCfg.teacher_checkpoint)
    teacher_model.to(TrainCfg.device)
    teacher_model.eval()

    transformer_policy = TransformerPolicy(
        obs_dim=53,
        img_dim=TrainCfg.logical_img_dim,
        act_dim=12,
        img_latent_dim=TrainCfg.image_latent_dim,
        head_dim=TrainCfg.head_dim,
        batchnorm=TrainCfg.use_batchnorm,
        num_layers=TrainCfg.num_layers,
        dropout=TrainCfg.dropout,
        causal=False,
    )
    transformer_policy.to(TrainCfg.device)

    if TrainCfg.student_checkpoint is not None:
        stated = logger.torch_load(TrainCfg.student_checkpoint)
        transformer_policy.load_state_dict(stated)

    logger.print("the model has been loaded!")

    if TrainCfg.optimizer == "adam":
        optimizer = torch.optim.Adam(
            transformer_policy.parameters(),
            TrainCfg.lr,
            weight_decay=TrainCfg.weight_decay,
        )
    elif TrainCfg.optimizer == "sgd":
        optimizer = torch.optim.SGD(
            transformer_policy.parameters(),
            TrainCfg.lr,
            momentum=TrainCfg.momentum,
            weight_decay=TrainCfg.weight_decay,
        )
    else:
        raise NotImplementedError

    if TrainCfg.lr_schedule:
        schedule = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=TrainCfg.n_epochs)

    logger.start("epoch")

    for epoch in range(0, TrainCfg.n_epochs + 1):
        if TrainCfg.lr_schedule:
            schedule.step(epoch)

        if TrainCfg.checkpoint_interval and epoch % TrainCfg.checkpoint_interval == 0:
            logger.print("Saving checkpoints...")
            stated = transformer_policy.state_dict()
            logger.torch_save(stated, f"checkpoints/net_{epoch}.pt")
            logger.duplicate(f"checkpoints/net_{epoch}.pt", "checkpoints/net_last.pt")

        train(train_loader, transformer_policy, optimizer, teacher_model)
        if val_loader:
            evaluate(val_loader, transformer_policy, teacher_model)

        logger.log_metrics_summary(key_values={"epoch": epoch, "dt_epoch": logger.split("epoch")})


if __name__ == "__main__":
    main()
