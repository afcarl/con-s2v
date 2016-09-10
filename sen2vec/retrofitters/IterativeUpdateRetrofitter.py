#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os 
import sys 
from log_manager.log_config import Logger 
import networkx as nx 
from copy import deepcopy

class IterativeUpdateRetrofitter:
    def __init__(self, *args, **kwargs):
      self.numIters = kwargs['numIter']
      self.nx_Graph = kwargs['nx_Graph']

    def retrofitWithIterUpdate(self, sen2vec):
      newSen2Vecs = deepcopy(sen2vec)
      allSentenceIds = set(newSen2Vecs.keys())

      for iter_ in range(self.numIters):
        for sentenceId in allSentenceIds:
          sentNeighbors = self.nx_Graph.neighbors(sentenceId)
          numNeighbors = len(sentNeighbors)
          if numNeighbors == 0:
            continue
          newVec = numNeighbors * sen2vec[sentenceId]
          for neighborSentId in sentNeighbors:
            newVec += newSen2Vecs[neighborSentId]

          newSen2Vecs[sentenceId] = newVec/(2*numNeighbors)
      return newSen2Vecs