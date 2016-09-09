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
    
    
    def get_total_count(self):
        return self.gxdindex_dao.get_total_count()
    
    
    def search(self, search_query):
        """
        Search using a SearchQuery
        """
        search_results = self.gxdindex_dao.search(search_query)
        
        # load data to be displayed
        gxdindex_records = search_results.items
        
        # convert results to gxd index domain objects
        search_results.items = convert_models(gxdindex_records, IndexRecordSearchResultDomain)
        
        return search_results
    
    
        
    def create(self, indexrecord_domain, current_user):
        """
        Create GxdIndexRecord with an argument object
        """
        gxdindex_record = GxdIndexRecord()
        # get the next primary key
        gxdindex_record._index_key = self.gxdindex_dao.get_next_key()
        # set GxdIndexRecord values
        gxdindex_record._refs_key = indexrecord_domain._refs_key
        gxdindex_record._marker_key = indexrecord_domain._marker_key
        gxdindex_record._priority_key = indexrecord_domain._priority_key
        gxdindex_record._conditionalmutants_key = indexrecord_domain._conditionalmutants_key
        gxdindex_record.comments = indexrecord_domain.comments
        gxdindex_record._createdby_key = current_user._user_key
        gxdindex_record._modifiedby_key = current_user._user_key
        
        # add the GxdIndexStage(s)
        gxdindex_record.indexstages = []
        for indexstage_input in indexrecord_domain.indexstages:
            
            indexstage = GxdIndexStage()
            indexstage._index_key = gxdindex_record._index_key
            indexstage._indexassay_key = indexstage_input._indexassay_key
            indexstage._stageid_key = indexstage_input._stageid_key
            indexstage._createdby_key = current_user._user_key
            indexstage._modifiedby_key = current_user._user_key
            
            gxdindex_record.indexstages.append(indexstage)
        
        self.gxdindex_dao.save(gxdindex_record)
        
        return convert_models(gxdindex_record, IndexRecordDomain)
        
        
    def update(self, key, indexrecord_domain, current_user):
        """
        Update GxdIndexRecord with and argument object
        """
        gxdindex_record = self.gxdindex_dao.get_by_key(key)
        if not gxdindex_record:
            raise NotFoundError("No GxdIndexRecord for _index_key=%d" % key)
        
        # set GxdIndexRecord values
        gxdindex_record._refs_key = indexrecord_domain._refs_key
        gxdindex_record._marker_key = indexrecord_domain._marker_key
        gxdindex_record._priority_key = indexrecord_domain._priority_key
        gxdindex_record._conditionalmutants_key = indexrecord_domain._conditionalmutants_key
        gxdindex_record.comments = indexrecord_domain.comments
        gxdindex_record._modifiedby_key = current_user._user_key
        
        gxdindex_record.indexstages = []
        for indexstage_input in indexrecord_domain.indexstages:
            
            indexstage = GxdIndexStage()
            indexstage._index_key = gxdindex_record._index_key
            indexstage._indexassay_key = indexstage_input._indexassay_key
            indexstage._stageid_key = indexstage_input._stageid_key
            indexstage._createdby_key = current_user._user_key
            indexstage._modifiedby_key = current_user._user_key
            
            gxdindex_record.indexstages.append(indexstage)
        
        self.gxdindex_dao.save()
        return convert_models(gxdindex_record, IndexRecordDomain)
        
        
    def delete(self, _index_key):
        """
        Delete GxdIndexRecord object
        """
        gxdindex_record = self.gxdindex_dao.get_by_key(_index_key)
        if not gxdindex_record:
            raise NotFoundError("No GxdIndexRecord for _index_key=%d" % _index_Key)
        
        logger.debug("nulling out createdby fields")
        self.gxdindex_dao.delete(gxdindex_record)
        
        
    @cache.memoize()
    def get_conditionalmutants_choices(self):
        """
        Get all possible conditionalmutants choices
        """
        conditionalmutants_vocab_key = 74
        return self.vocterm_service \
            .get_term_choices_by_vocab_key(GxdIndexRecord._conditionalmutants_vocab_key)
            
    
    @cache.memoize()
    def get_indexassay_choices(self):
        """
        Get all possible indexassay choices
        """
        return self.vocterm_service \
            .get_term_choices_by_vocab_key(GxdIndexStage._indexassay_vocab_key)
            
    
    @cache.memoize()
    def get_priority_choices(self):
        """
        Get all possible priority choices
        """
        return self.vocterm_service \
            .get_term_choices_by_vocab_key(GxdIndexRecord._priority_vocab_key)
            
            
    @cache.memoize()
    def get_stageid_choices(self):
        """
        Get all possible stageid choices
        """
        return self.vocterm_service \
            .get_term_choices_by_vocab_key(GxdIndexStage._stageid_vocab_key)
    
    
    
        
        