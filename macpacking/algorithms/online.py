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


class RefinedFirstFit(Online):

    def _first_fit_helper(self, capacity: int, num_bins: int, w: int, solution: Solution):
        bin_index = 0
        while bin_index < num_bins:
            if sum(solution[bin_index]) + w <= capacity:
                solution[bin_index].append(w)
                break
            bin_index += 1
        else:
            solution.append([w])
            num_bins += 1
        return solution, num_bins

    def _determine_category(self, w: int, capacity: int, count_b2: int):
        cap = [0, (1/3 * capacity), (2/5 * capacity), (1/2 * capacity), capacity]
        m = 6
        category = ''
        if (w>cap[3] and w<=cap[4]):
                category = 'L'
        elif (w>cap[2] and w<=cap[3]):
                category = 'M'
        elif (w>cap[1] and w<=cap[2]):
                count_b2 += 1
                if(count_b2 < m):
                    category = 'S'
                else:
                    category = 'L'
        elif (w>0 and w<=cap[1]):
                category = 'XS'
        return category, count_b2

    def _process(self, capacity: int, stream: WeightStream) -> Solution:
        num_bins = {"L": 1, "M": 1, "S": 1, "XS": 1} #each of the keys is a bin category, bins are divided among four categories
        sol = {"L": [[]], "M": [[]], "S": [[]], "XS": [[]]}
        bi = {"L": 0, "M": 0, "S": 0, "XS": 0}
        count_b2 = 0

        for w in stream:
            category,count_b2 = self._determine_category(w,capacity,count_b2)
            sol[category], num_bins[category] = self._first_fit_helper(capacity, num_bins[category],w,sol[category])
            
        solution = sol["L"] + sol["M"] + sol["S"] + sol["XS"]
        return solution 


class BestFit(Online):

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


class OneFit(Online):

    def _process(self, capacity: int, stream: WeightStream) -> Solution:
        solution = []
        for w in stream:
            solution.append([w])
        return solution
