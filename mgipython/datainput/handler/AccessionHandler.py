"""
    Handles Accession input files
"""

from Handler import Handler, ColumnDef
from mgipython.model import Accession

class AccessionHandler(Handler):
    
    DATA_TYPE = "Accession"
    
    MODEL = Accession
    
    COLUMNS = [ColumnDef(Accession._accession_key, updatable=False),
               ColumnDef(Accession.accid),
               ColumnDef(Accession.prefixpart),
               ColumnDef(Accession.numericpart),
               ColumnDef(Accession._object_key),
               ColumnDef(Accession._mgitype_key),
               ColumnDef(Accession._logicaldb_key),
               ColumnDef(Accession.private),
               ColumnDef(Accession.preferred),
               ColumnDef(Accession._createdby_key),
               ColumnDef(Accession._modifiedby_key)]
    
    UNIQUE_KEYS = [
        ('_accession_key'),
        ('accid', '_object_key', '_mgitype_key', '_logicaldb_key'),
    ]
        