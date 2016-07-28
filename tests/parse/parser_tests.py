"""
Tests related to parsing input
"""

import sys,os.path
# adjust the path for running the tests locally, so that it can find mgipython (i.e. 3 dirs up)
sys.path.insert(1, os.path.join(os.path.dirname(__file__), '../..'))

import unittest

from mgipython.modelconfig import createMockDatabaseEngine
createMockDatabaseEngine()

from mgipython.parse import emapaStageParser
from mgipython.error import  InvalidStageInputError


# EMAPA theiler stage search parser
class TheilerStageParserTestCase(unittest.TestCase):
    """
    Test parsing of theiler stage input
    """
    
    
    def test_empty_input(self):
        stages = emapaStageParser("")
        expected = []
        self.assertEqual(expected, stages)

    def test_single_stage(self):
        stages = emapaStageParser("10")
        expected = [10]
        self.assertEqual(expected, stages)
        
    def test_invalid_integer(self):
        """
        non-integer should throw custom exception
        """
        
        with self.assertRaises(InvalidStageInputError):
            emapaStageParser("b")
            
    def test_list_input(self):
       stages = emapaStageParser("1, 11, 10")
       expected = [1, 11, 10]
       self.assertEqual(expected, stages)
       
    def test_list_input_unique(self):
       stages = emapaStageParser("1, 10, 10, 10, 20")
       expected = [1, 10, 20]
       self.assertEqual(expected, stages)
       
    def test_range_input(self):
       stages = emapaStageParser("7-10")
       expected = [7, 8, 9, 10]
       self.assertEqual(expected, stages)
       
    def test_range_input_same_stage(self):
       stages = emapaStageParser("10-10")
       expected = [10]
       self.assertEqual(expected, stages)
       
    def test_invalid_range_multiple_ranges(self):
        
        with self.assertRaises(InvalidStageInputError):
            emapaStageParser("1-10-4")
            
        with self.assertRaises(InvalidStageInputError):
            emapaStageParser("1--4")
            
    def test_invalid_range_non_integer(self):
        
        with self.assertRaises(InvalidStageInputError):
            emapaStageParser("1-b")
            
        with self.assertRaises(InvalidStageInputError):
            emapaStageParser("b-10")
            
        with self.assertRaises(InvalidStageInputError):
            emapaStageParser("x-z")
            
    def test_invalid_range_empty_range(self):
        
        with self.assertRaises(InvalidStageInputError):
            emapaStageParser(" -4")
            
        with self.assertRaises(InvalidStageInputError):
            emapaStageParser("10 - ")
            
        with self.assertRaises(InvalidStageInputError):
            emapaStageParser(" - ")
            
            
    def test_invalid_range_left_greater_than_right(self):
        
        with self.assertRaises(InvalidStageInputError):
            emapaStageParser("10 - 2")
            
            
    def test_range_and_list(self):
       stages = emapaStageParser("1, 5-7, 20, 22-24")
       expected = [1, 5,6,7, 20, 22,23,24]
       self.assertEqual(expected, stages)
       
       
    def test_wildcard_asterisk(self):
       stages = emapaStageParser("*")
       expected = range(1,29)
       self.assertEqual(expected, stages)
       
    def test_wildcard_all(self):
       stages = emapaStageParser("all")
       expected = range(1,29)
       self.assertEqual(expected, stages)
       
       stages = emapaStageParser("ALL")
       self.assertEqual(expected, stages)
       
       
    def test_wildcard_in_list (self):
       stages = emapaStageParser("1, *, 20")
       expected = range(1,29)
       self.assertEqual(expected, stages)
        
          
        
def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TheilerStageParserTestCase))
    # add future test suites here
    return suite

if __name__ == '__main__':
    unittest.main()
