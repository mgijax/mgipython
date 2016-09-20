from mgipython.dao.gxdindex_dao import GxdIndexDAO
from mgipython.model import GxdIndexRecord, GxdIndexStage
from mgipython.model.query import batchLoadAttribute
from mgipython.error import NotFoundError, ValidationError
from mgipython.modelconfig import cache
from mgipython.domain import convert_models
from mgipython.domain.gxdindex_domains import IndexRecordDomain, IndexRecordSearchResultDomain
from mgipython.service_schema.search import SearchQuery
from vocterm_service import VocTermService
import logging

logger = logging.getLogger("mgipython.service")

class GxdIndexService():
    
    gxdindex_dao = GxdIndexDAO()
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
        self.validate_input(indexrecord_domain)
        
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
        
        if indexrecord_domain.indexstages:
            
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
        
        self.validate_input(indexrecord_domain)
        
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
        
        
    def validate_input(self, indexrecord_domain):
        """
        Validate incoming IndexRecordDomain object
        
        throws ValidationError if not valid to save
        """
        if not indexrecord_domain._refs_key:
            raise ValidationError("Please select a Reference")
        
        if not indexrecord_domain._marker_key:
            raise ValidationError("Please select a Marker")
        
	#
	# note: 'null' priority, conditionalmutatnt will be handled by database trigger
	#
        #if not indexrecord_domain._priority_key:
        #    raise ValidationError("Please select a Priority value")

        #if not indexrecord_domain._conditionalmutants_key:
            
        #    logger.info("_conditionalmutants_key not set. Using 'Not Applicable'")
            # set default value of 'Not Applicable'
        #    not_applicable = self._get_not_applicable_term()
        #    indexrecord_domain._conditionalmutants_key = not_applicable._term_key

        return indexrecord_domain
        
    
    @cache.memoize()
    def _get_not_applicable_term(self):
        """
        Retrieve the Conditional Mutants value
            'Not Applicable'
        """
        search_query = SearchQuery()
        search_query.set_params({
            'vocab_name': 'GXD Conditional Mutants',
            'term': 'Not Applicable'
        })
        results = self.vocterm_service.search(search_query)
        return results.items[0]
    
        
        
