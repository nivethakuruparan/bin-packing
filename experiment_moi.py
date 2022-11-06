from macpacking.algorithms.online import NextFit, FirstFit, BestFit, WorstFit, OneFit
from macpacking.algorithms.offline import NextFit as NextFitDesc, FirstFit as FirstFitDec, BestFit as BestFitDec, WorstFit as WorstFitDec
from macpacking.algorithms.baseline import BenMaier
from macpacking.reader import BinppReader, JburkardtReader
from os import listdir
from os.path import isfile, join, basename
import matplotlib.pyplot as matplot
import numpy 
import csv

CASES = './_datasets/binpp-hard'
data_path = './_datasets/oracle_binpp-hard.csv'
res_path = 'experiment_res.csv'

def list_case_files(dir:str) -> list[str]:
    return sorted([f'{dir}/{f}' for f in listdir(dir) if isfile(join(dir,f))])

def generate_online_alg_list():
    algs = [NextFit, FirstFit, BestFit, WorstFit, OneFit]
    return algs

def generate_offline_alg_list():
    algs = [NextFitDesc, FirstFitDec, BestFitDec, WorstFitDec]
    return algs 

def extract_optimal_data(path:str):
    data = {}
    with open(path,'r') as file:
        read_ob = csv.reader(file)
        for j in read_ob:
            if(j[0]=='Problem'):continue
            i = str(j)
            key = i.split(',')[0]
            key = key[2:7]+'.BPP.txt'
            value = i.split(',')[1]
            data[key] = []
            data[key].append(['Optimal',int(value[2:4])])
    return data

def execute_algorithm(cases:list[str],algs:list, alg_type:str):
    res = {}
    if alg_type == "Online":
        alg_names = ['NextFit','FirstFit','BestFit','WorstFit','OneFit']
    elif alg_type == "Offline":
        alg_names = ['NextFitOffline','FirstFitDecreasing','BestFitDecreasing','WorstFitDecreasing']
    elif alg_type == "Benchmark":
        alg_names = ['Benchmark']
    for case in cases:
        name = basename(case)
        res[name] = []
        for k in range(len(algs)):
            j = algs[k]
            if alg_type == "Online":
                data = BinppReader(case).online()
            elif alg_type == "Offline":
                data = BinppReader(case).offline()
            elif alg_type == "Benchmark":
                data = BinppReader(case).offline()
            nob = len(j._process(j,data[0],data[1]))
            res[name].append([alg_names[k],nob])
    return res

def execute_bm_algorithm(cases:list[str], alg):
    alg_name = 'Benchmark'
    res = {}
    for case in cases:
        name = basename(case)
        res[name] = []
        data = BinppReader(case).offline()
        nob = len(alg._process(alg,data[0],data[1]))
        res[name].append([alg_name,nob])
    return res

def execute_online_algorithm(cases:list[str],algs:list):
    res = {}
    alg_names = ['NextFit','FirstFit','BestFit','WorstFit','OneFit']
    for case in cases:
        name = basename(case)
        res[name] = []
        for k in range(len(algs)):
            j = algs[k]
            data = BinppReader(case).online()
            nob = len(j._process(j,data[0],data[1]))
            res[name].append([alg_names[k],nob])
    return res


def execute_offline_algorithm(cases:list[str], algs:list):
    res = {}
    alg_names = ['NextFitOffline','FirstFitDecreasing','BestFitDecreasing','WorstFitDecreasing']
    for case in cases:
        name = basename(case)
        res[name] = []
        for k in range(len(algs)):
            j = algs[k]
            data = BinppReader(case).offline()
            nob = len(j._process(j,data[0],data[1]))
            res[name].append([alg_names[k],nob])
    return res



def merge_results(res0,res1,res2,res3):
    res = {}
    res['Algorithm'] = ['Optimal','NextFit','FirstFit','BestFit','WorstFit','OneFit','NextFitOffline','FirstFitDecreasing','BestFitDecreasing','WorstFitDecreasing','Benchmark']
    keys = res1.keys()
    for k in keys:
        res[k] = []
        for i in res0[k]:
            res[k].append(i[1])
        for i in res1[k]:
            res[k].append(i[1])
        for i in res2[k]:
            res[k].append(i[1])
        for i in res3[k]:
            res[k].append(i[1])
    return res

def save_results(path:str,res):
    with open(path,'w') as f:
        writer = csv.writer(f)
        writer.writerow((res.keys()))
        for i in res:
            writer.writerow(res[i])

def plot_moi(moi):
    algs = ['Optimal','NextFit','FirstFit','BestFit','WorstFit','OneFit','NextFitOffline','FirstFitDecreasing','BestFitDecreasing','WorstFitDecreasing','Benchmark']
    for i in moi:
        sheet = matplot.figure()
        bar_graph = sheet.add_axes([0,0,1,1])
        bar_graph.bar(algs,moi[i])
        bar_graph.set_ylabel('Number of Bins More Than Optimal')
        bar_graph.set_xlabel('Algorithm Used')
        bar_graph.set_title(i)
        sheet.set_size_inches(18,5)
        matplot.show()

def compute_moi(res):
    moi = {}
    for case in res.keys():
        if (case == 'Algorithm'):continue
        optimal = res[case][0]
        moi[case] = []
        for i in res[case]:
            margin = i - optimal
            moi[case].append(margin)
    plot_moi(moi)      

def main():
    cases = list_case_files(CASES)

    online_algs = generate_online_alg_list()
    offline_algs = generate_offline_alg_list()
    baseline_alg = [BenMaier]

    res0 = extract_optimal_data(data_path)
    res1 = execute_algorithm(cases, online_algs, "Online")
    res2 = execute_algorithm(cases, offline_algs, "Offline")
    res3 = execute_algorithm(cases, baseline_alg, "Benchmark")
    
    res = merge_results(res0,res1,res2,res3)

    save_results(res_path,res)
    compute_moi(res)

if __name__ == "__main__":
    main()
