from mgipython.dao.gxdindex_dao import GxdResultDAO
from mgipython.model.query import batchLoadAttribute
from mgipython.domain import convert_models
from mgipython.service_schema.search import SearchQuery
import logging

logger = logging.getLogger("mgipython.service")

class GxdResultService():
    
    gxdresult_dao = GxdResultDAO()
    
    def search(self, search_query):
        """
        Search using a SearchQuery
        """
        search_results = self.gxdindex_dao.search(search_query)
        
        results = search_results.items
        
        batchLoadAttribute(results, 'marker')
        batchLoadAttribute(results, 'structure')
        batchLoadAttribute(results, 'reference')
        batchLoadAttribute(results, 'assay')
        batchLoadAttribute(results, 'genotype')
        batchLoadAttribute(results, 'specimen')
    
        return search_results
    
    
    def get_search_count(self, search_query):
        """
        Search using a SearchQuery
        return only count of results
        """
        count = self.gxdindex_dao.get_search_count(search_query)
        
        return count
    
    
    