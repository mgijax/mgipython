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
      Field("featuretypes"),
      Field("markerstatus"),
      Field("markertype"),
      Field("chromosome"),
      Field("cytogeneticoffset"),
      Field("mgiid"),
      Field("name"),
      Field("symbol")
    ]
    
    
    def get_featuretypes(self, marker):
        terms = marker.featuretype_vocterms
        return [t.term for t in terms]
    