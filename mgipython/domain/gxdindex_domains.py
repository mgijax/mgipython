"""
gxdindex related domain objects
"""
from base_serializer import Field, Serializer
import logging

logger = logging.getLogger("mgipython.domain")

class IndexStageDomain(Serializer):
    
    __fields__ = [
      Field("_indexassay_key"),
      Field("_stageid_key")
    
    ]

class IndexRecordDomain(Serializer):
    
    __fields__ = [
      Field("_index_key"),
      Field("_refs_key"),
      Field("_marker_key"),
      Field("_priority_key"),
      Field("_conditionalmutants_key"),
      Field("comments"),
      Field("is_coded"),
      Field("_createdby_key"),
      Field("createdby_login"),
      Field("creation_date"),
      Field("_modifiedby_key"),
      Field("modifiedby_login"),
      Field("modification_date"),
      
      Field("indexstages", conversion_class=IndexStageDomain),
      
      # display only
      Field("jnumid"),
      Field("short_citation"),
      Field("marker_symbol")
    ]
    
    def get_is_coded(self, record):
        return record.fully_coded
    
    def get_jnumid(self, record):
        return record.reference.jnumid
    
    def get_short_citation(self, record):
        return record.reference.short_citation
    
    def get_marker_symbol(self, record):
        return record.marker.symbol
    
    def get_createdby_login(self, record):
        return record.createdby.login
    
    def get_modifiedby_login(self, record):
        return record.modifiedby.login
    
    
class IndexRecordSearchResultDomain(Serializer):
    """
    gxdindex module search results
    """
    
    __fields__ = [
      Field("_index_key"),
      
      # display only
      Field("jnumid"),
      Field("short_citation"),
      Field("marker_symbol")
    ]
    
    def get_jnumid(self, record):
        return record.reference.jnumid
    
    def get_short_citation(self, record):
        return record.reference.short_citation
    
    def get_marker_symbol(self, record):
        return record.marker.symbol
    
    
    
    