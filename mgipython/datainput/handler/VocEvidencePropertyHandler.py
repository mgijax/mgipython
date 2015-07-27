"""
    Handles VocEvidenceProperty input files
"""

from Handler import Handler, ColumnDef
from mgipython.model import VocEvidenceProperty

class VocEvidencePropertyHandler(Handler):
    
    DATA_TYPE = "VocEvidenceProperty"
    
    MODEL = VocEvidenceProperty
    
    COLUMNS = [ColumnDef(VocEvidenceProperty._evidenceproperty_key, updatable=False),
               ColumnDef(VocEvidenceProperty._annotevidence_key),
               ColumnDef(VocEvidenceProperty._propertyterm_key),
               ColumnDef(VocEvidenceProperty.value),
               ColumnDef(VocEvidenceProperty.stanza, default=1),
               ColumnDef(VocEvidenceProperty.sequencenum, default=1),
               ColumnDef(VocEvidenceProperty._modifiedby_key)]
    
    UNIQUE_KEYS = [
        ('_evidenceproperty_key'),
        ('_annotevidence_key', '_propertyterm_key','stanza','sequencenum'),
    ]
        