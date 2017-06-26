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
    
class ReferenceDomain(Serializer):
    """
    Represents a reference object
    """
    __fields__ = [
       Field("_refs_key"),
       Field("jnumid"),
       Field("pubmedid"),
       Field("doiid"),
       Field("title"), 
       Field("short_citation"),
       Field("authors"), 
       Field("primaryAuthor"), 
       Field("journal"), 
       Field("volume"), 
       Field("year"),
       Field("current_workflow_statuses")
    ]
    
class WorkflowStatusDomain(Serializer):
    """
    Represents a status entry for one workflow group for a reference
    """
    __fields__ = [
        Field("_group_key"),
        Field("_status_key"),
        Field("iscurrent"),
        Field("group"),
        Field("groupAbbreviation"),
        Field("status")
    ] 