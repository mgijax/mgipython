
class VocTermDomain():

    def __init__(self, db_object=None):

        if db_object != None:
            self.key = db_object._term_key
            self.term = db_object.term
        else:
            return None
