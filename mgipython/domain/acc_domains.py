from base_serializer import Field, Serializer
import logging

logger = logging.getLogger("mgipython.domain")

class AccessionDomain(Serializer):
    """
    Represents a choice in a vocabulary select list
    """    
    __fields__ = [
      Field("_accession_key"),
      Field("accid")
    ]
 
