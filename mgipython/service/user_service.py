from mgipython.dao.user_dao import UserDAO
from mgipython.dao.vocterm_dao import VocTermDAO
from mgipython.model import MGIUser
from mgipython.error import NotFoundError
from mgipython.modelconfig import cache
from vocterm_service import VocTermService

class UserService():
    
    user_dao = UserDAO()
    vocterm_dao = VocTermDAO()
    vocterm_service = VocTermService()
    
    def get_by_key(self, _user_key):
        user = self.user_dao.get_by_key(_user_key)
        if not user:
            raise NotFoundError("No MGIUser for _user_key=%d" % _user_key)
        return user
    
    
    def search(self, search_query):
        """
        Search using a SearchQuery
        """
        users = self.user_dao.search(search_query)
        return users
    
    
        
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
        self.user_dao.save(user)
        
        return user
        
        
    def edit(self, key, args):
        """
        Edit user with and argument object
        """
        user = self.user_dao.get_by_key(key)
        if not user:
            raise NotFoundError("No MGIUser for _user_key=%d" % key)
        user.login = args['login']
        user.name = args['name']
        user._usertype_key = args['_usertype_key']
        user._userstatus_key = args['_userstatus_key']
        #user._modifiedby_key = current_user._modifiedby_key
        
        self.user_dao.save()
        return user
        
        
    def delete(self, _user_key):
        """
        Delete MGIUser object
        """
        user = self.user_dao.get_by_key(_user_key)
        if not user:
            raise NotFoundError("No MGIUser for _user_key=%d" % _user_key)
        self.user_dao.delete(user)
        
    
    @cache.memoize()
    def get_user_status_choices(self):
        """
        Get all possible userstatus choices
        return format is
        { 'choices': [{'term', '_term_key'}] }
        """
        
        user_status_vocab_key = 22
        return self.vocterm_service \
            .get_term_choices_by_vocab_key(user_status_vocab_key)
    
    @cache.memoize()
    def get_user_type_choices(self):
        """
        Get all possible usertype choices
        return format is
        { 'choices': [{'term', '_term_key'}] }
        """
        user_type_vocab_key = 23
        return self.vocterm_service \
            .get_term_choices_by_vocab_key(user_type_vocab_key)
        
        
