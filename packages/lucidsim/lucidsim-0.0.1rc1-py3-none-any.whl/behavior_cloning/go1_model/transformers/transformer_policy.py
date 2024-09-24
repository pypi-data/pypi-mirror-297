import torch
import torch.nn as nn
import warnings
from einops import rearrange
from params_proto import ParamsProto
from typing import Mapping, Any

from behavior_cloning.go1_model.transformers.parallem_transformer import PalmTransformer


class TransformerPolicyArgs(ParamsProto, prefix="transformer_policy", cli=False):
    obs_dim = 53
    img_dim = 3
    act_dim = 12
    head_dim = 128
    num_layers = 5
    dropout = 0.1
    img_latent_dim = 64


class DepthTransformerPolicyArgs(ParamsProto, prefix="depth_transformer_policy", cli=False):
    obs_dim = 53
    img_dim = 1
    act_dim = 12
    head_dim = 128
    num_layers = 5
    dropout = 0.1
    img_latent_dim = 64


def get_depth_transformer_policy():
    return TransformerPolicy(
        **vars(DepthTransformerPolicyArgs),
    )


def get_depth_transformer_policy_yaw():
    return TransformerPolicy(
        **vars(DepthTransformerPolicyArgs),
        pred_yaw=True,
    )


def get_rgb_transformer_policy_batchnorm():
    return TransformerPolicy(
        **vars(TransformerPolicyArgs),
        batchnorm=True,
    )


def get_rgb_transformer_policy():
    return TransformerPolicy(
        **vars(TransformerPolicyArgs),
    )


def get_rgb_transformer_policy_yaw():
    return TransformerPolicy(
        **vars(TransformerPolicyArgs),
        pred_yaw=True,
    )


class TransformerPolicy(nn.Module):
    def __init__(
        self,
        obs_dim,
        img_dim,
        act_dim,
        img_latent_dim,
        head_dim,
        num_layers,
        num_heads=8,
        num_steps=300,
        dropout=0.1,
        causal=False,
        pred_yaw=False,
        batchnorm=False,
    ):
        super().__init__()
        self.transformer = PalmTransformer(
            head_dim,
            num_layers,
            heads=num_heads,
            attn_dropout=dropout,
            ff_dropout=dropout,
            causal=causal,
        )

        # self.rotary_emb
        # self.q_scale
        # self.k_scale
        # self.act_prof
        self.head_d = head_dim

        # Encoders: time, obs, image.
        self.steps = num_steps
        # 20ms per step, 50 per second, 300 per 3 seconds
        # self.ts_enc = nn.Embedding(num_steps, 64)
        # self.ts_latent = self.ts_enc(torch.arange(num_steps))

        self.obs_enc = nn.Conv1d(obs_dim, head_dim, 1)

        self.img_dim = img_dim

        img_pipe = []
        if batchnorm:
            img_pipe.append(nn.BatchNorm2d(img_dim))
        img_pipe.extend(
            [
                nn.Conv2d(img_dim, 64, 8, 8),
                nn.ReLU(),
                nn.Conv2d(64, head_dim, 2, 1),
            ]
        )

        self.img_enc = nn.Sequential(
            *img_pipe,
        )

        # We use a special set of action tokens. Channel first.
        self.act_tokens = nn.Parameter(torch.randn(1, num_steps, head_dim))

        self.pred_yaw = pred_yaw

        # just one action output right now.
        self.act_proj = nn.Sequential(
            nn.Linear(head_dim, act_dim),
            # nn.Tanh(),
        )

        self.yaw_proj = nn.Sequential(
            nn.Linear(head_dim, 64),
            nn.ReLU(),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Linear(32, 16),
            nn.ReLU(),
            nn.Linear(16, 2),
            nn.Tanh(),
        )

        # self.yaw_proj = nn.Sequential(
        #     nn.Linear(head_dim, 2),
        # )

    def forward_yaw(self, frames, obs, **extras):
        """
        dagger_mode: if True, use mixed teacher student supervision -- obs will always contain gt yaw
        """
        B, T, C, H, W = frames.shape

        frames_flattened = rearrange(frames, "b t c h w -> (b t) c h w")
        image_tokens = self.img_enc(frames_flattened).reshape(B, T, self.head_d, -1)  # B, T, head_d, 2x6
        image_tokens_sequence_first = rearrange(image_tokens, "b t c f -> b (t f) c")
        pred_yaw = self.yaw_proj(image_tokens_sequence_first[:, -1]) / 1.5

        obs = obs.clone()

        # # mask out and replace yaw observation
        obs[:, :, 6:8] = 0
        obs[:, -1, 6:8] = pred_yaw

        obs_channel_first = rearrange(obs, "b t c -> b c t")
        obs_tokens = self.obs_enc(obs_channel_first).transpose(1, 2)

        act_input_tokens = self.act_tokens[:, 0].repeat(B, 1, 1)

        all_tokens = torch.cat([obs_tokens, image_tokens_sequence_first, act_input_tokens], dim=1)

        output = self.transformer(all_tokens)

        act = self.act_proj(output[:, -1])

        return act, pred_yaw

    def forward(self, frames, obs, **extras):
        if self.pred_yaw:
            return self.forward_yaw(frames, obs, **extras)

        B, img_T, C, H, W = frames.shape

        frames = frames[:, :, : self.img_dim, :, :]

        # print(frames.mean())

        # if timesteps is None:
        #     ts_latents = self.ts_latent[:T]
        # else:
        #     ts_latents = self.ts_enc(timesteps)

        obs_channel_first = rearrange(obs, "b t c -> b c t")

        obs_tokens = self.obs_enc(obs_channel_first).transpose(1, 2)

        frames_flattened = rearrange(frames, "b t c h w -> (b t) c h w")
        image_tokens = self.img_enc(frames_flattened).reshape(B, img_T, self.head_d, -1)  # B, T, head_d, 2x6
        image_tokens_sequence_first = rearrange(image_tokens, "b t c f -> b (t f) c")

        # we only predict one action right now, but we can predict a lot more.
        act_input_tokens = self.act_tokens[:, 0].repeat(B, 1, 1)

        all_tokens = torch.cat([obs_tokens, image_tokens_sequence_first, act_input_tokens], dim=1)

        output = self.transformer(all_tokens)

        act = self.act_proj(output[:, -1])

        return act

    def load_state_dict(self, state_dict: Mapping[str, Any], strict: bool = True, assign: bool = False):
        # Hack to avoid issues with loading yaw projection
        try:
            super().load_state_dict(state_dict, strict=strict)
        except RuntimeError:
            # find all keys with 'yaw' in them
            yaw_keys = [k for k in state_dict.keys() if "yaw" in k]
            for k in yaw_keys:
                state_dict.pop(k)
            super().load_state_dict(state_dict, strict=False)

            warnings.warn(
                "Had to pop out the yaw keys. If these were needed, you will deal with the consequences of your actions later",
            )


if __name__ == "__main__":
    B, T, d = 32, 100, 512

    input_t = torch.randn(B, T, d)

    obs = torch.randn(B, 11, 53)
    teacher_act = torch.randn(B, 11, 12)
    frames = torch.randn(B, 11, 10, 64, 64)

    policy = TransformerPolicy(53, 12, 64, 7, 8, 10)

    output_t = policy(obs, frames)
    assert output_t.shape == (B, 11, 12)

    print(output_t)
