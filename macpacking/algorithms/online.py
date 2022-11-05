from .. import Solution, WeightStream
from ..model import Online


class NextFit(Online):

    def _process(self, capacity: int, stream: WeightStream) -> Solution:
        bin_index = 0
        solution = [[]]
        remaining = capacity
        for w in stream:
            if remaining >= w:
                solution[bin_index].append(w)
                remaining = remaining - w
            else:
                bin_index += 1
                solution.append([w])
                remaining = capacity - w
        return solution


class OneFit(Online):

    def _process(self, capacity: int, stream: WeightStream) -> Solution:
        solution = []
        for w in stream:
            solution.append([w])
        return solution


class FirstFit(Online):
    """Code Referenced From: https://github.com/erelsgl/prtpy/blob/main/
    prtpy/packing/first_fit.py"""

    def _process(self, capacity: int, stream: WeightStream) -> Solution:
        solution = [[]]
        num_bins = 1
        for w in stream:
            bin_index = 0
            while bin_index < num_bins:
                if sum(solution[bin_index]) + w <= capacity:
                    solution[bin_index].append(w)
                    break
                bin_index += 1
            else:
                solution.append([w])
                num_bins += 1
        return solution


class BestFit(Online):
    """Code Referenced From: https://github.com/erelsgl/prtpy/blob/main/
    prtpy/packing/best_fit.py"""

    def _process(self, capacity: int, stream: WeightStream) -> Solution:
        solution = [[]]
        num_bins = 1
        for w in stream:
            bin_index = 0
            best_bin_info = (-1, -1)  # (bin index, min space left)
            while bin_index < num_bins:
                temp_sum = sum(solution[bin_index]) + w
                if temp_sum <= capacity and temp_sum > best_bin_info[1]:
                    best_bin_info = (bin_index, temp_sum)
                bin_index += 1
            if best_bin_info[0] > -1:
                solution[best_bin_info[0]].append(w)
            else:
                solution.append([w])
                num_bins += 1
        return solution


class WorstFit(Online):

    def _process(self, capacity: int, stream: WeightStream) -> Solution:
        solution = [[]]
        num_bins = 1
        for w in stream:
            bin_index = 0
            worst_bin_info = (-1, -1)  # (bin index, max space left)
            while bin_index < num_bins:
                temp_sum = sum(solution[bin_index]) + w
                max_space = capacity - temp_sum
                if temp_sum <= capacity and max_space > worst_bin_info[1]:
                    worst_bin_info = (bin_index, max_space)
                bin_index += 1
            if worst_bin_info[0] > -1:
                solution[worst_bin_info[0]].append(w)
            else:
                solution.append([w])
                num_bins += 1
        return solution
