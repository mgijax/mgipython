"""
    Handles VocTerm input files
"""

from Handler import Handler, ColumnDef
from mgipython.model import VocTerm, Vocab

class VocTermHandler(Handler):
    
    DATA_TYPE = "VocTerm"
    
    MODEL = VocTerm
    
    COLUMNS = [ColumnDef(VocTerm._term_key, updatable=False),
               ColumnDef(VocTerm.term),
               ColumnDef(VocTerm.primaryid, updatable=False),
               ColumnDef(VocTerm._vocab_key, updatable=False),
               ColumnDef(VocTerm.vocabname, updatable=False, 
                         foreignColumn=VocTerm._vocab_key,
                         foreignInsert=Vocab._vocab_key,
                         foreignMapping=Vocab.name
               ),
               ColumnDef(VocTerm.isobsolete),
               ColumnDef(VocTerm._createdby_key),
               ColumnDef(VocTerm._modifiedby_key),
               ColumnDef(VocTerm.modification_date)]
    
    UNIQUE_KEYS = [
        ('_term_key'),
        ('term', '_vocab_key'),
        ('term', 'vocabname'),
        ('primaryid'),
    ]
        