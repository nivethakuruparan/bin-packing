from .. import Solution
from ..model import Partition
import binpacking as bp


class BenMaier(Partition):

    def _process(self, num_bins: int, weights: list[int]) -> Solution:
        return bp.to_constant_bin_number(weights, num_bins)
