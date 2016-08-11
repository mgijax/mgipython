from mgipython.model import MGIUser
from mgipython.model import db
from base_dao import BaseDAO


class UserDAO(BaseDAO):
    
    model_class = MGIUser
    
    def search(self,
               login=None,
               name=None,
               _usertype_key=None,
               _userstatus_key=None,
               orcid=None,
               _createdby_key=None,
               _modifiedby_key=None
                ):
        """
        Search MGIUser by fields:
            login
            name
            _usertype_key
            orcid
            _createdby_key
            _modifiedby_key
        """
        query = MGIUser.query
        
        if login:
            login = login.lower()
            query = query.filter(db.func.lower(MGIUser.login).like(login))
            
        if name:
            name = name.lower()
            query = query.filter(db.func.lower(MGIUser.name).like(name))
            
        if _usertype_key:
            query = query.filter(MGIUser._usertype_key==_usertype_key)
        if _userstatus_key:
            query = query.filter(MGIUser._userstatus_key==_userstatus_key)
            
        if orcid:
            orcid = orcid.lower()
            query = query.filter(db.func.lower(MGIUser.orcid).like(orcid))
            
        if _createdby_key:
            query = query.filter(MGIUser._createdby_key==_createdby_key)
        if _modifiedby_key:
            query = query.filter(MGIUser._modifiedby_key==_modifiedby_key)
        
        query = query.order_by(MGIUser.login)
        
        return query.all()
        
        