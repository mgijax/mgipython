"""
Help with sorting results in service methods
"""


class ValidMarkerSortHelper(object):
    
    def sort(self, markers):
        markers.sort(self.compare_valid_marker)
        
    
    def compare_valid_marker(self, m1, m2):
        """
        Sort markers by placing 
            protein coding genes first.
            all else second
        """
        m1_featuretypes = [t.term for t in m1.featuretype_vocterms]
        m2_featuretypes = [t.term for t in m2.featuretype_vocterms]
        
        m1_is_coding = 'protein coding gene' in m1_featuretypes
        m2_is_coding = 'protein coding gene' in m2_featuretypes
        
        if m1_is_coding == m2_is_coding:
            return 0
        
        if m1_is_coding:
            return -1
        
        return 1
    
    
            
        
    