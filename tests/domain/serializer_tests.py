"""
Tests related to the Serializer base class
"""

import sys,os.path
# adjust the path for running the tests locally, so that it can find mgipython (i.e. 3 dirs up)
sys.path.insert(1, os.path.join(os.path.dirname(__file__), '../..'))

import unittest

from mgipython.modelconfig import createMockDatabaseEngine
createMockDatabaseEngine()

from mgipython.domain import Field, Serializer


# sample classes for testing
class NoFieldsModel(object):
    pass

class SimpleModel(object):
    col1 = 1
    col2 = "2"
    col3 = [1,2,3,4]
    
    
# Nested models for testing child relationships
class NestedModel(object):
    def __init__(self, name):
      self.name = name
    
class ParentModel(object):
    child = NestedModel("single_child")
    
    children = [
            NestedModel("child1"), 
            NestedModel("child2"), 
            NestedModel("child3")
    ]



class LoadFromModelTestCase(unittest.TestCase):
    """
    Test load_from_model() method
    """
    
    def test_no_fields_mapped(self):
        """
        No errors should be thrown
        """
        
        class SimpleDomain(Serializer):
            __fields__ = [
                Field("col1"),
                Field("col2"),
                Field("col3")
            ]
            
        simple_model = NoFieldsModel()
            
        serializer = SimpleDomain()
        serializer.load_from_model(simple_model)
        
        self.assertEqual(serializer.col1, None)
        self.assertEqual(serializer.col2, None)
        self.assertEqual(serializer.col3, None) 
        
    
    def test_simple_map_all_fields(self):
        
        class SimpleDomain(Serializer):
            __fields__ = [
                Field("col1"),
                Field("col2"),
                Field("col3")
            ]
            
        simple_model = SimpleModel()
            
        serializer = SimpleDomain()
        serializer.load_from_model(simple_model)
        
        self.assertEqual(serializer.col1, simple_model.col1)
        self.assertEqual(serializer.col2, simple_model.col2)
        self.assertEqual(serializer.col3, simple_model.col3) 
        
        
    def test_simple_map_partial_fields(self):
        
        class SimpleDomain(Serializer):
            __fields__ = [
                Field("col1"),
                Field("col2"),
                
                # col4 does not exist in model, should be None
                Field("col4")
            ]
            
        simple_model = SimpleModel()
            
        serializer = SimpleDomain()
        serializer.load_from_model(simple_model)
        
        self.assertEqual(serializer.col1, simple_model.col1)
        self.assertEqual(serializer.col2, simple_model.col2)
        self.assertEqual(serializer.col4, None) 
        
        
    def test_single_nested_model(self):
        
        class NestedDomain(Serializer):
            __fields__ = [
                Field("name")
            ]
            
        class ParentDomain(Serializer):
            __fields__ = [
                Field("child", conversion_class=NestedDomain)
            ]
            
        parent_model = ParentModel()
            
        serializer = ParentDomain()
        serializer.load_from_model(parent_model)
        
        self.assertIsInstance(serializer.child, NestedDomain)
        self.assertEqual(serializer.child.name, "single_child")
        
        
    def test_single_nested_model_list(self):
        
        class NestedDomain(Serializer):
            __fields__ = [
                Field("name")
            ]
            
        class ParentDomain(Serializer):
            __fields__ = [
                Field("children", conversion_class=NestedDomain)
            ]
            
        parent_model = ParentModel()
            
        serializer = ParentDomain()
        serializer.load_from_model(parent_model)
        
        # there should be 3 children of type NestedDomain
        self.assertEqual(len(serializer.children), 3)
        self.assertIsInstance(serializer.children[0], NestedDomain)
        self.assertEqual(serializer.children[0].name, "child1")
        
        
    def test_computed_field(self):
        
        class ComputedDomain(Serializer):
            __fields__ = [
              Field("computed")
            ]
            
            def get_computed(self, model):
                return model.col2 + "_test"
            
        simple_model = SimpleModel()
            
        serializer = ComputedDomain()
        serializer.load_from_model(simple_model)
        
        self.assertEqual(serializer.computed, "2_test")
        
        
    def test_computed_nested_model(self):
        
        class NestedDomain(Serializer):
            __fields__ = [
                Field("name")
            ]
            
        class ComputedDomain(Serializer):
            __fields__ = [
              Field("computed", conversion_class=NestedDomain)
            ]
            
            def get_computed(self, model):
                return model.children[0]
            
        parent_model = ParentModel()
            
        serializer = ComputedDomain()
        serializer.load_from_model(parent_model)
        
        self.assertIsInstance(serializer.computed, NestedDomain)
        self.assertEqual(serializer.computed.name, "child1")
    

class SerializeTestCase(unittest.TestCase):
    """
    Test serialize() method
    """
    
    
        
def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(LoadFromModelTestCase))
    suite.addTest(unittest.makeSuite(SerializeTestCase))
    # add future test suites here
    return suite

if __name__ == '__main__':
    unittest.main()
