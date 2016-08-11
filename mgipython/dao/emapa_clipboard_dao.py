from mgipython.model import db
from mgipython.model import SetMember, SetMemberEMAPA
from mgipython.model.query import performQuery
from base_dao import BaseDAO


class EMAPAClipboardDAO(BaseDAO):
    """
    Uses both the SetMember and SetMemberEMAPA tables
    which combined represent a single EMAPA clipboard entry
    """
    
    model_class = SetMember
    
    # constant
    emapa_clipboard_set_key = 1046


    def get_next_setmember_emapa_key(self):
        """
        Return next primary key for SetMemberEMAPA object
        """
        return self._get_next_key(SetMemberEMAPA)
    
    
    def get_next_sequencenum(self, _user_key):
        """
        Return next value for sequencenum of SetMember
        For the given user
        """
        next_sequencenum = db.session.query(
                    db.func.max(SetMember.sequencenum)+1) \
                    .filter(SetMember._set_key==self.emapa_clipboard_set_key) \
                    .filter(SetMember._createdby_key==_user_key) \
                    .one()[0] or 1
        return next_sequencenum
        
        
    def get_clipboard_items(self, _user_key):
        """
        Returns all EMAPA clipboard SetMembers for the given user
        """
        items = SetMember.query.filter_by(_set_key=self.emapa_clipboard_set_key) \
            .filter_by(_createdby_key=_user_key) \
            .order_by(SetMember.sequencenum) \
            .all()
        return items
    
        
    def normalize_sequencenums(self, _user_key):
        """
        Normalizes all the sequencenum fields in
        the MGI_SetMember table for EMAPA
        
        This is necessary after you've done any number of 
            adds or deletes, because it can leave holes
            in the sequencenum order 
            e.g [1,2,5,9,10] becomes [1,2,3,4,5]
        """
        
        performQuery("""
            select MGI_resetSequenceNum(
                    'MGI_SetMember',
                    %d,
                    %d
                )
        """ % (self.emapa_clipboard_set_key, _user_key))
        
        
            
