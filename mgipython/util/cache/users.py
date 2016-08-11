"""
cache of MGI Users
"""
from mgipython.model import MGIUser, VocTerm
from mgipython.modelconfig import db

def getUsernames():
    
    return _loadUsernames()
    
def _loadUsernames():
    """
    Loads the master list of all usernames
        in MGI
        in format [name,]
    """

    userStatusAlias = db.aliased(VocTerm)
    userTypeAlias = db.aliased(VocTerm)
    
    # get all users
    users = MGIUser.query \
        .join(userTypeAlias, MGIUser.usertype_object) \
        .join(userStatusAlias, MGIUser.userstatus_object) \
        .filter(userTypeAlias.term.in_(['Curator','SE','PI','User Support'])) \
        .filter(userStatusAlias.term=='Active') \
        .order_by(MGIUser.name) \
        .all()
    
    
    return [u.name for u in users]
    