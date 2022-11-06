from .. import Solution, WeightSet
from ..model import Partition


class GreedyNumberPartitioning(Partition):
    """Code Referenced From: https://github.com/erelsgl/prtpy/blob/main/
    prtpy/partitioning/greedy.py"""
    def _process(self, num_bins: int, weights: WeightSet) -> Solution:
        solution = [[] for i in range(num_bins)]
        weights = sorted(weights, reverse=True)

        for w in weights:
            sums = list(map(sum, solution))
            bin_index = min(range(num_bins), key=sums.__getitem__)
            solution[bin_index].append(w)

        return solution
