from mgipython.dao.gxdindex_dao import GxdIndexDAO
from mgipython.dao.vocterm_dao import VocTermDAO
from mgipython.model import GxdIndexRecord, GxdIndexStage
from mgipython.model.query import batchLoadAttribute
from mgipython.error import NotFoundError
from mgipython.modelconfig import cache
from mgipython.domain import convert_models
from mgipython.domain.gxdindex_domains import IndexRecordDomain, IndexRecordSearchResultDomain
from vocterm_service import VocTermService
import logging

logger = logging.getLogger("mgipython.service")

class GxdIndexService():
    
    gxdindex_dao = GxdIndexDAO()
    vocterm_dao = VocTermDAO()
    vocterm_service = VocTermService()
    
    def get_by_key(self, _index_key):
        gxdindex_record = self.gxdindex_dao.get_by_key(_index_key)
        if not gxdindex_record:
            raise NotFoundError("No GxdIndexRecord for _index_key=%d" % _index_key)
    
        
        # convert to domain object
        return convert_models(gxdindex_record, IndexRecordDomain)
    
    
    def search(self, search_query):
        """
        Search using a SearchQuery
        """
        search_results = self.gxdindex_dao.search(search_query)
        
        # load data to be displayed
        gxdindex_records = search_results.items
        batchLoadAttribute(gxdindex_records, 'indexstages')
        batchLoadAttribute(gxdindex_records, 'reference')
        batchLoadAttribute(gxdindex_records, 'reference.citation_cache')
        batchLoadAttribute(gxdindex_records, 'marker')
        batchLoadAttribute(gxdindex_records, 'createdby')
        batchLoadAttribute(gxdindex_records, 'modifiedby')
        
        
        # convert results to gxd index domain objects
        search_results.items = convert_models(gxdindex_records, IndexRecordSearchResultDomain)
        
        return search_results
    
    
        
    def create(self, args, current_user):
        """
        Create GxdIndexRecord with an argument object
        """
        gxdindex_record = GxdIndexRecord()
        # get the next primary key
        gxdindex_record._index_key = self.gxdindex_dao.get_next_key()
        # set GxdIndexRecord values
        gxdindex_record._refs_key = args['_refs_key']
        gxdindex_record._marker_key = args['_marker_key']
        gxdindex_record._priority_key = args['_priority_key']
        gxdindex_record._conditionalmutants_key = args['_conditionalmutants_key']
        gxdindex_record.comments = args['comments']
        gxdindex_record._createdby_key = current_user._user_key
        gxdindex_record._modifiedby_key = current_user._user_key
        
        # add the GxdIndexStage(s)
        gxdindex_record.indexstages = []
        for indexstage_input in args['indexstages']:
            
            indexstage = GxdIndexStage()
            indexstage._index_key = gxdindex_record._index_key
            indexstage._indexassay_key = indexstage_input['_indexassay_key']
            indexstage._stageid_key = indexstage_input['_stageid_key']
            indexstage._createdby_key = current_user._user_key
            indexstage._modifiedby_key = current_user._user_key
            
            gxdindex_record.indexstages.append(indexstage)
        
        self.gxdindex_dao.save(gxdindex_record)
        
        return convert_models(gxdindex_record, IndexRecordDomain)
        
        
    def edit(self, key, args, current_user):
        """
        Edit GxdIndexRecord with and argument object
        """
        gxdindex_record = self.gxdindex_dao.get_by_key(key)
        if not gxdindex_record:
            raise NotFoundError("No GxdIndexRecord for _index_key=%d" % key)
        
        # set GxdIndexRecord values
        gxdindex_record._refs_key = args['_refs_key']
        gxdindex_record._marker_key = args['_marker_key']
        gxdindex_record._priority_key = args['_priority_key']
        gxdindex_record._conditionalmutants_key = args['_conditionalmutants_key']
        gxdindex_record.comments = args['comments']
        gxdindex_record._createdby_key = current_user._user_key
        gxdindex_record._modifiedby_key = current_user._user_key
        
        # TODO(kstone:
        # Some magic to determine how to save indexstages
        #   New ones should not have _createdby_key
        #   Pre-existing ones should...
        
        self.gxdindex_dao.save()
        return convert_models(gxdindex_record, IndexRecordDomain)
        
        
    def delete(self, _index_key):
        """
        Delete GxdIndexRecord object
        """
        gxdindex_record = self.gxdindex_dao.get_by_key(_index_key)
        if not gxdindex_record:
            raise NotFoundError("No GxdIndexRecord for _index_key=%d" % _index_Key)
        self.gxdindex_dao.delete(gxdindex_record)
        
        
    @cache.memoize()
    def get_conditionalmutants_choices(self):
        """
        Get all possible conditionalmutants choices
        return format is
        { 'choices': [{'term', '_term_key'}] }
        """
        conditionalmutants_vocab_key = 74
        return self.vocterm_service \
            .get_term_choices_by_vocab_key(GxdIndexRecord._conditionalmutants_vocab_key)
            
    
    @cache.memoize()
    def get_indexassay_choices(self):
        """
        Get all possible indexassay choices
        return format is
        { 'choices': [{'term', '_term_key'}] }
        """
        return self.vocterm_service \
            .get_term_choices_by_vocab_key(GxdIndexStage._indexassay_vocab_key)
            
    
    @cache.memoize()
    def get_priority_choices(self):
        """
        Get all possible priority choices
        return format is
        { 'choices': [{'term', '_term_key'}] }
        """
        return self.vocterm_service \
            .get_term_choices_by_vocab_key(GxdIndexRecord._priority_vocab_key)
            
            
    @cache.memoize()
    def get_stageid_choices(self):
        """
        Get all possible stageid choices
        return format is
        { 'choices': [{'term', '_term_key'}] }
        """
        return self.vocterm_service \
            .get_term_choices_by_vocab_key(GxdIndexStage._stageid_vocab_key)
    
    
    
        
        