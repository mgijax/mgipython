from mgipython.modelconfig import cache
from mgipython.error import NotFoundError, InvalidStageInputError, InvalidEMAPAIDError
from mgipython.parse import emapaStageParser, splitCommaInput
from mgipython.util.sort import smartAlphaCompare
from mgipython.model.query import batchLoadAttribute
from mgipython.model import SetMember, SetMemberEMAPA
from mgipython.dao.emapa_clipboard_dao import EMAPAClipboardDAO
from mgipython.dao.vocterm_dao import VocTermDAO
from mgipython.domain import convert_models
from mgipython.domain.clipboard_domains import EMAPAClipboardItem

import logging
logger = logging.getLogger('mgipython.service')


class EMAPAClipboardService():
    
    clipboard_dao = EMAPAClipboardDAO()
    vocterm_dao = VocTermDAO()
    
    def get_by_key(self, _user_key):
        user = self.vocterm_dao.get_by_key(_user_key)
        if not user:
            raise NotFoundError("No VocTerm for _user_key=%d" % _user_key)
        return user
    
    
    def get_clipboard_items(self, _user_key):
        result = self.clipboard_dao.get_clipboard_items(_user_key)
        
        # convert to domain object
        result.items = convert_models(result.items, EMAPAClipboardItem)
        
        return result

    
    def add_items(self, _user_key, emapa_id, stages_to_add):
        """
        Parse stages_to_add into list of stages
        
        throws InvalidStageInputError on invalid input
        
        Adds clipboard record for every emapa_id, stage combo
        """
        
        # find vocterm record
        emapa_term = self.vocterm_dao.get_by_primary_id(emapa_id)
        
        if not emapa_term:
            raise InvalidEMAPAIDError("Cannot find term for EMAPA ID: %s" % emapa_id)
        
        
        # parse stage input
        stages = emapaStageParser(stages_to_add)
        
        added_items = []
        
        for stage in stages:
            
            # only add stages valid for this term
            if stage >= emapa_term.emapa_info.startstage \
                and stage <= emapa_term.emapa_info.endstage:
                
                set_member = self.add_item(_user_key, emapa_term._term_key, stage)
                added_items.append(set_member)
                
            else:
                if "*" not in stages_to_add and "all" not in stages_to_add.lower():
                    raise InvalidStageInputError("%s is invalid for range %d-%d for %s(%s)" % \
                            (stage, 
                             emapa_term.emapa_info.startstage,
                             emapa_term.emapa_info.endstage,
                             emapa_term.term,
                             emapa_id)
                    )
        
        
        if added_items:
            # adding a duplicate can cause sequencenums to have gaps
            #    so we normalize them here
            #    This is necessary, because EI requires sequencenums without gaps
            self.clipboard_dao.normalize_sequencenums(_user_key)
            
        return added_items
        
        
    def add_item(self, _user_key, 
                   _term_key, 
                   _stage_key):
        """
        1) Create a single EMAPA clipboard item
        2) Add it to the user's clipboard
        """
        
        # create a new set member
        set_member = SetMember()
        
        ## set columns
        set_member._createdby_key = _user_key
        set_member._modifiedby_key = _user_key
        set_member._set_key = self.clipboard_dao.emapa_clipboard_set_key
        set_member._object_key = _term_key
        
        ## get max key and sequencenum
        set_member._setmember_key = self.clipboard_dao.get_next_key()
            
        set_member.sequencenum = self.clipboard_dao.get_next_sequencenum(_user_key)
        
    
        # create a new set member EMAPA
        set_memberEMAPA = SetMemberEMAPA()
        
        ## set columns
        set_memberEMAPA._stage_key = _stage_key
        set_memberEMAPA._createdby_key = _user_key
        set_memberEMAPA._modifiedby_key = _user_key
        set_memberEMAPA._setmember_key = set_member._setmember_key
        
        ## get max key
        set_memberEMAPA._setmember_emapa_key = self.clipboard_dao.get_next_setmember_emapa_key()
        
        # add EMAPA to set member
        set_member.emapa = set_memberEMAPA
        
        self.clipboard_dao.create(set_member)
        
        return set_member
    
    
    def delete_all_items(self, _user_key):
        """
        Deletes all _setmember_keys,
            for the given _user_key
        """
        
        result = self.get_clipboard_items(_user_key)
        
        
        for setmember in result.items:
            _setmember_key = setmember._setmember_key
            
            self.delete_item(_setmember_key, _user_key=_user_key)
            
        
            
    def delete_item(self, _setmember_key, _user_key=None):
        """
        Deletes an EMAPA clipboard item
        
        Also filters by _user_key if provided
        """
        
        set_member = self.clipboard_dao.get_by_key(_setmember_key)
        if not set_member:
            raise NotFoundError("No SetMember with _setmember_key = %s" % _setmember_key)
        
        if _user_key:
            # We cannot delete a setmember from a different user
            # ignore the command
            if set_member._createdby_key != _user_key:
                return
        
        # perform delete
        set_member._object_key = None
        self.clipboard_dao.delete(set_member)
        
        # HACK (kstone):
        # deleting items can cause gaps in sequencenums. 
        # teluse EI requires no gap in sequencenums, 
        # so we normalize them here
        self.clipboard_dao.normalize_sequencenums(_user_key)
    
    
    def sort_clipboard(self, _user_key):
        """
        Sorts all EMAPA clipboard items
            where _createdby_key == _user_key
            
        Sort is by stage, then alpha on term
        """
            
        result = self.clipboard_dao.get_clipboard_items(_user_key)
        set_members = result.items
            
        batchLoadAttribute(set_members, "emapa")
        batchLoadAttribute(set_members, "emapa_term")
            
        # sort
        self._sort_items_by_alpha(set_members)
        
        self.clipboard_dao.save_all(set_members)
        
        
    # function hook for unit-testing
    def _sort_items_by_alpha(self, set_members):
        """
        Sort clipboard items by alpha
        returns nothing.
        
        Assigns new sequencenum for each item
        """
        
        # define the compare function
        def stage_term_compare(a, b):
            
            if a.emapa._stage_key != b.emapa._stage_key:
                return cmp(a.emapa._stage_key, b.emapa._stage_key)
            
            # user smart alpha for the term
            return smartAlphaCompare(a.emapa_term.term, b.emapa_term.term)
            
        # apply the sort
        set_members.sort(stage_term_compare)
                
        # assign sequencenum
        new_seqnum = 0
        for set_member in set_members:
            
            new_seqnum += 1
            set_member.sequencenum = new_seqnum
                        
            
        
