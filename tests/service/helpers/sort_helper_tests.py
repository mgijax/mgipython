"""
Tests related to the Serializer base class
"""

import sys,os.path
# adjust the path for running the tests locally, so that it can find mgipython (i.e. 3 dirs up)
sys.path.insert(1, os.path.join(os.path.dirname(__file__), '../../..'))

import unittest

from mgipython.modelconfig import createMockDatabaseEngine
createMockDatabaseEngine()

from mgipython.model import Marker, VocTerm
from mgipython.service.helpers.sort_helper import ValidMarkerSortHelper



class ValidMarkerSortHelperTest(unittest.TestCase):
    """
    Test ValidMarkerSortHelper.sort()
    """
    
    def setUp(self):
        self.sort_helper = ValidMarkerSortHelper()
        
    def tearDown(self):
        pass
    
    # helpers
    def _mock_marker(self, _marker_key, featuretypes):
        """
        Create a mock marker object for testing
        """
        marker = Marker()
        marker.symbol = "Test (key=%s)" % _marker_key
        marker._marker_key = _marker_key
        marker.featuretype_vocterms = self._create_feature_types(featuretypes)
        
        return marker
    
    
    def _create_feature_types(self, terms):
        """
        Create list of feature type vocterm objects
        """
        featuretype_vocterms = []
        
        for term in terms:
            vocterm = VocTerm()
            vocterm.term = term
            featuretype_vocterms.append(vocterm)
            
        return featuretype_vocterms
    
    
    # Tests
    def test_basic_protein_coding_sort(self):
        """
        protein coding genes always sort first
        """
        marker1 = self._mock_marker(1, ['non-coding gene'])
        marker2 = self._mock_marker(2, ['protein coding gene'])
        markers = [marker1, marker2]
        
        self.sort_helper.sort(markers)
        
        self.assertEqual([marker2, marker1], markers)
        
    def test_multiple_featuretypes(self):
        """
        protein coding genes always sort first
        """
        
        marker1 = self._mock_marker(1, ['non-coding gene', 'test feature type'])
        marker2 = self._mock_marker(2, ['test feature type', 'protein coding gene'])
        markers = [marker1, marker2]
        
        self.sort_helper.sort(markers)
        
        self.assertEqual([marker2, marker1], markers)
        
        
    def test_same_featuretype(self):
        
        marker1 = self._mock_marker(1, ['non-coding gene'])
        marker2 = self._mock_marker(2, ['non-coding gene'])
        markers = [marker1, marker2]
        
        self.sort_helper.sort(markers)
        
        self.assertEqual([marker1, marker2], markers)
        
    
    def test_same_protein_coding_featuretype(self):
        
        marker1 = self._mock_marker(1, ['protein coding gene'])
        marker2 = self._mock_marker(2, ['protein coding gene'])
        markers = [marker1, marker2]
        
        self.sort_helper.sort(markers)
        
        self.assertEqual([marker1, marker2], markers)
        
        
    def test_no_featuretype(self):
        
        marker1 = self._mock_marker(1, [])
        marker2 = self._mock_marker(2, [])
        markers = [marker1, marker2]
        
        self.sort_helper.sort(markers)
        
        self.assertEqual([marker1, marker2], markers)
        
  
  
    
    
        
def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ValidMarkerSortHelperTest))
    # add future test suites here
    return suite

if __name__ == '__main__':
    unittest.main()
