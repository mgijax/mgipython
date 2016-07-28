"""
  mgipython exceptions
"""

class NotFoundError(Exception):
    """
    Thrown when a requested database object is not found
    """

class InvalidPermissionError(Exception):
    """
    Thrown when user does not have permission to perform an operation
    or to access a resource
    """    

    
    
### EMAPA  Browser ###
class InvalidStageInputError(SyntaxError):
    """
    Raised on invalid theiler stage input
    """

class InvalidEMAPAIDError(SyntaxError):
    """
    Raised on invalid EMAPA ID input
    """
    