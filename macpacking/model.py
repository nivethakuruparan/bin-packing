from abc import ABC, abstractmethod
from typing import Iterator
from . import WeightStream, WeightSet, Solution


class Partition(ABC):
    pass


class Online(Partition):

    def __call__(self, ws: WeightStream):
        capacity, stream = ws
        return self._process(capacity, stream)

    @abstractmethod
    def _process(self, c: int, stream: Iterator[int]) -> Solution:
        pass


class Offline(Partition):

    def __call__(self, ws: WeightSet):
        capacity, weights = ws
        return self._process(capacity, weights)

    @abstractmethod
    def _process(self, c: int, weights: list[int]) -> Solution:
        pass


class Partition(Partition):

    def __call__(self, ws: WeightSet):
        num_bins, weights = ws
        return self._process(num_bins, weights)

    @abstractmethod
    def _process(self, num_bins: int, weights: list[int]) -> Solution:
        pass
