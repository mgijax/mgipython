from mgipython.model import *
from .base_dao import BaseDAO


class ActualDbDAO(BaseDAO):
    
    model_class = ActualDb
    
    def _build_search_query(self, search_query):

        query = ActualDb.query
        
        if search_query.has_valid_param('_actualdb_key'):
            _actualdb_key = search_query.get_value('_actualdb_key')
            query = query.filter(ActualDb._actualdb_key==_actualdb_key)
 
        return query
        
