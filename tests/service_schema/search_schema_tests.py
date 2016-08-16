"""
Test the search schema classes
"""

import sys,os.path
# adjust the path for running the tests locally, so that it can find mgipython (i.e. 3 dirs up)
sys.path.insert(1, os.path.join(os.path.dirname(__file__), '../..'))

import unittest


from mgipython.service_schema.search import SearchQuery


class SearchQueryParamValidatorTest(unittest.TestCase):
    """
    Test how SearchQuery validates query params
    """
    
    def setUp(self):
        self.search_query = SearchQuery()
    
    # False cases
    def test_none(self):
        self.assertFalse(
            self.search_query._is_value_not_empty(None)
        )
        
    def test_empty_string(self):
        self.assertFalse(
            self.search_query._is_value_not_empty("")
        )
        
    def test_empty_list(self):
        self.assertFalse(
            self.search_query._is_value_not_empty([])
        )
        
    # True / valid cases
    def test_boolean_false(self):
        self.assertTrue(
            self.search_query._is_value_not_empty(False)
        )
        
    def test_boolean_true(self):
        self.assertTrue(
            self.search_query._is_value_not_empty(True)
        )
        
    def test_string(self):
        self.assertTrue(
            self.search_query._is_value_not_empty("value")
        )
        
    def test_list(self):
        self.assertTrue(
            self.search_query._is_value_not_empty(["value"])
        )
        
    def test_list_with_empty_item(self):
        self.assertTrue(
            self.search_query._is_value_not_empty([""])
        )
        
    def test_list_with_none_item(self):
        self.assertTrue(
            self.search_query._is_value_not_empty([None])
        )
     
          
        
def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(SearchQueryParamValidatorTest))
    # add future test suites here
    return suite

if __name__ == '__main__':
    unittest.main()
