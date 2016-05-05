"""
Tests related to editing the EMAPA clipboard
"""

import sys,os.path
# adjust the path for running the tests locally, so that it can find mgipython (i.e. 3 dirs up)
sys.path.insert(1, os.path.join(os.path.dirname(__file__), '../..'))

import unittest

from mgipython.modelconfig import createMockDatabaseEngine
createMockDatabaseEngine()

from mgipython.model.edit.EMAPA import clipboard
from mgipython.model import *


class ClipboardSortTest(unittest.TestCase):
    """
    Test stage, term sorting
    """
    
    def setUp(self):
        self.seqnum = 1
        
        
    def tearDown(self):
        self.seqnum = 1
        
    
    def test_different_stage(self):
        
        l = [
             self.mockClipboardItem("term1", 20),
             self.mockClipboardItem("term1", 9)
             ]
        
        clipboard._sortItemsByAlpha(l)
        
        self.assertClipboardOrder(["term1 TS9", "term1 TS20"], l)
        
        
    def test_different_term(self):
        
        l = [
             self.mockClipboardItem("term12", 10),
             self.mockClipboardItem("term8", 10)
             ]
        
        clipboard._sortItemsByAlpha(l)
        
        self.assertClipboardOrder(["term8 TS10", "term12 TS10"], l)
        
        
    def test_smart_alpha(self):
        
        l = [
             self.mockClipboardItem("somite 11", 10),
             self.mockClipboardItem("somite 5", 10)
             ]
        
        clipboard._sortItemsByAlpha(l)
        
        self.assertClipboardOrder(["somite 5 TS10", "somite 11 TS10"], l)
        
        
    # helper functions
    def assertClipboardOrder(self, expectedList, actualItems):
        """
            Asserts that expectedList
                in format ["term TSstage", ...]
            matches the order of actualItems clipboard items
        """
        
        # format actualList
        actualList = []
        for item in actualItems:
            actualList.append("%s TS%d" % (item.emapa_term.term, item.emapa._stage_key))
        
        self.assertEqual(expectedList, actualList)
        
        
    def mockClipboardItem(self, term, stage):
        """
        Create a mock SetMember object for testing
        """
        setMember = SetMember()
        
        # always set with and increment seqnum counter
        setMember.sequencenum = self.seqnum
        self.seqnum += 1
        
        
        # set the term
        vocTerm = VocTerm()
        vocTerm.term = term
        setMember.emapa_term = vocTerm
        
        
        # set the stage
        setMemberEMAPA = SetMemberEMAPA()
        setMemberEMAPA._stage_key = stage
        setMember.emapa = setMemberEMAPA
        
        
        return setMember
        
          
        
def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ClipboardSortTest))
    # add future test suites here
    return suite

if __name__ == '__main__':
    unittest.main()
