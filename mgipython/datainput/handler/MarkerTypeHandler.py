"""
    Handles MarkerType input files
"""

from Handler import Handler, ColumnDef
from mgipython.model import MarkerType

class MarkerTypeHandler(Handler):
    
    DATA_TYPE = "MarkerType"
    
    MODEL = MarkerType
    
    COLUMNS = [ColumnDef(MarkerType._marker_type_key, updatable=False),
               ColumnDef(MarkerType.name)]
    
    UNIQUE_KEYS = [
        ('_marker_type_key'),
        ('name'),
    ]
        