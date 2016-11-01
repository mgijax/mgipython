"""
Tests related to parsing input
"""

import sys,os.path
# adjust the path for running the tests locally, so that it can find mgipython (i.e. 3 dirs up)
sys.path.insert(1, os.path.join(os.path.dirname(__file__), '../..'))

import unittest

from mgipython.modelconfig import createMockDatabaseEngine
createMockDatabaseEngine()

from mgipython.parse.highlight import highlight, highlightContains, highlightEMAPA

# test the highlight filter function
class HighlightTestCase(unittest.TestCase):
    
    def setUp(self):
        # define once, what text wraps a highlighted term
        self.begin = "<mark>"
        self.end = "</mark>"
    
    def test_highlight_empty(self):
        self.assertEquals("test", highlight("test",""))
        
    def test_highlight_one_word_match(self):
        hl = highlight("test", "test")
        expected = self.expectedHighlight("test")
        self.assertEquals(expected, hl)
    
    def test_highlight_one_word_in_many(self):
        hl = highlight("test1 test2 test3", "test2", delim=None)
        expected = "test1 test2 test3"
        self.assertEquals(expected, hl)
        
    def test_highlight_many_word_match(self):
        hl = highlight("test1 test2 test3", "test1 test2 test3", delim=None)
        expected = (self.expectedHighlight("test1 test2 test3"))
        self.assertEquals(expected, hl)
        
    def test_highlight_phrase_in_many(self):
        hl = highlight("test1 test2 test3", "test2 test3", delim=None)
        expected = "test1 test2 test3"
        self.assertEquals(expected, hl)
        
    def test_highlight_wildcard(self):
        hl = highlight("testing", "test%", wildcard='%')
        expected = self.expectedHighlight("testing")
        self.assertEquals(expected, hl)
        
    def test_highlight_wildcard_reverse(self):
        hl = highlight("testing", "%ing", wildcard='%')
        expected = self.expectedHighlight("testing")
        self.assertEquals(expected, hl)
        
    def test_highlight_wildcard_in_middle(self):
        hl = highlight("testing", "t%ing", wildcard='%')
        expected = self.expectedHighlight("testing")
        self.assertEquals(expected, hl)
        
    def test_highlight_complex_wildcard(self):
        hl = highlight("testing123456789", "%es%ing123%8%", wildcard='%')
        expected = self.expectedHighlight("testing123456789")
        self.assertEquals(expected, hl)
        
    def test_highlight_match_in_list(self):
        hl = highlight("test1, test2, test3", "test2", delim=', ')
        expected = "test1, %s, test3" % (self.expectedHighlight("test2"))
        self.assertEquals(expected, hl)
        
    def test_highlight_multi_token_wildcard(self):
        hl = highlight("testing1, testing2, nottesting", "test%", wildcard='%', delim=', ')
        expected = "%s, %s, nottesting" % (self.expectedHighlight("testing1"), 
                                           self.expectedHighlight("testing2"))
        self.assertEquals(expected, hl)
        
    # helpers
    def expectedHighlight(self, expected):
        """
        Build expected highlight string
        """
        return "%s%s%s" % (self.begin, expected, self.end)
    
    
# test the highlightContains filter function
class HighlightContainsTestCase(unittest.TestCase):
    
    def setUp(self):
        # define once, what text wraps a highlighted term
        self.begin = "<mark>"
        self.end = "</mark>"
    
    def test_highlight_empty(self):
        self.assertEquals("test", highlightContains("test",""))
        
    def test_highlight_one_word_match(self):
        hl = highlightContains("test", "test")
        expected = self.expectedHighlight("test")
        self.assertEquals(expected, hl)
    
    def test_highlight_one_word_in_many(self):
        hl = highlightContains("test1 test2 test3", "test2")
        expected = "test1 test2 test3"
        expected = "test1 %s test3" % (self.expectedHighlight("test2"))
        self.assertEquals(expected, hl)
        
    def test_highlight_multiple_matches(self):
        hl = highlightContains("test1 test2 test3 test2 test2", "test2")
        expected = "test1 test2 test3"
        expected = "test1 %s test3 %s %s" % (self.expectedHighlight("test2"),
                                             self.expectedHighlight("test2"),
                                             self.expectedHighlight("test2"))
        self.assertEquals(expected, hl)
        
    def test_highlight_phrase_match(self):
        hl = highlightContains("test1 test2 test3", "test2 test3")
        expected = "test1 test2 test3"
        expected = "test1 %s" % (self.expectedHighlight("test2 test3"))
        self.assertEquals(expected, hl)
        
        
    # helpers
    def expectedHighlight(self, expected):
        """
        Build expected highlight string
        """
        return "%s%s%s" % (self.begin, expected, self.end)
      
# test the highlightEMAPA filter function
class HighlightEMAPATestCase(unittest.TestCase):
    
    def setUp(self):
        # define once, what text wraps a highlighted term
        self.begin = "<mark>"
        self.end = "</mark>"
    
    def test_highlight_empty(self):
        self.assertEquals("test", highlightEMAPA("test",[""]))
        
    def test_highlight_one_word_match(self):
        hl = highlightEMAPA("test", ["test"])
        expected = self.expectedHighlight("test")
        self.assertEquals(expected, hl)
        
    def test_highlight_multi_word_match(self):
        hl = highlightEMAPA("testing test", ["testing test"])
        expected = self.expectedHighlight("testing test")
        self.assertEquals(expected, hl)
        
    def test_highlight_wildcard_begins_match(self):
        hl = highlightEMAPA("testing test", ["test%"])
        expected = "%sing test" % self.expectedHighlight("test")
        self.assertEquals(expected, hl)

    def test_highlight_wildcard_ends_match(self):
        hl = highlightEMAPA("testing test", ["%test"])
        expected = "testing %s" % self.expectedHighlight("test")
        self.assertEquals(expected, hl)
        
    def test_highlight_wildcard_contains_match(self):
        hl = highlightEMAPA("testing test", ["%test%"])
        expected = "%sing %s" % (self.expectedHighlight("test"), self.expectedHighlight("test"))
        self.assertEquals(expected, hl)
        
    def test_highlight_mixed_tokens(self):
        hl = highlightEMAPA("testing test2", ["testing test2", "%test2%"])
        expected = self.expectedHighlight("testing test2")
        self.assertEquals(expected, hl)
        
    def test_highlight_mixed_tokens_different_order(self):
        hl = highlightEMAPA("testing test2", ["%test2%", "testing test2"])
        expected = "testing %s" % (self.expectedHighlight("test2"))
        self.assertEquals(expected, hl)
    
    def test_highlight_insensitive_begins(self):
        hl = highlightEMAPA("Testing test", ["test%"])
        expected = "%sing test" % (self.expectedHighlight("Test"))
        self.assertEquals(expected, hl) 
        
    def test_highlight_insensitive_ends(self):
        hl = highlightEMAPA("testing TEST", ["%test"])
        expected = "testing %s" % (self.expectedHighlight("TEST"))
        self.assertEquals(expected, hl) 
    
    # helpers
    def expectedHighlight(self, expected):
        """
        Build expected highlight string
        """
        return "%s%s%s" % (self.begin, expected, self.end)
    
        
def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(HighlightTestCase))
    suite.addTest(unittest.makeSuite(HighlightContainsTestCase))
    suite.addTest(unittest.makeSuite(HighlightEMAPATestCase))
    # add future test suites here
    return suite

if __name__ == '__main__':
    unittest.main()
