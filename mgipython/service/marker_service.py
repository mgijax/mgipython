from mgipython.dao.marker_dao import MarkerDAO
from mgipython.model import Marker
from mgipython.model.query import batchLoadAttributeExists
from mgipython.error import NotFoundError
from mgipython.modelconfig import cache
from mgipython.domain.marker_domains import SmallMarker
from mgipython.domain import convert_models
from mgipython.service_schema.search import SearchQuery

class MarkerService():
    
    marker_dao = MarkerDAO()
    
    def get_by_key(self, _refs_key):
        marker = self.marker_dao.get_by_key(_marker_key)
        if not marker:
            raise NotFoundError("No Marker for _marker_key=%d" % _marker_key)
    
        return marker
    
    
    def get_valid_markers_by_symbol(self, symbol):
        """
        Retrieve list of valid markers by symbol
        """
        search_query = SearchQuery()
        search_query.set_param('symbol', symbol)
        # restrict to official and withdrawn
        search_query.set_param('_marker_status_keys', [1,2])
        
        # only search mouse
        search_query.set_param('_organism_keys', [1])
        
        search_results = self.marker_dao.search(search_query)
        
        # convert db models to domain objects
        search_results.items = convert_models(search_results.items, SmallMarker)
        
        return search_results
  
  



