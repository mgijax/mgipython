from .base_serializer import Field, Serializer
from mgipython.domain.voc_domains import *

class EMAPAClipboardItem(Serializer):
    
    __fields__ = [
        Field("_setmember_key"),
        Field("emapa_term"),
        Field("emapa_term_key"),
        Field("emapa_stage"),
        Field("emapa_stage_key"),
        Field("emaps_term", conversion_class=VocTermEMAPSDomain),
    ]
    
    def get_emapa_term(self, item):
        return item.emapa_term.term

    def get_emapa_term_key(self, item):
        return item.emapa_term._term_key
        
    def get_emapa_stage_key(self, item):
        return item.emapa._stage_key

    def get_emapa_stage(self, item):
        return item.emapa._stage_key

