"""
Test the sort utilities
"""

import sys,os.path
# adjust the path for running the tests locally, so that it can find mgipython (i.e. 3 dirs up)
sys.path.insert(1, os.path.join(os.path.dirname(__file__), '../..'))

import unittest


from mgipython.util.sort import smartAlphaCompare


class SmartAlphaTest(unittest.TestCase):
    """
    Test smart alpha sorting
    """
    
    def test_simple_ascii(self):
        
        l = ["beta", "alpha"]       
        l.sort(smartAlphaCompare)
        
        self.assertEqual(["alpha","beta"], l)
        
        
    def test_simple_numeric(self):
        
        l = ["10","9","2","1"]       
        l.sort(smartAlphaCompare)
        
        self.assertEqual(["1","2","9","10"], l)
        
        
    def test_numeric_many_digits(self):
        
        l = ["1000000","1000","10","1","1000000000"]       
        l.sort(smartAlphaCompare)
        
        self.assertEqual(["1","10","1000","1000000","1000000000"], l)
        
        
    def test_basic_alpha_numeric(self):
        
        l = ["pax6","pax10","pax1"]       
        l.sort(smartAlphaCompare)
        
        self.assertEqual(["pax1","pax6","pax10"], l)
        
        
    def test_complex_alpha_numeric(self):
        
        l = ["10a5c50b12","10a5c50b1","1a5c50b12"]       
        l.sort(smartAlphaCompare)
        
        self.assertEqual(["1a5c50b12","10a5c50b1","10a5c50b12"], l)
        
        
    def test_alpha_numeric_with_spaces(self):
        
        l = ["somite 10", "somite 12", "somite 1"]       
        l.sort(smartAlphaCompare)
        
        self.assertEqual(["somite 1", "somite 10", "somite 12"], l)
        
        
    def test_alpha_numeric_with_special_characters(self):
        
        l = ["test.!@#$%^&*10", "test.!@#$%^&*9"]       
        l.sort(smartAlphaCompare)
        
        self.assertEqual(["test.!@#$%^&*9", "test.!@#$%^&*10"], l)
   
          
        
def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(SmartAlphaTest))
    # add future test suites here
    return suite

if __name__ == '__main__':
    unittest.main()
