from mgipython.model import MGIUser
from mgipython.model import db
from base_dao import BaseDAO


class UserDAO(BaseDAO):
    
    model_class = MGIUser
    
    def _build_search_query(self, search_query):
        """
        search_query is a SearchQuery object
        
        Search MGIUser by fields:
            login
            name
            _usertype_key
            orcid
            _createdby_key
            _modifiedby_key
        """
        query = MGIUser.query
        
        if search_query.has_valid_param('login'):
            login = search_query.get_value('login')
            login = login.lower()
            query = query.filter(db.func.lower(MGIUser.login).like(login))
            
        if search_query.has_valid_param('name'):
            name = search_query.get_value('name')
            name = name.lower()
            query = query.filter(db.func.lower(MGIUser.name).like(name))
            
        if search_query.has_valid_param('_usertype_key'):
            _usertype_key = search_query.get_value('_usertype_key')
            query = query.filter(MGIUser._usertype_key==_usertype_key)
            
        if search_query.has_valid_param('_userstatus_key'):
            _userstatus_key = search_query.get_value('_userstatus_key')
            query = query.filter(MGIUser._userstatus_key==_userstatus_key)
            
        if search_query.has_valid_param('orcid'):
            orcid = search_query.get_value('orcid')
            orcid = orcid.lower()
            query = query.filter(db.func.lower(MGIUser.orcid).like(orcid))
            
            
        if search_query.has_valid_param('_createdby_key'):
            _createdby_key = search_query.get_value('_createdby_key')
            query = query.filter(MGIUser._createdby_key==_createdby_key)
            
        if search_query.has_valid_param('_modifiedby_key'):
            _modifiedby_key = search_query.get_value('_modifiedby_key')
            query = query.filter(MGIUser._modifiedby_key==_modifiedby_key)
        
        query = query.order_by(MGIUser.login)
        
        
        return query
        
