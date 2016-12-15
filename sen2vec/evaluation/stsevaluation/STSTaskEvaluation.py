#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os 
import sys 
import math
import numpy as np
import pandas as pd
import scipy.stats 
import sklearn.metrics as mt
from sklearn import linear_model
from abc import ABCMeta, abstractmethod
from log_manager.log_config import Logger
from sklearn.dummy import DummyClassifier



class STSTaskEvaluation:
	"""
	Semantic Textual Similarity Task Evaluation Base
	"""
	__metaclass__ = ABCMeta

	def __init__(self):
		self.dataFolder = os.environ['TRTESTFOLDER']
		self.postgresConnection = kwargs['postgres_connection']
		self.rootdir = os.environ['SEN2VEC_DIR']
		self.original_val = list ()
		self.computed_val = list ()

	def computeAndWriteResults(self, latReprName):
		sp = scipy.stats.spearmanr(original_val,computed_val)[0]
		pearson = scipy.stats.pearsonr(original_val,computed_val)[0]

		evaluationResultFile = open("%s/%sstseval.txt"%(self.dataFolder,\
				latReprName), "w")
		evaluationResultFile.write("spearman corr:%.4f%s"%(sp, os.linesep))
		evaluationResultFile.write("pearsonn corr:%.4f%s"%(pearson, os.linesep))

	def runValidation(self, vDict, latReprName):
		Logger.logr.info ("[%s] Running Validation for STS Task"%())
		validation_pair_file = open(os.path.join(self.rootdir,\
				"Data/validation_pair_%s.p"%(os.environ['DATASET'])), "rb")
		val_dict = pickle.load(validation_pair_file)

		for k, val in val_dict.items():
			self.original_val.append(val)
			self.computed_val.append(np.inner(vDict[(k[0])],vDict[(k[1])]))

		self.computeAndWriteResults (latReprName)

	def runSTSTest(self, vDict, latReprName):
		
		test_pair_file = open(os.path.join(self.rootdir,\
				"Data/test_pair_%s.p"%(os.environ['DATASET'])), "rb")
		test_dict = pickle.load(test_pair_file)

		
		for k, val in test_dict.items():
			self.original_val.append(val)
			self.computed_val.append(np.inner(vDict[(k[0])],vDict[(k[1])]))

		if os.environ['TEST_AND_TRAIN'] == 'YES':
			train_pair_file = open(os.path.join(self.rootdir,\
				"Data/train_pair_%s.p"%(os.environ['DATASET'])), "rb")
			train_dict = pickle.load(train_pair_file)
			for k, val in train_dict.items():
				self.original_val.append(val)
				self.computed_val.append(np.inner(vDict[(k[0])],vDict[(k[1])]))

		self.computeAndWriteResults(latReprName)