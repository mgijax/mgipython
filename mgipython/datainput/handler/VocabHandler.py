"""
    Handles Vocab input files
"""

from Handler import Handler, ColumnDef
from mgipython.model import Vocab

class VocabHandler(Handler):
    
    DATA_TYPE = "Vocab"
    
    MODEL = Vocab
    
    COLUMNS = [ColumnDef(Vocab._vocab_key, updatable=False),
               ColumnDef(Vocab.name),
               ColumnDef(Vocab._refs_key, default=-1),
               ColumnDef(Vocab._logicaldb_key, default=-1)]
    
    UNIQUE_KEYS = [
        ('_vocab_key'),
        ('name', '_refs_key', '_logicaldb_key'),
    ]
        