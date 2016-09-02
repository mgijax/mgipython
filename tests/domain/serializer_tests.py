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
    
    def test_empty_serialize(self):
        class EmptyDomain(Serializer):
            __fields__ = []
            
        serializer = EmptyDomain()
        output = serializer.serialize()
        self.assertEqual(output, {})
        
    
    def test_simple_serialize(self):
        class SimpleDomain(Serializer):
            __fields__ = [
                Field("col1"),
                Field("col2")
            ]
            
        serializer = SimpleDomain()
        serializer.col1 = 1
        serializer.col2 = "2"
        
        output = serializer.serialize()
        expected = {
            "col1": 1,
            "col2": "2"
        }
        self.assertEqual(output, expected)
        
        
    def test_nested_serialize(self):
        
        class NestedDomain(Serializer):
            __fields__ = [
                Field("name")
            ]
        
        class ParentDomain(Serializer):
            __fields__ = [
                Field("child")
            ]
            
        parent = ParentDomain()
        child = NestedDomain()
        child.name = "test"
        parent.child = child
        
        output = parent.serialize()
        expected = {
            "child": {
                "name": "test"
            }
        }
        self.assertEqual(output, expected)
        
        
    def test_nested_list_serialize(self):
        
        class NestedDomain(Serializer):
            __fields__ = [
                Field("name")
            ]
        
        class ParentDomain(Serializer):
            __fields__ = [
                Field("children")
            ]
            
        parent = ParentDomain()
        
        child1 = NestedDomain()
        child1.name = "child1"
        
        child2 = NestedDomain()
        child2.name = "child2"
        
        parent.children = [child1, child2]
        
        output = parent.serialize()
        expected = {
            "children": [
                {"name": "child1"},
                {"name": "child2"}
            ]
        }
        self.assertEqual(output, expected)
        
    
    
class LoadFromDictTestCase(unittest.TestCase):
    """
    Test load_from_dict() method
    """
    
    def test_empty_dict(self):
        
        class SimpleDomain(Serializer):
            __fields__ = [
                Field("col1")
            ]
            
        serializer = SimpleDomain()
        serializer.load_from_dict({})
        
        self.assertEqual(serializer.col1, None)
        
        
    def test_simple_dict(self):
        
        class SimpleDomain(Serializer):
            __fields__ = [
                Field("col1"),
                Field("col2"),
                Field("col3")
            ]
            
        input = {
            "col1": 1,
            "col2": "2",
            "col3": [1,2,3,4]
        }
            
        serializer = SimpleDomain()
        serializer.load_from_dict(input)
        
        self.assertEqual(serializer.col1, 1)
        self.assertEqual(serializer.col2, "2")
        self.assertEqual(serializer.col3, [1,2,3,4])
        
        
    def test_extra_fields(self):
        
        class SimpleDomain(Serializer):
            __fields__ = [
                Field("col1"),
                Field("col2")
            ]
            
        input = {
            "col1": 1,
            "col2": "2",
            "col3": [1,2,3,4]
        }
            
        serializer = SimpleDomain()
        serializer.load_from_dict(input)
        
        self.assertEqual(serializer.col1, 1)
        self.assertEqual(serializer.col2, "2")
        self.assertFalse(hasattr(serializer, "col3"), "SimpleDomain should not have a col3 attribute")
        
    
    def test_missing_field(self):
        
        class SimpleDomain(Serializer):
            __fields__ = [
                Field("col1"),
                Field("col2"),
                Field("col3")
            ]
            
        input = {
            "col1": 1,
            "col2": "2"
        }
            
        serializer = SimpleDomain()
        serializer.load_from_dict(input)
        
        self.assertEqual(serializer.col1, 1)
        self.assertEqual(serializer.col2, "2")
        self.assertEqual(serializer.col3, None)
        
        
    def test_nested_domain(self):
        
        class NestedDomain(Serializer):
            __fields__ = [
                Field("name")
            ]
            
        class ParentDomain(Serializer):
            __fields__ = [
                Field("child", conversion_class=NestedDomain)
            ]
            
        input = {
            "child": {"name":"test"}
        }
            
        parent = ParentDomain()
        parent.load_from_dict(input)
        
        self.assertIsInstance(parent.child, NestedDomain)
        self.assertEqual(parent.child.name, "test")
        
        
    def test_nested_domain_as_list(self):
        
        class NestedDomain(Serializer):
            __fields__ = [
                Field("name")
            ]
            
        class ParentDomain(Serializer):
            __fields__ = [
                Field("children", conversion_class=NestedDomain)
            ]
            
        input = {
            "children": [
                {"name":"child1"},
                {"name":"child2"}
            ]
        }
            
        parent = ParentDomain()
        parent.load_from_dict(input)
        
        self.assertEqual(len(parent.children), 2)
        self.assertIsInstance(parent.children[0], NestedDomain)
        self.assertEqual(parent.children[1].name, "child2")
    
    
        
def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(LoadFromModelTestCase))
    suite.addTest(unittest.makeSuite(SerializeTestCase))
    suite.addTest(unittest.makeSuite(LoadFromDictTestCase))
    # add future test suites here
    return suite

if __name__ == '__main__':
    unittest.main()
