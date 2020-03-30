#
# Module for handling database logins
#

from pam import pam
from .mgd.mgi import MGIUser
import logging
#from mgipython import logger

logger = logging.getLogger('mgipython.model.login')


def unixUserLogin(userName, password):
    """
    returns if unix user can login, using unix login
    If successful, returns MGIUser object from database
    """
    
    logger.debug('%s - attempting to authenticate' % userName)
    
    user = None
    
    # authenticate using Python-PAM
    authenticated = pam().authenticate(userName, password)
    
    if authenticated:
        
        logger.debug('%s - authentication successful' % userName)
        # now look up user in database
        user = MGIUser.query.filter_by(login=userName).first()
        
        if not user:
            logger.debug('%s - does not exist in MGI_User table' % userName)
        
    return user
    
