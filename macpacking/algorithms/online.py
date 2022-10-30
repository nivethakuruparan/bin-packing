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

class FirstFit(Online):

    def _process(self, capacity: int, stream: WeightStream) -> Solution:
        solution = [[]]
        bin_index = 0
        n = 0
        for w in stream:
            n += 1
        remaining = [0] * n
        for w in stream:
            i = 0
            while (i < bin_index):
                if (remaining[i] >= w):
                    solution[i].append(w)
                    remaining[i] = remaining[i] - w
                    break
                i += 1
            if(i == bin_index):
                remaining[bin_index] = capacity - w
                solution.append([w])
                bin_index += 1
        return solution 

class BestFit(Online):

    def _process(self, capacity:int, stream: WeightStream) -> Solution:
        solution = [[]]
        bin_index = 0
        n = 0
        for w in stream:
            n += 1
        remaining = [0] * n
        for w in stream:
            i = 0
            min = capacity + 1
            best_index = 0
            for i in range(bin_index):
                if(remaining[i] >= w and remaining[i] - w < min):
                    best_index = i
                    min = remaining[i] - w
            if (min == capacity+1):
                remaining[bin_index] = capacity - w
                solution.append([w])
                bin_index += 1
            else:
                remaining[best_index] -= w
                solution[best_index].append(w)
        return solution 

class WorstFit(Online):

    def _process(self, capacity:int, stream: WeightStream) -> Solution:
        solution = [[]]
        bin_index = 0
        n = 0 
        for w in stream:
            n += 1
        remaining = [0] * n
        for w in stream:
            max_space = -1
            worst_index = 0
            for i in range(bin_index):
                if(remaining[i] >= w and remaining[i] - w > max_space):
                    worst_index = i
                    max_space = remaining[i] - w
            if (max_space == -1):
                remaining[bin_index] = capacity - w
                solution.append([w])
                bin_index += 1
            else:
                remaining[worst_index] -= w
                solution[worst_index].append(w)
        return solution

class OneFit(Online):

    def _process(self, capacity:int, stream: WeightStream) -> Solution:
        bin_index = 0
        solution = []
        remaining = capacity
        for w in stream:
            solution.append([w])
        return solution 
