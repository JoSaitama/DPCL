"""A 64-input, 64-hidden, 10-logit MLP for native Digits pixels."""

from flax import linen as nn
import jax.numpy as jnp


class DigitsMLP(nn.Module):
    num_classes: int = 10
    dtype: object = jnp.float32

    @nn.compact
    def __call__(self, x, train=True):
        x = x.reshape((x.shape[0], 64))
        x = nn.relu(nn.Dense(64, dtype=self.dtype)(x))
        return nn.Dense(self.num_classes, dtype=self.dtype)(x)
