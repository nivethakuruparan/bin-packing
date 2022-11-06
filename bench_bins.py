from os import listdir
from os.path import isfile, join, basename 
from macpacking.reader import BinppReader, JburReader
from macpacking.algorithms.online import NextFit, FirstFit, BestFit, WorstFit, OneFit
from macpacking.algorithms.offline import NextFit as nf, FirstFitDec, BestFitDec, WorstFitDec
import matplotlib.pyplot as matplot
import numpy 

CASES = './_datasets/binpp/N4C2W2'
    
def list_case_files(dir: str) -> list[str]:
    return sorted([f'{dir}/{f}' for f in listdir(dir) if isfile(join(dir,f))])

def generate_online_alg_list():
    algs = [NextFit, FirstFit, BestFit, WorstFit, OneFit]
    return algs

def generate_offline_alg_list():
    algs = [nf, FirstFitDec, BestFitDec, WorstFitDec]
    return algs 

def plot_results(case: str ,alg_names : list[str], res: list[int]):
    sheet = matplot.figure()
    bar_graph = sheet.add_axes([0,0,1,1])
    bar_graph.bar(alg_names, res)
    bar_graph.set_ylabel('Number of Bins Used')
    bar_graph.set_xlabel('Algorithm Used')
    bar_graph.set_title(case)
    matplot.show()


def run_online_bench(cases:list[str],algs: list):
    res = []
    # alg_names = [] 
    # for i in algs:
    #     alg_names.append(str(i)[37:44])
    alg_names = ['NextFit','FirstFit','BestFit','WorstFit','OneFit']
    for i in cases:
        res = []
        for j in algs:
            name = basename(i)
            # data = BinppReader(i).offline()
            data = BinppReader(i).online()
            nob = len(j._process(j, data[0], data[1]))
            res.append(nob)
        plot_results(name, alg_names, res)

def run_offline_bench(cases: list[str], algs: list):
    res = []
    # alg_names = [] 
    # for i in algs:
    #     alg_names.append(str(i)[37:44])
    alg_names = ['NextFitOffline','FirstFitDecreasing','BestFitDecreasing','WorstFitDecreasing']
    for i in cases:
        res = []
        for j in algs:
            name = basename(i)
            # data = BinppReader(i).online()
            data = BinppReader(i).offline()
            nob = len(j._process(j, data[0], data[1]))
            res.append(nob)
        plot_results(name, alg_names, res)
    

def main():
    cases = list_case_files(CASES)
    algs = generate_online_alg_list()
    run_online_bench(cases, algs)
    algs = generate_offline_alg_list()
    run_offline_bench(cases, algs)

if __name__ == "__main__":
    main()






