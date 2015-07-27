"""
    Handles AccessionReference input files
"""

from Handler import Handler, ColumnDef
from mgipython.model import AccessionReference

class AccessionReferenceHandler(Handler):
    
    DATA_TYPE = "AccessionReference"
    
    MODEL = AccessionReference
    
    COLUMNS = [ColumnDef(AccessionReference._accession_key, updatable=False),
               ColumnDef(AccessionReference._refs_key, updatable=False)]
    
    UNIQUE_KEYS = [
        ('_accession_key', '_refs_key'),
    ]
        