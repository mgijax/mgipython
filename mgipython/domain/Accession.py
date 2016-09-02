
class AccessionDomain():

    def __init__(self, db_object=None):

        if db_object != None:
            self.key = db_object._accession_key
            self.accid = db_object.accid
        else:
            return None
