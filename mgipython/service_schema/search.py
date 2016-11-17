"""
Models for driving search services
"""
import logging
from mgipython.domain import Field, Serializer


logger = logging.getLogger('mgipython.service_schema')


class Paginator(Serializer):
    """
    page_num is the page you are on or requesting
    page_size is the number of results per page
    """
    __fields__ = [
        Field("page_num"),
        Field("page_size")
    ]

    def __init__(self):
        super(Paginator, self).__init__()
        self.page_num = 1
        self.page_size = 0
        
    
    
class SearchQuery(Serializer):
    """
    params is a dict of search field names to values
    sorts is a list of sort argument strings
    paginator is a Paginator instance
    """
    __fields__ = [
        Field("_params"),
        Field("sorts"),
        Field("paginator", conversion_class=Paginator)
    ]
    
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
        
    def clear_param(self, param_name):
        """
        unset a single param_name, value pair
        """
        self._params[param_name] = None
    
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
        
        if isinstance(value, int):
            return True
        
        return True and value
    
    
    def get_value(self, param_name):
        """
        returns param value
        """
        return self._params[param_name]
    
    
class SearchResults(Serializer):
    """
    items is the list of result objects (typically database models)
    total_count of items (if paginated, represents total count in database)
    paginator - populated if results are paginated
    """
    
    __fields__ = [
        Field("items"),
        Field("total_count"),
        Field("paginator", conversion_class=Paginator)
    ]

    def __init__(self):
        super(SearchResults, self).__init__()
        self.items = []
        self.total_count = 0
        self.paginator = None
