from mgipython.dao.actualdb_dao import ActualDbDAO
from mgipython.error import NotFoundError
from mgipython.modelconfig import cache
from mgipython.model.query import batchLoadAttribute
from mgipython.service_schema.search import SearchQuery
from mgipython.domain.acc_domains import ActualDbDomain
from mgipython.domain import convert_models
import logging

logger = logging.getLogger('mgipython.service')

class ActualDbService():
    
    actualdb_dao = ActualDbDAO()
    
    def search(self, search_query):
        
        search_result = self.actualdb_dao.search(search_query)
        
        # convert results to domain objects
        search_result.items = convert_models(search_result.items, ActualDbDomain)
        
        return search_result

