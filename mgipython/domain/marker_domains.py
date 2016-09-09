"""
Marker related domain objects
"""
from base_serializer import Field, Serializer
import logging

logger = logging.getLogger("mgipython.domain")


class SmallMarker(Serializer):
    """
    Represents a simplified marker object to display in search results
    and to populate dynamic forms
    """    
    __fields__ = [
      Field("_marker_key"),
      Field("_marker_status_key"),
      Field("markerstatus"),
      Field("markertype"),
      Field("chromosome"),
      Field("cytogeneticoffset"),
      Field("mgiid"),
      Field("name"),
      Field("symbol"),
      
      # computed fields
      
      Field("current_symbols"),
      Field("featuretypes")
    ]
    
    def get_current_symbols(self, marker):
        current_markers = []
        
        if marker.markerstatus == 'withdrawn':
            current_markers = marker.current_markers
            
        return [m.symbol for m in current_markers]
    
    def get_featuretypes(self, marker):
        terms = marker.featuretype_vocterms
        return [t.term for t in terms]
    