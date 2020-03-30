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
from . import dag_tests

from .domain import serializer_tests

from .model import edit_clipboard_tests

from .parse import parser_tests
from .parse import highlight_tests

from .service.helpers import sort_helper_tests

from .service_schema import search_schema_tests

from .util import gxdindex_aggregator_tests
from .util import sort_tests

# add the test suites
def master_suite():
    suites = []
    suites.append(dag_tests.suite())
    suites.append(edit_clipboard_tests.suite())
    suites.append(gxdindex_aggregator_tests.suite())
    suites.append(parser_tests.suite())
    suites.append(highlight_tests.suite())
    suites.append(search_schema_tests.suite())
    suites.append(serializer_tests.suite())
    suites.append(sort_tests.suite())
    suites.append(sort_helper_tests.suite())

    master_suite = unittest.TestSuite(suites)
    return master_suite

if __name__ == '__main__':
    test_suite = master_suite()
    runner = unittest.TextTestRunner()

    ret = not runner.run(test_suite).wasSuccessful()
    sys.exit(ret)
