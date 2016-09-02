
class UserDomain():

    def __init__(self, db_object=None):

        if db_object != None:
            self.key = db_object._user_key
            self.name = db_object.name
            self.login = db_object.login
        else:
            return None
