#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os 
import sys 
import numpy as np
import networkx as nx
import random
from gensim.models import Word2Vec
import subprocess 
from log_manager.log_config import Logger 

from node2vec.Node2VecWalk import Node2VecWalk
from word2vec.WordDoc2Vec import WordDoc2Vec


class Node2Vec: 

	def __init__(self, *args, **kwargs):
		"""
		"""
		self.dimension = kwargs['dimension'] 
		self.window_size = kwargs['window_size']
		self.num_walks = kwargs['num_walks']
		self.walk_length = kwargs['walk_length']
		self.dataDir = os.environ['TRTESTFOLDER']
		self.p = kwargs['p']
		self.q = kwargs['q']

	def learnEmbeddings(self, walkInput, initFromFile, initFile, outputfile, retrofit=0, beta=0.0):
		"""
		Learn embeddings by optimizing the Skipgram 
		objective using SGD. [GENSIM]
		"""
		
		wordDoc2Vec = WordDoc2Vec()
		wPDict = wordDoc2Vec.buildWordDoc2VecParamDict()
		wPDict["cbow"] = str(0) 
		wPDict["sentence-vectors"] = str(0)
		wPDict["min-count"] = str(0)
		wPDict["train"] = walkInput
		wPDict["output"] = outputfile
		wPDict["size"]= str(self.dimension)

		args = []
		if initFromFile==True:
			wPDict["init"] = initFile
			if retrofit ==1:
				wPDict["beta"] = str(beta)
			args = wordDoc2Vec.buildArgListforW2VWithInit(wPDict, retrofit)
		else:
			args = wordDoc2Vec.buildArgListforW2V(wPDict, retrofit)

		Logger.logr.info(args)
		process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		out, err = process.communicate()
		if 	process.returncode != 0: 
			Logger.logr.error("Process haven't terminated successfully")
			sys.exit(1)
		print (out)
		print (err)

	def getWalkFile(self, nx_G, walkInputFileName, precalc=False):
		"""
		Pipeline for representational learning for all nodes in a graph.
		"""
		n2vWalk= Node2VecWalk(nx_G, False, self.p, self.q)
		Logger.logr.info("Simulating Walks")
		

		walkInput = open(walkInputFileName, "w")
		for walk in n2vWalk.simulate_walks(self.num_walks, self.walk_length, precalc):
			Logger.logr.info(walk)
			walkInput.write("%s%s"%(" ".join(list(map(str,walk))),os.linesep)) 

		walkInput.flush()
		walkInput.close()

		return 

		