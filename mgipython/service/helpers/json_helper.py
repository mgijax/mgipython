'''
Name: json_helper.py
Purpose: to provide wrappers that will easily convert standard Python data types to JSON strings,
    and vice-versa
Note: This only deals with standard Python data types (int, float, string, boolean, list, dictionary).  Tuples
    are converted to lists when generating JSON.  Objects will raise a TypeError if you attempt to convert
    them to JSON.
'''

import json

class JsonHelper:
    '''
    provides methods for converting standard Python data types to and from JSON strings
    '''

    def __init__(self):
        '''
        Constructor; no-op for now.
        '''
        return
    
    def toJson (self, data):
        return json.dumps(data)
    
    def fromJson (self, s):
        return json.loads(s)