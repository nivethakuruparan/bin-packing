import pyperf
from typing import TypedDict
from os.path import basename
from macpacking.model import BinPacker
from macpacking.reader import BinppReader


class SpaceElement(TypedDict):
    name: str
    data: tuple
    binpacker: BinPacker


class BenchmarkSpace():
    def __init__(self, strategies, num_weights, capacity, alg_type) -> None:
        self.__strategies: list[BinPacker] = strategies
        self.__num_weights: list[int] = num_weights
        self.__capacity: list[int] = capacity
        self.__algorithm_type: str = alg_type

    def finalize(self) -> list[SpaceElement]:
        result = []

        for w in self.__num_weights:
            for c in self.__capacity:
                case = self.__gen_cases(w, c)
                for strategy in self.__strategies:
                    if self.__algorithm_type == "Online":
                        elem: SpaceElement = {
                            'name': self.__build_name(case, strategy, w, c),
                            'data': BinppReader(case).online(),
                            'binpacker': strategy
                        }
                    elif self.__algorithm_type == "Offline":
                        elem: SpaceElement = {
                            'name': self.__build_name(case, strategy, w, c),
                            'data': BinppReader(case).offline(),
                            'binpacker': strategy
                        }
                    result.append(elem)

        return result

    def __gen_cases(self, num_weights: int, capacity: int) -> list[str]:
        if num_weights == 50:
            w = '1'
        elif num_weights == 100:
            w = '2'
        elif num_weights == 200:
            w = '3'
        elif num_weights == 500:
            w = '4'

        if capacity == 100:
            c = '1'
        elif capacity == 120:
            c = '2'
        elif capacity == 150:
            c = '3'

        return '_datasets/binpp/N' + w + 'C' + c + 'W1/N' + w + \
            'C' + c + 'W1_A.BPP.txt'

    def __build_name(self, case: str, strategy: BinPacker, num_weights: int, capacity: int) -> str:
        return f'{basename(case)}-{strategy.__class__.__name__}-{num_weights}-{capacity}'


def run_benchmark(space: BenchmarkSpace):
    runner = pyperf.Runner()
    elements: list[SpaceElement] = space.finalize()
    for e in elements:
        runner.bench_func(e['name'], e['binpacker'], e['data'])
