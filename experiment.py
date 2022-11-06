import csv


def extract_optimal_data(filename: str):
    data = {}
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        next(csv_reader)
        for row in csv_reader:
            key = row[0] + '.BPP.txt'
            data[key] = int(row[1])
    return data
