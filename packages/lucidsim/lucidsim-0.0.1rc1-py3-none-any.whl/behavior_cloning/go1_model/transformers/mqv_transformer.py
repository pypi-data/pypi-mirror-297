"""
Source: https://github.com/karpathy/nanoGPT/blob/master/model.py
"""

import math
import torch
import torch.nn.functional as F
from torch import nn


class CausalSelfAttention(nn.Module):
    def __init__(
        self,
        d,
        H,
        T,
        bias=False,
        dropout=0.2,
    ):
        """
        Arguments:
        d: size of embedding dimension
        H: number of attention heads
        T: maximum length of input sequences (in tokens)
        bias: whether to use bias in linear layers
        dropout: probability of dropout
        """
        super().__init__()
        assert d % H == 0

        # key, query, value projections for all heads, but in a batch
        # output is d + 2 because we share one pair of k and v (the 2) across all heads.
        self.head_d = d // H
        self.c_attn = nn.Linear(d, d + self.head_d + self.head_d, bias=bias)

        # projection of concatenated attention head outputs
        self.c_proj = nn.Linear(d, d, bias=bias)

        # dropout modules
        self.attn_dropout = nn.Dropout(dropout)
        self.resid_dropout = nn.Dropout(dropout)
        self.H = H
        self.d = d

        # causal mask to ensure that attention is only applied to
        # the left in the input sequence
        self.register_buffer("bias", torch.tril(torch.ones(T, T)).view(1, 1, T, T))

    def forward(self, x):
        B, T, _ = x.size()  # batch size, sequence length, embedding dimensionality

        # compute query, key, and value vectors for all heads in batch
        # split the output into separate query, key, and value tensors
        q, k, v = self.c_attn(x).split([d, self.head_d, self.head_d], dim=2)
        # q, k, v = self.c_attn(x).split(self.d, dim=2)  # [B, T, d]

        # reshape tensor into sequences of smaller token vectors for each head
        q = q.view(B, T, self.H, self.head_d).transpose(1, 2)  # [B, H, T, d // H]
        k = k.view(B, T, 1, self.head_d).transpose(1, 2)
        v = v.view(B, T, 1, self.head_d).transpose(1, 2)

        # compute the attention matrix, perform masking, and apply dropout
        att = (q @ k.transpose(-2, -1)) * (1.0 / math.sqrt(k.size(-1)))  # [B, H, T, T]
        att = att.masked_fill(self.bias[:, :, :T, :T] == 0, float("-inf"))
        att = F.softmax(att, dim=-1)
        att = self.attn_dropout(att)

        # compute output vectors for each TOKEN
        y = att @ v  # [B, H, T, d // H]

        # concatenate outputs from each attention head and linearly project
        y = y.transpose(1, 2).contiguous().view(B, T, self.d)
        y = self.resid_dropout(self.c_proj(y))
        self.c_proj(y).shape
        return y


class MQVTransformer(nn.Sequential):
    def __init__(
        self,
        d,
        num_layers,
        H,
        T,
        bias=False,
        dropout=0.2,
    ):
        """
        Arguments:
        d: size of embedding dimension
        H: number of attention heads
        T: maximum length of input sequences (in tokens)
        bias: whether to use bias in linear layers
        dropout: probability of dropout
        """
        layers = []

        for _ in range(num_layers):
            layers += [
                CausalSelfAttention(d, H, T, bias, dropout),
                nn.Tanh(),
            ]
        super().__init__(*layers)


if __name__ == "__main__":
    B, T, d = 32, 100, 512

    input_t = torch.randn(B, T, d)

    attn = CausalSelfAttention(512, 8, 100)
    print(attn)

    output_t = attn(input_t)
    print(output_t.shape)

    transformer = MQVTransformer(512, 7, 8, 100)
    output_t = transformer(input_t)
    print(output_t.shape)
