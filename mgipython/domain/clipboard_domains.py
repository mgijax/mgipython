from base_serializer import Field, Serializer


class EMAPAClipboardItem(Serializer):
    
    __fields__ = [
        Field("_setmember_key"),
        Field("emapa_term"),
        Field("emapa_stage_key")
    ]
    
    def get_emapa_term(self, item):
        return item.emapa_term.term
        
    def get_emapa_stage_key(self, item):
        return item.emapa._stage_key



