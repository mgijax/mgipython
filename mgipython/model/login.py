#
# Module for handling database logins
#

from pam import pam
from mgd.mgi import MGIUser


def unixUserLogin(userName, password):
    """
    returns if unix user can login, using unix login
    If successful, returns MGIUser object from database
    """
    
    user = None
    
    # authenticate using Python-PAM
    authenticated = pam().authenticate(userName, password)
    
    if authenticated:
        
        # now look up user in database
        user = MGIUser.query.filter_by(login=userName).first()
        
    return user
    
