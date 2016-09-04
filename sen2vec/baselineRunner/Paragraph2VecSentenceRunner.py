#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os 
import sys
import pickle
from gensim.models import Doc2Vec
import gensim.models.doc2vec
from log_manager.log_config import Logger 
import multiprocessing
from baselineRunner.BaselineRunner import BaselineRunner
from gensim.models.doc2vec import TaggedDocument


assert gensim.models.doc2vec.FAST_VERSION > -1, \
	"this will be painfully slow otherwise"

class TaggedLineSentence(object):
    def __init__(self, filename):
        self.data_file=open(filename, 'rb')

    def __iter__(self):
       while True: 
       	try:
       		sent_dict = pickle.load(self.data_file)
       		content = sent_dict ["content"]
       		id_ = sent_dict["id"]
       		Logger.logr.info(content)
       		Logger.logr.info(id_)
       		yield TaggedDocument(words=content.split(),\
       			tags=['SENT_%s' %(id_)])

       	except EOFError:
        	break


class Paragraph2VecSentenceRunner(BaselineRunner):
	def __init__(self, *args, **kwargs):
		"""
		"""
		BaselineRunner.__init__(self, *args, **kwargs)
		self.sentsFile = os.environ['P2VECSENTRUNNERINFILE']
		self.sentReprFile = os.environ['P2VECSENTRUNNEROUTFILE']
		self.cores = multiprocessing.cpu_count()

	
	def prepareData(self):
		"""
		Query Sentence Data. As a rough heuristics 
		sentences shorter than 9 words are excluded. We dump 
		both the sentence and their ids in different files. I am 
		not sure whether I am doing correct encoding.  
		"""
		self.postgresConnection.connect_database()
		
		sentfiletoWrite = open("%s.p"%(self.sentsFile),"wb")
	

		for result in self.postgresConnection.memoryEfficientSelect(["id","content"],\
			 ["sentence"], [], [], ["id"]):
			for row_id in range(0,len(result)):
				id_ = result[row_id][0]
				content = result[row_id][1]
				if len(content.split()) < 5:
					continue 
				else:
					sent_dict = {}
					sent_dict["id"] = id_ 
					content = gensim.utils.to_unicode(content.lower())
					content = content.replace("\n", " ")
					sent_dict["content"] = content	
					pickle.dump(sent_dict,sentfiletoWrite)
					
		sentfiletoWrite.close()
	
	def runTheBaseline(self):
		"""
		"""
		para2vecModel = Doc2Vec(TaggedLineSentence("%s.p"%(self.sentsFile)),\
			 size=100, window=4, min_count=4, workers=self.cores)
		para2vecModel.save("%s"%(self.sentReprFile))

	def runEvaluationTask(self):
		"""
		"""
		pass

	
	def prepareStatisticsAndWrite(self):
		"""
		"""
		pass