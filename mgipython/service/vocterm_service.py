from mgipython.dao.vocterm_dao import VocTermDAO
from mgipython.dao.vocvocab_dao import VocVocabDAO
from mgipython.error import NotFoundError
from mgipython.modelconfig import cache
from mgipython.model.query import batchLoadAttribute
from mgipython.service_schema.search import SearchQuery
from mgipython.domain.vocab_domains import VocTermChoiceList
from mgipython.domain.voc_domains import VocTermDomain
from mgipython.domain import convert_models
import logging

logger = logging.getLogger('mgipython.service')


class VocTermService():
    
    vocterm_dao = VocTermDAO()
    
    def get_by_key(self, _term_key):
        term = self.vocterm_dao.get_by_key(_term_key)
        if not term:
            raise NotFoundError("No VocTerm for _term_key=%d" % _term_key)
        return term
    
    def get_by_primary_id(self, id):
        term = self.vocterm_dao.get_by_primary_id(id)
        if not term:
            raise NotFoundError("No VocTerm with id=%s" % id)
        return term
    
    
    
    def search(self, search_query):
        
        search_result = self.vocterm_dao.search(search_query)
        
        # convert results to domain objects
        search_result.items = convert_models(search_result.items, VocTermDomain)
        
        return search_result
    
    
    def search_emapa_terms(self,
                         termSearch="",
                         stageSearch="",
                         isobsolete=0,
                         limit=None):
        """
        Search specifically for EMAPA vocterm objects
        """
        terms = self.vocterm_dao.search_emapa_terms(
             termSearch=termSearch,
             stageSearch=stageSearch,
             isobsolete=isobsolete,
             limit=limit
        )
        
        # batch load necessary attributes
        batchLoadAttribute(terms, "emapa_info")
        
        return terms
    
    
