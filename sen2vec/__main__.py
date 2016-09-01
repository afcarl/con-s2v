#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import random
import importlib
from io import open
from utility.ArgumentParserUtility  import ArgumentParserUtility
#from argparse import ArgumentParser, FileType, ArgumentDefaultsHelpFormatter
#from collections import Counter

#from concurrent.futures import ProcessPoolExecutor

from documentReader.NewsGroupReader import NewsGroupReader 
from documentReader.ReutersReader import ReutersReader


from six import text_type as unicode
# from six import iteritems
# from six.moves import range


# import psutil
# from multiprocessing import cpu_count

from log_manager.log_config import Logger 


module_dict ={"reuter": "documentReader.ReutersReader", 
		"news": "documentReader.NewsGroupReader" }
class_dict = {"reuter": "ReutersReader", 
		"news": "NewsGroupReader"}

def main():
	"""
	Logging levels can be: critical, error, warning, info, debug and notset
	We can Log as info, debug, warning, error and critical
	It Dynamic Loads corresonding dataset specific classes. 
	"""
	argparser = ArgumentParserUtility('Sen2Vec')
	argparser.add_argument_to_parser("dataset", "Please enter dataset "\
		"to work on [reuter, news]", True)
	argparser.parse_argument()

	
	dataset = argparser.get_value_of_argument("dataset")
	module = None 
	try: 
		module = module_dict[dataset]
		klass = class_dict[dataset]
	except: 
		Logger.logr.error("Dataset Name does not match")
		sys.exit()

	Klass = getattr(importlib.import_module(module), klass)
	reader = Klass()
	Logger.logr.info("Successfuly loaded the class %s", str(Klass))
	
	reader.readDocument()

if __name__ == "__main__":
   sys.exit(main())