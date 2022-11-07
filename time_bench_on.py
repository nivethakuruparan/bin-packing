from time_bench import BenchmarkSpace, run_benchmark
from macpacking.algorithms.online import NextFit, FirstFit, BestFit, \
    WorstFit, OneFit


def main():
    algorithms = [NextFit(), FirstFit(), BestFit(), WorstFit(), OneFit()]
    num_weights = [50, 100, 200, 500]
    capacity = [100, 120, 150]

    algo_space = BenchmarkSpace(algorithms, num_weights, capacity, "Online")
    run_benchmark(algo_space)


if __name__ == "__main__":
    main()
