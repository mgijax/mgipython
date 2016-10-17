from mgipython.dao.mgitype_dao import MGITypeDAO
from mgipython.error import NotFoundError
from mgipython.modelconfig import cache
from mgipython.model.query import batchLoadAttribute
from mgipython.service_schema.search import SearchQuery
from mgipython.domain.acc_domains import MGITypeDomain
from mgipython.domain import convert_models
import logging

logger = logging.getLogger('mgipython.service')

class MGITypeService():
    
    mgitype_dao = MGITypeDAO()
    
    def get_by_key(self, _term_key):
        term = self.mgitype_dao.get_by_key(_term_key)
        if not term:
            raise NotFoundError("No MGIType for _mgitype_key=%d" % _term_key)
        return term
    
    def search(self, search_query):
        
        search_result = self.mgitype_dao.search(search_query)
        
        # convert results to domain objects
        search_result.items = convert_models(search_result.items, MGITypeDomain)
        
        return search_result
