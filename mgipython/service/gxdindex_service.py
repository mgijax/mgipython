from mgipython.dao.gxdindex_dao import GxdIndexDAO
from mgipython.dao.vocterm_dao import VocTermDAO
from mgipython.model import GxdIndexRecord
from mgipython.model.query import batchLoadAttribute
from mgipython.error import NotFoundError
from mgipython.modelconfig import cache
from vocterm_service import VocTermService

class GxdIndexService():
    
    gxdindex_dao = GxdIndexDAO()
    vocterm_dao = VocTermDAO()
    vocterm_service = VocTermService()
    
    def get_by_key(self, _index_key):
        gxdindex_record = self.gxdindex_dao.get_by_key(_index_key)
        if not gxdindex_record:
            raise NotFoundError("No GxdIndexRecord for _index_key=%d" % _index_key)
    
        return gxdindex_record
    
    
    def search(self, args):
        """
        Search using an argument object
        """
        index_records = self.gxdindex_dao.search(
            _refs_key=args._refs_key,
            short_citation=args.short_citation,
            _marker_key=args._marker_key,
            _priority_key=args._priority_key,
            _conditionalmutants_key=args._conditionalmutants_key,
            comments=args.comments,
            _createdby_key=args._createdby_key,
            _modifiedby_key=args._modifiedby_key
        )
        
        return index_records
    
    
        
    def create(self, args, current_user):
        """
        Create GxdIndexRecord with an argument object
        """
        gxdindex_record = GxdIndexRecord()
        # get the next primary key
        gxdindex_record._index_key = self.gxdindex_dao.get_next_key()
        # set GxdIndexRecord values
        gxdindex_record._refs_key = args._refs_key
        gxdindex_record._marker_key = args._marker_key
        gxdindex_record._priority_key = args._priority_key
        gxdindex_record._conditionalmutants_key = args._conditionalmutants_key
        gxdindex_record.comments = args.comments
        gxdindex_record._createdby_key = current_user._user_key
        gxdindex_record._modifiedby_key = current_user._user_key
        
        self.gxdindex_dao.save(gxdindex_record)
        
        return gxdindex_record
        
        
    def edit(self, key, args, current_user):
        """
        Edit GxdIndexRecord with and argument object
        """
        gxdindex_record = self.gxdindex_dao.get_by_key(key)
        if not gxdindex_record:
            raise NotFoundError("No GxdIndexRecord for _index_key=%d" % key)
        gxdindex_record._refs_key = args._refs_key
        gxdindex_record._marker_key = args._marker_key
        gxdindex_record._priority_key = args._priority_key
        gxdindex_record._conditionalmutants_key = args._conditionalmutants_key
        gxdindex_record.comments = args.comments
        
        gxdindex_record._modifiedby_key = current_user._modifiedby_key
        
        self.gxdindex_dao.save()
        return gxdindex_record
        
        
    def delete(self, _index_key):
        """
        Delete GxdIndexRecord object
        """
        gxdindex_record = self.gxdindex_dao.get_by_key(_index_key)
        if not gxdindex_record:
            raise NotFoundError("No GxdIndexRecord for _index_key=%d" % _index_Key)
        self.gxdindex_dao.delete(gxdindex_record)
        
    
    @cache.memoize()
    def get_priority_choices(self):
        """
        Get all possible priority choices
        return format is
        { 'choices': [{'term', '_term_key'}] }
        """
        priority_vocab_key = 11
        return self.vocterm_service \
            .get_term_choices_by_vocab_key(priority_vocab_key)
    
    
    @cache.memoize()
    def get_conditionalmutants_choices(self):
        """
        Get all possible conditionalmutants choices
        return format is
        { 'choices': [{'term', '_term_key'}] }
        """
        conditionalmutants_vocab_key = 74
        return self.vocterm_service \
            .get_term_choices_by_vocab_key(conditionalmutants_vocab_key)
        
        