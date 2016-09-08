from mgipython.model import Accession, Allele, Marker, Reference
from mgipython.model import db
from mgipython.parse.parser import splitCommaInput
from base_dao import BaseDAO

import logging

logger = logging.getLogger("mgipython.dao")


class MarkerDAO(BaseDAO):
    
    model_class = Reference


    def _build_search_query(self, search_query):
        """
        Search Marker by fields:
            symbol,
            _marker_status_keys,
            _organism_keys
        """
        query = Marker.query
                
        
        if search_query.has_valid_param('symbol'):
            
            symbol = search_query.get_value('symbol')
            symbol = symbol.lower()
            query = query.filter(db.func.lower(Marker.symbol)==symbol)
        
        
        if search_query.has_valid_param('_marker_status_keys'):
            
            # matches any key in the list
            _marker_status_keys = search_query.get_value('_marker_status_keys')
            query = query.filter(Marker._marker_status_key.in_(_marker_status_keys))
        
        
        if search_query.has_valid_param('_organism_keys'):
            
            # matches any key in the list
            _organism_keys = search_query.get_value('_organism_keys')
            query = query.filter(Marker._organism_key.in_(_organism_keys))
        
        
        
        
        query = query.order_by(Marker.symbol)
        
        return query
        
        