"""
reference related domain objects
"""
from base_serializer import Field, Serializer
import logging

logger = logging.getLogger("mgipython.domain")


class SmallReference(Serializer):
    """
    Represents a simplified reference object to display in search results
    and to populate dynamic forms
    """    
    __fields__ = [
      Field("_refs_key"),
      Field("jnumid"),
      Field("short_citation")
    ]
    
    