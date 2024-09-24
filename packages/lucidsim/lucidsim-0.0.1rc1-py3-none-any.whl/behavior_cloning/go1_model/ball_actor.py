import torch
from params_proto import PrefixProto
from torch import nn
from torchtyping import TensorType
from typing import List, Tuple, Union

from behavior_cloning.cifar10.models import MODEL_TYPES, get_model
from behavior_cloning.model import get_soda_model
from cxx.modules import Estimator
from cxx.modules.actor_critic import Actor, get_activation


class Go1RGBConfig(PrefixProto):
    n_proprio = 53
    n_scan = 132
    num_actions = 12
    scan_encoder_dims = [128, 64, 32]
    actor_hidden_dims = [512, 256, 128]
    priv_encoder_dims = [64, 20]
    estimator_hidden_dims = [128, 64]
    n_priv_latent = 29
    n_priv = 9
    history_len = 10
    depth_buffer_len = 3
    activation_fn = "elu"
    tanh_encoder_output = False


def get_rgb_ball_actor_5():
    vision_head = get_soda_model(
        inp_shape=(3 * 5, 45, 80),
        num_filters=64,
        projection_dim=32,
        num_shared_layers=10,
        coord_conv=False,
    )

    model = BallRGBActor(
        **vars(Go1RGBConfig),
        vision_head=vision_head,
        freeze_teacher_modules=False,
    )

    return model


class BallRGBActor(nn.Module):
    def __init__(
        self,
        n_proprio: int,
        n_scan: int,
        num_actions: int,
        scan_encoder_dims: List[int],
        actor_hidden_dims: List[int],
        priv_encoder_dims: List[int],
        estimator_hidden_dims: List[int],
        n_priv_latent: int,
        n_priv: int,
        history_len: int,
        activation_fn: str,
        tanh_encoder_output,
        vision_head: MODEL_TYPES,
        freeze_teacher_modules: bool,
        **kwargs,
    ):
        super().__init__()

        self.n_proprio = n_proprio
        self.n_scan = n_scan
        self.num_actions = num_actions
        self.n_priv = n_priv

        self.freeze_teacher_modules = freeze_teacher_modules

        self.vision_latent_dim = scan_encoder_dims[-1]

        activation_fn = get_activation(activation_fn)

        self.actor = Actor(
            n_proprio=n_proprio,
            n_scan=n_scan,
            num_actions=num_actions,
            scan_encoder_dims=scan_encoder_dims,
            actor_hidden_dims=actor_hidden_dims,
            priv_encoder_dims=priv_encoder_dims,
            n_priv_latent=n_priv_latent,
            n_priv=n_priv,
            history_len=history_len,
            activation_fn=activation_fn,
            tanh_encoder_output=tanh_encoder_output,
        )

        self.estimator = Estimator(input_dim=n_proprio, output_dim=n_priv, hidden_dims=estimator_hidden_dims)  # .to(self.device)

        if isinstance(vision_head, str):
            self.vision_head = get_model(vision_head)  # , device=self.device)
        else:
            self.vision_head = vision_head

        # self.combination_mlp = nn.Sequential(
        #     nn.Linear(32 + n_proprio, 128),
        #     activation_fn,
        #     nn.Linear(128, 32 + 1)
        # )

        self.combination_mlp = nn.Sequential(nn.Linear(32, 128), activation_fn, nn.Linear(128, 32 + 1))

    def _parse_ac_params(self, params):
        actor_params = {}
        for k, v in params.items():
            if k.startswith("actor."):
                actor_params[k[6:]] = v
        return actor_params

    def load_teacher_modules(self, logger_prefix: str, device: str):
        from ml_logger import logger

        state_dict = logger.torch_load(logger_prefix, map_location=device)
        model_dict = self._parse_ac_params(state_dict["model_state_dict"])

        self.actor.load_state_dict(model_dict)
        self.estimator.load_state_dict(state_dict["estimator_state_dict"])

        if self.freeze_teacher_modules:
            for param in self.estimator.parameters():
                param.requires_grad = False
            for param in self.actor.parameters():
                param.requires_grad = False

    def forward(
        self,
        ego: Union[TensorType["batch", "num_channels", "height", "width"], None],
        obs: TensorType["batch", "num_observations"],
        vision_latent: Union[TensorType["batch", "self.vision_latent_dim"], None] = None,
        hist_encoding: bool = True,
        **_,
    ) -> Tuple[TensorType["batch", 12], TensorType["batch", "depth_latent_dim"]]:
        # assert camera is not None or vision_latent is not None, "Either camera or vision_latent must be provided"

        # mask out the yaw observation
        # print('yo')
        obs_prop = obs[:, : self.n_proprio].clone()
        if ego is not None:
            # run inference with the vision head. If no image is provided, then we reuse the previous latent.
            vision_latent = self.vision_head(ego)  # , obs[:, :self.n_proprio])
        elif vision_latent is None:
            raise ValueError("Either camera or vision_latent must be provided")
            # vision_latent = self.last_latent

        # mask out the yaw observation
        obs_prop[:, 6:8] = 0
        # vision_latent_and_yaw = self.combination_mlp(torch.cat((vision_latent, obs_prop), dim=-1))
        vision_latent_and_yaw = self.combination_mlp(vision_latent)
        vision_latent = vision_latent_and_yaw[:, :-1]
        yaw = 1.5 * vision_latent_and_yaw[:, -1:]

        obs_prop[:, 6:8] = yaw
        # print("Yaw: ", yaw)

        priv_states_estimated = self.estimator(obs_prop.float())
        start_idx = self.n_proprio + self.n_scan
        end_idx = self.n_proprio + self.n_scan + self.n_priv
        obs_prop_scan = torch.cat([obs_prop, obs[:, self.n_proprio : start_idx]], dim=-1)
        tail = obs[:, end_idx:]
        estimated_obs = torch.cat([obs_prop_scan, priv_states_estimated, tail], dim=1)

        actions = self.actor(estimated_obs, hist_encoding=hist_encoding, scandots_latent=vision_latent)

        return actions, vision_latent, yaw
