from mgipython.model import MGIType
from mgipython.model import db
from base_dao import BaseDAO


class MGITypeDAO(BaseDAO):
    
    model_class = MGIType
    
    def _build_search_query(self, search_query):

        query = MGIType.query
        
        if search_query.has_valid_param('name'):
            name = search_query.get_value('name')
            name = name.lower()
            query = query.filter(db.func.lower(MGIType.name).like(name))

        if search_query.has_valid_param('_mgitype_key'):
            _mgitype_key = search_query.get_value('_mgitype_key')
            query = query.filter(MGIType._mgitype_key==_mgitype_key)
 
        if search_query.has_valid_param('_createdby_key'):
            _createdby_key = search_query.get_value('_createdby_key')
            query = query.filter(MGIType._createdby_key==_createdby_key)
            
        if search_query.has_valid_param('_modifiedby_key'):
            _modifiedby_key = search_query.get_value('_modifiedby_key')
            query = query.filter(MGIType._modifiedby_key==_modifiedby_key)
        
        return query
        
