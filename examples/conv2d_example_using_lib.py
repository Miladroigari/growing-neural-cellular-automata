import torch as t
import torch.nn.functional as F

from examples.conv2d_example import inspect
from lib.conv import conv, kernel


def create_samples_batch():
    # Create a sample with two channels
    channel = t.tensor(list(range(1, 25 + 1))).view((5, 5)).type(t.float)
    sample = t.stack([channel, channel * 2], 0)
    inspect('sample', sample)

    samples_batch = sample[None, :]
    inspect('samples_batch', samples_batch)
    return samples_batch


batch = create_samples_batch()

_filter = conv.single_kernel_filter(kernel.SOLVER_X, in_channels=2)
inspect('filter', _filter)

weights = conv.weights(_filter, out_channels=2)
inspect('weights', weights)

# Apply conv2d to input batch
output = F.conv2d(batch, weights, stride=1, padding=0)

inspect('output', output)
