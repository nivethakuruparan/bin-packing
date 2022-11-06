from macpacking.reader import DatasetReader, BinppReader
from macpacking.model import Online, Offline
import macpacking.algorithms.online as online
import macpacking.algorithms.offline as offline


def test_result_type_online():
    dataset = '_datasets/binpp/N1C1W1/N1C1W1_B.BPP.txt'
    reader: DatasetReader = BinppReader(dataset)

    nf: Online = online.NextFit()
    nf_result = nf(reader.online())

    ff: Online = online.FirstFit()
    ff_result = ff(reader.online())

    bf: Online = online.BestFit()
    bf_result = bf(reader.online())

    wf: Online = online.WorstFit()
    wf_result = wf(reader.online())

    of: Online = online.OneFit()
    of_result = of(reader.online())

    assert type(nf_result) == list
    assert type(ff_result) == list
    assert type(bf_result) == list
    assert type(wf_result) == list
    assert type(of_result) == list


def test_max_sum_online():
    dataset = '_datasets/binpp/N1C1W1/N1C1W1_B.BPP.txt'
    reader: DatasetReader = BinppReader(dataset)
    capacity = 100

    nf: Online = online.NextFit()
    nf_result = nf(reader.online())
    nf_sums = list(map(sum, nf_result))

    ff: Online = online.WorstFit()
    ff_result = ff(reader.online())
    ff_sums = list(map(sum, ff_result))

    bf: Online = online.BestFit()
    bf_result = bf(reader.online())
    bf_sums = list(map(sum, bf_result))

    wf: Online = online.WorstFit()
    wf_result = wf(reader.online())
    wf_sums = list(map(sum, wf_result))

    of: Online = online.OneFit()
    of_result = of(reader.online())
    of_sums = list(map(sum, of_result))

    assert all(i <= capacity for i in nf_sums)
    assert all(i <= capacity for i in ff_sums)
    assert all(i <= capacity for i in bf_sums)
    assert all(i <= capacity for i in wf_sums)
    assert all(i <= capacity for i in of_sums)


def test_result_type_offline():
    dataset = '_datasets/binpp/N1C1W1/N1C1W1_B.BPP.txt'
    reader: DatasetReader = BinppReader(dataset)

    nf: Offline = offline.NextFit()
    nf_result = nf(reader.offline())

    ff: Offline = offline.FirstFit()
    ff_result = ff(reader.offline())

    bf: Offline = offline.BestFit()
    bf_result = bf(reader.offline())

    wf: Offline = offline.WorstFit()
    wf_result = wf(reader.offline())

    assert type(nf_result) == list
    assert type(ff_result) == list
    assert type(bf_result) == list
    assert type(wf_result) == list


def test_max_sum_offline():
    dataset = '_datasets/binpp/N1C1W1/N1C1W1_B.BPP.txt'
    reader: DatasetReader = BinppReader(dataset)
    capacity = 100

    nf: Offline = offline.NextFit()
    nf_result = nf(reader.offline())
    nf_sums = list(map(sum, nf_result))

    ff: Offline = offline.WorstFit()
    ff_result = ff(reader.offline())
    ff_sums = list(map(sum, ff_result))

    bf: Offline = offline.BestFit()
    bf_result = bf(reader.offline())
    bf_sums = list(map(sum, bf_result))

    wf: Offline = offline.WorstFit()
    wf_result = wf(reader.offline())
    wf_sums = list(map(sum, wf_result))

    assert all(i <= capacity for i in nf_sums)
    assert all(i <= capacity for i in ff_sums)
    assert all(i <= capacity for i in bf_sums)
    assert all(i <= capacity for i in wf_sums)
