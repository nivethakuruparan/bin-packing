from abc import ABC, abstractmethod
from os import path
from random import shuffle, seed
# from tarfile import _Bz2ReadableFileobj
from . import WeightSet, WeightStream


class DatasetReader(ABC):

    def offline(self) -> WeightSet:
        '''Return a WeightSet to support an offline algorithm'''
        (capacity, weights) = self._load_data_from_disk()
        seed(42)          # always produce the same shuffled result
        shuffle(weights)  # side effect shuffling
        return (capacity, weights)

    def online(self) -> WeightStream:
        '''Return a WeighStream, to support an online algorithm'''
        (capacity, weights) = self.offline()

        def iterator():  # Wrapping the contents into an iterator
            for w in weights:
                yield w  # yields the current value and moves to the next one

        return (capacity, iterator())

    @abstractmethod
    def _load_data_from_disk(self) -> WeightSet:
        '''Method that read the data from disk, depending on the file format'''
        pass


class BinppReader(DatasetReader):
    '''Read problem description according to the BinPP format'''

    def __init__(self, filename: str) -> None:
        if not path.exists(filename):
            raise ValueError(f'Unkown file [{filename}]')
        self.__filename = filename

    def _load_data_from_disk(self) -> WeightSet:
        with open(self.__filename, 'r') as reader:
            nb_objects: int = int(reader.readline())
            capacity: int = int(reader.readline())
            weights = []
            for _ in range(nb_objects):
                weights.append(int(reader.readline()))
            return (capacity, weights)

class JburReader(DatasetReader):
    '''Read problem description according to the jburkardt format'''
    def __init__(self, filename1:str, filename2: str) -> None:
        if not path.exists(filename1):
            raise ValueError(f'Unknown file [{filename1}]')
        if not path.exists(filename2):
            raise ValueError(f'Unknown file [{filename2}]')
        self._filename1 = filename1
        self._filename2 = filename2

    def _load_data_from_disk(self) -> WeightSet:
        with open(self._filename1, 'r') as reader:
            capacity: int = int(reader.readline())
        
        with open(self._filename2, 'r') as reader:
            weights = []
            while True:
                line = reader.readline()
                if not line:
                    break
                weights.append(int(line))
            
        return (capacity, weights)