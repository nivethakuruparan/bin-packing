from .. import Solution, WeightSet
from ..model import Offline
from .online import NextFit as Nf_online
from .online import FirstFit as Ff_online 
from .online import BestFit as Bf_online
from .online import WorstFit as Wf_online


class NextFit(Offline):

    def _process(self, capacity: int, weights: WeightSet) -> Solution:
        '''An offline version of NextFit, ordering the weigh stream and
        delegating to the online version (avoiding code duplication)'''
        weights = sorted(weights, reverse=True)
        delegation = Nf_online()
        return delegation((capacity, weights))

class FirstFitDec(Offline):

    def _process(self, capacity: int, weights: WeightSet) -> Solution:
        weights = sorted(weights, reverse=True)
        delegation = Ff_online() 
        return delegation((capacity, weights))

class BestFitDec(Offline):

    def _process(self, capacity:int, weights: WeightSet) -> Solution:
        weights = sorted(weights, reverse = True)
        delegation = Bf_online()
        return delegation((capacity, weights))

class WorstFitDec(Offline):

    def _process(self, capacity: int, weights: WeightSet) -> Solution:
        weights = sorted(weights, reverse = True)
        delegation = Wf_online()
        return delegation((capacity, weights))