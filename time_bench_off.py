from time_bench import BenchmarkSpace, run_benchmark
from macpacking.algorithms.offline import NextFit, FirstFit, BestFit, WorstFit


def main():
    algorithms = [NextFit(), FirstFit(), BestFit(), WorstFit()]
    num_weights = [50, 100, 200, 500]
    capacity = [100, 120, 150]

    algo_space = BenchmarkSpace(algorithms, num_weights, capacity, "Offline")
    run_benchmark(algo_space)


if __name__ == "__main__":
    main()
