"""
    Handles VocAnnot input files
"""

from Handler import Handler, ColumnDef
from mgipython.model import VocAnnot

class VocAnnotHandler(Handler):
    
    DATA_TYPE = "VocAnnot"
    
    MODEL = VocAnnot
    
    COLUMNS = [ColumnDef(VocAnnot._annot_key, updatable=False),
               ColumnDef(VocAnnot._annottype_key),
               ColumnDef(VocAnnot._object_key),
               ColumnDef(VocAnnot._term_key),
               ColumnDef(VocAnnot._qualifier_key),]
    
    UNIQUE_KEYS = [
        ('_annot_key'),
        ('_annottype_key', '_object_key', '_term_key', '_qualifier_key'),
    ]
        