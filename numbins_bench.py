from os import listdir
from os.path import isfile, join, basename
from macpacking.algorithms.online import NextFit, FirstFit, RefinedFirstFit, BestFit, WorstFit, OneFit
from macpacking.algorithms.offline import NextFit as NextFitDesc, FirstFit as FirstFitDesc, RefinedFirstFit as RFDesc, BestFit as BestFitDesc, WorstFit as WorstFitDesc
from macpacking.reader import BinppReader
import matplotlib.pyplot as matplot

CASES = './_datasets/binpp/N4C2W2'


def main():
    cases = list_case_files(CASES)
    online_algs = generate_online_alg_list()
    offline_algs = generate_offline_alg_list()
    run_bench(cases, online_algs, "Online")
    run_bench(cases, offline_algs, "Offline")


def list_case_files(dir: str) -> list[str]:
    return sorted([f'{dir}/{f}' for f in listdir(dir) if isfile(join(dir, f))])


def generate_online_alg_list():
    return [NextFit, FirstFit, RefinedFirstFit, BestFit, WorstFit, OneFit]


def generate_offline_alg_list():
    return [NextFitDesc, FirstFitDesc, RFDesc, BestFitDesc, WorstFitDesc]


def run_bench(cases: list[str], algs: list, alg_type: str):
    if alg_type == "Online":
        print("Benchmarking for Online Algorithms:")
    elif alg_type == "Offline":
        print("Benchmarking for Offline Algorithms:")

    alg_names = []
    if alg_type == "Online":
        alg_names = ['NextFit', 'FirstFit', 'RefinedFirstFit', 'BestFit', 'WorstFit', 'OneFit']
    elif alg_type == "Offline":
        alg_names = ['NextFitOffline', 'FirstFitDecreasing', 'RefinedFirstFitDecreasing', 'BestFitDecreasing', 'WorstFitDecreasing']

    for case in cases:
        result = []
        for alg in algs:
            name = basename(case)
            if alg_type == "Online":
                data = BinppReader(case).online()
            elif alg_type == "Offline":
                data = BinppReader(case).offline()
            delegation = alg()
            num_bins = len(delegation((data[0],data[1])))
            # num_bins = len(alg._process(alg, data[0], data[1]))
            result.append(num_bins)
        plot_results(name, alg_names, result)


def plot_results(case: str, alg_names: list[str], result: list[int]):
    sheet = matplot.figure()
    bar_graph = sheet.add_axes([0, 0, 1, 1])
    bar_graph.bar(alg_names, result)
    for i in range(len(alg_names)):
        bar_graph.text(i, result[i], result[i])
    bar_graph.set_ylabel('Number of Bins')
    bar_graph.set_xlabel('Algorithm Name')
    bar_graph.set_title(case)
    sheet.set_size_inches(18,5)
    matplot.show()


if __name__ == "__main__":
    main()
