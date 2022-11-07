import pyperf
from typing import TypedDict
from os.path import basename
from macpacking.model import Partition
from macpacking.reader import BinppPartitionReader
from macpacking.partitioning_algorithms.baseline import BenMaier
from macpacking.partitioning_algorithms.partition \
    import GreedyNumberPartitioning


class SpaceElement(TypedDict):
    name: str
    data: tuple
    binpacker: Partition


class BenchmarkSpace():
    def __init__(self, strategies, num_weights, num_bins) -> None:
        self.__strategies: list[Partition] = strategies
        self.__num_weights: list[int] = num_weights
        self.__num_bins: list[int] = num_bins

    def finalize(self) -> list[SpaceElement]:
        result = []

        for w in self.__num_weights:
            for n in self.__num_bins:
                case = self.__gen_cases(w, n)
                for strategy in self.__strategies:
                    elem: SpaceElement = {
                        'name': self.__build_name(case, strategy, w, n),
                        'data': BinppPartitionReader(case, n).partition(),
                        'binpacker': strategy
                    }
                    result.append(elem)

        return result

    def __gen_cases(self, num_weights: int, num_bins: int) -> list[str]:
        if num_weights == 50:
            w = '1'
        elif num_weights == 100:
            w = '2'
        elif num_weights == 200:
            w = '3'
        elif num_weights == 500:
            w = '4'

        if num_bins == 10:
            c = '1'
        elif num_bins == 20:
            c = '2'
        elif num_bins == 40:
            c = '3'

        return '_datasets/binpp/N' + w + 'C' + c + 'W1/N' + w + \
            'C' + c + 'W1_A.BPP.txt'

    def __build_name(self, case: str, strategy: Partition, num_weights: int, num_bins: int) -> str:
        return f'{basename(case)}-{strategy.__class__.__name__}-{num_weights}-{num_bins}'


def run_benchmark(space: BenchmarkSpace):
    runner = pyperf.Runner()
    elements: list[SpaceElement] = space.finalize()
    for e in elements:
        runner.bench_func(e['name'], e['binpacker'], e['data'])


def main():
    algorithms = [GreedyNumberPartitioning(), BenMaier()]
    num_weights = [50, 100, 200, 500]
    num_bins = [10, 20, 40]

    algo_space = BenchmarkSpace(algorithms, num_weights, num_bins)
    run_benchmark(algo_space)


if __name__ == "__main__":
    main()
