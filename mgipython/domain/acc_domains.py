from base_serializer import Field, Serializer
from mgipython.domain.mgi_domains import *
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
 
class MGITypeDomain(Serializer):
    __fields__ = [
        Field("_mgitype_key"),
        Field("name"),
        Field("tablename"),
        Field("primarykeyname"),
        Field("identitycolumnname"),
        Field("dbview"),
        Field("organisms", conversion_class=MGIOrganism),
    ]

class ActualDbDomain(Serializer):
    __fields__ = [
        Field("url"),
        Field("name")
    ]
