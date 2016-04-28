"""
Run all mgipython test suites
"""
import sys,os.path

# disable SQLAlchemy Warnings
import warnings
from sqlalchemy.exc import SAWarning
warnings.filterwarnings('ignore', category=SAWarning)

import unittest

# import all sub test suites
import dag_tests

from util import gxdindex_aggregator_tests
from util import sort_tests

# add the test suites
def master_suite():
	suites = []
	suites.append(dag_tests.suite())
	suites.append(gxdindex_aggregator_tests.suite())
        suites.append(sort_tests.suite())
	
	master_suite = unittest.TestSuite(suites)
	return master_suite

if __name__ == '__main__':
	test_suite = master_suite()
	runner = unittest.TextTestRunner()
	
	ret = not runner.run(test_suite).wasSuccessful()
	sys.exit(ret)
