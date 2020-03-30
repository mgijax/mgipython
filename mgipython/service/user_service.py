from mgipython.dao.user_dao import UserDAO
from mgipython.dao.vocterm_dao import VocTermDAO
from mgipython.model import MGIUser
from mgipython.domain.mgi_domains import UserDomain
from mgipython.domain.gxd_domains import *
from flask_login import current_user
from mgipython.error import NotFoundError
from mgipython.modelconfig import cache
from mgipython.domain import convert_models
from .vocterm_service import VocTermService

class UserService():
    
    user_dao = UserDAO()
    vocterm_dao = VocTermDAO()
    vocterm_service = VocTermService()
    
    def get_by_key(self, _user_key):
        user = self.user_dao.get_by_key(_user_key)
        if not user:
            raise NotFoundError("No MGIUser for _user_key=%d" % _user_key)
        return convert_models(user, UserDomain)
    
    def search(self, search_query):
        """
        Search using a SearchQuery
        """
        search_result = self.user_dao.search(search_query)
        
        # convert results to domain objects
        users = search_result.items
        search_result.items = convert_models(users, UserDomain)
        
        return search_result
        
    def create(self, args):
        """
        Create user with an argument object
        """
        user = MGIUser()
        # get the next primary key
        user._user_key = self.user_dao.get_next_key()
        # set MGIUser values
        user.login = args['login']
        user.name = args['name']
        user._usertype_key = args['_usertype_key']
        user._userstatus_key = args['_userstatus_key']
        
        #user._createdby_key = current_user._user_key
        #user._modifiedby_key = current_user._modifiedby_key
        self.user_dao.create(user)
        return convert_models(user, UserDomain)
        
        
    def update(self, key, args):
        """
        update user with and argument object
        """
        user = self.user_dao.get_by_key(key)
        if not user:
            raise NotFoundError("No MGIUser for _user_key=%d" % key)
        user.login = args['login']
        user.name = args['name']
        user._usertype_key = args['_usertype_key']
        user._userstatus_key = args['_userstatus_key']
        #user._modifiedby_key = current_user._modifiedby_key
        self.user_dao.update(user)
        return convert_models(user, UserDomain)
        
        
    def delete(self, _user_key):
        """
        Delete MGIUser object
        """
        user = self.user_dao.get_by_key(_user_key)
        if not user:
            raise NotFoundError("No MGIUser for _user_key=%d" % _user_key)
        self.user_dao.delete(user)
        return convert_models(user, UserDomain)

    def current_user(self):
        return convert_models(current_user, UserDomain)
