from mgipython.dao.user_dao import UserDAO
from mgipython.model import MGIUser

class UserManager():
    
    user_dao = UserDAO()
    
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
        
        
    def edit(self, user, args):
        """
        Edit user with and argument object
        """
        user.login = args.login
        user.name = args.name
        user._usertype_key = args._usertype_key
        user._userstatus_key = args._userstatus_key
        #user._modifiedby_key = current_user._modifiedby_key
        
        
    def delete(self, user):
        """
        Delete MGIUser object
        """
        self.user_dao.delete(user)
        
        
        