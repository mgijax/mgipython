from mgipython.dao.user_dao import UserDAO
from mgipython.dao.vocterm_dao import VocTermDAO
from mgipython.model import MGIUser
from mgipython.exception import NotFoundException
from mgipython.modelconfig import cache

class UserService():
    
    user_dao = UserDAO()
    vocterm_dao = VocTermDAO()
    
    def get_by_key(self, _user_key):
        user = self.user_dao.get_by_key(_user_key)
        return user
    
    
    def search(self, args):
        """
        Search using an argument object
        """
        users = self.user_dao.search(
            login=args.login,
            name=args.name,
            _usertype_key=args._usertype_key,
            _userstatus_key=args._userstatus_key,
            orcid=args.orcid,
            _createdby_key=args._createdby_key,
            _modifiedby_key=args._modifiedby_key
        )
        return users
    
    
        
    def create(self, args):
        """
        Create user with an argument object
        """
        user = MGIUser()
        # get the next primary key
        user._user_key = self.user_dao.get_next_key()
        # set MGIUser values
        user.login = args.login
        user.name = args.name
        user._usertype_key = args._usertype_key
        user._userstatus_key = args._userstatus_key
        
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
            raise NotFoundException("No MGIUser for _user_key=%d" % key)
        user.login = args.login
        user.name = args.name
        user._usertype_key = args._usertype_key
        user._userstatus_key = args._userstatus_key
        #user._modifiedby_key = current_user._modifiedby_key
        return user
        
        
    def delete(self, _user_key):
        """
        Delete MGIUser object
        """
        user = self.user_dao.get_by_key(key)
        if not user:
            raise NotFoundException("No MGIUser for _user_key=%d" % key)
        self.user_dao.delete(user)
        
    
    @cache.memoize()
    def get_user_status_choices(self):
        """
        Get all possible userstatus choices
        return format is
        { 'choices': [{'term', '_term_key'}] }
        """
        terms = self.vocterm_dao.search(_vocab_key=22)
        json = {
            'choices':[]
        }
        for term in terms:
            json['choices'].append({'term':term.term, '_term_key':term._term_key})
        
        return json
    
    @cache.memoize()
    def get_user_type_choices(self):
        """
        Get all possible usertype choices
        return format is
        { 'choices': [{'term', '_term_key'}] }
        """
        terms = self.vocterm_dao.search(_vocab_key=23)
        json = {
            'choices':[]
        }
        for term in terms:
            json['choices'].append({'term':term.term, '_term_key':term._term_key})
        
        return json
        
        