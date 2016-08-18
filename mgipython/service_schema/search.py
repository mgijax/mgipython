"""
Models for driving search services
"""
import logging

logger = logging.getLogger('mgipython.service_schema')


class Paginator():
    """
    page_num is the page you are on or requesting
    page_size is the number of results per page
    """
    page_num = 1
    page_size = 0

    def __init__(self):
        self.page_num = 1
        self.page_size = 0
    
    
class SearchQuery():
    """
    params is a dict of search field names to values
    sorts is a list of sort argument strings
    paginator is a Paginator instance
    """
    _params = {}
    sorts = []
    paginator = None
 
    def __init__(self):
        self._params = {}
        self.sorts = []
        self.paginator = None
    
    def set_params(self, params):
        """
        sets search params
        """
        for key, value in params.items():
            self.set_param(key, value)

    def set_param(self, param_name, value):
        """
        set a single param_name, value pair
        """
        self._params[param_name] = value
        
    
    def has_valid_param(self, param_name):
        """
        check for key param_name
        and checks if it exists
        """
        param_valid = False
        
        param_exists = param_name in self._params
        if param_exists:
            
            param_valid = self._is_value_not_empty(self._params[param_name])
            
        return param_valid
    
    
    def _is_value_not_empty(self, value):
        """
        checks if the value is not empty
        """
        if isinstance(value, bool):
            return True
        
        return True and value
    
    
    def get_value(self, param_name):
        """
        returns param value
        """
        return self._params[param_name]
    
    
    
    
class SearchResults():
    """
    items is the list of result objects (typically database models)
    total_count of items (if paginated, represents total count in database)
    paginator - populated if results are paginated
    """
    items = []
    total_count = 0
    paginator = None

    def __init__(self):
        self.items = []
        self.total_count = 0
        paginator = None
