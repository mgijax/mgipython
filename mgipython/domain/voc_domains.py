from base_serializer import Field, Serializer
import logging

logger = logging.getLogger("mgipython.domain")

class VocTermDomain(Serializer):
    """
    Represents a choice in a vocabulary select list
    """    
    __fields__ = [
      Field("_term_key"),
      Field("abbreviation"),
      Field("term")
    ]
