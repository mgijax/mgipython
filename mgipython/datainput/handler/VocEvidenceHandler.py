"""
    Handles VocEvidence input files
"""

from Handler import Handler, ColumnDef
from mgipython.model import VocEvidence

class VocEvidenceHandler(Handler):
    
    DATA_TYPE = "VocEvidence"
    
    MODEL = VocEvidence
    
    COLUMNS = [ColumnDef(VocEvidence._annotevidence_key, updatable=False),
               ColumnDef(VocEvidence._annot_key),
               ColumnDef(VocEvidence._refs_key),
               ColumnDef(VocEvidence._evidenceterm_key),
               ColumnDef(VocEvidence._modifiedby_key)]
    
    UNIQUE_KEYS = [
        ('_annotevidence_key'),
        ('_annot_key', '_refs_key', '_evidenceterm_key'),
    ]
        