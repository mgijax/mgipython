from mgipython.model import GxdIndexRecord, GxdIndexStage, \
                    Marker, Reference, ReferenceCitationCache, \
                    Result

from mgipython.model import db
from base_dao import BaseDAO
import logging

logger = logging.getLogger('mgipython.dao')


class GxdIndexDAO(BaseDAO):
    
    model_class = GxdIndexRecord
    
    def _build_search_query(self, search_query):
        """
        Search GXDIndexRecord by fields:
            _refs_key
            _marker_key
            _priority_key
            _conditionalmutants_key
            comments
            _modifiedby_key
            _modifiedby_key
        """
        query = GxdIndexRecord.query
                
        # join to Marker for sorting
        query = query.join(GxdIndexRecord.marker)
        
        # join to Reference for sorting
        # also for query
        query = query.join(GxdIndexRecord.reference)
        
        if search_query.has_valid_param('_refs_key'):
            _refs_key = search_query.get_value('_refs_key')
            query = query.filter(GxdIndexRecord._refs_key==_refs_key)
            
        if search_query.has_valid_param('short_citation'):
            short_citation = search_query.get_value('short_citation')
            short_citation = short_citation.lower()
            
            query = query.join(Reference.citation_cache)
            query = query.filter(
                db.func.lower(ReferenceCitationCache.short_citation).like(short_citation)
            )
            
        if search_query.has_valid_param('_marker_key'):
            _marker_key = search_query.get_value('_marker_key')
            query = query.filter(GxdIndexRecord._marker_key==_marker_key)
            
        if search_query.has_valid_param('_priority_key'):
            _priority_key = search_query.get_value('_priority_key')
            query = query.filter(GxdIndexRecord._priority_key==_priority_key)
            
        if search_query.has_valid_param('comments'):
            comments = search_query.get_value('comments')
            comments = comments.lower()
            query = query.filter(db.func.lower(GxdIndexRecord.comments).like(comments))
            
            
        if search_query.has_valid_param('is_coded'):
            is_coded = search_query.get_value('is_coded')
            
            logger.debug("is_coded = %s" % is_coded)
            logger.debug("params = %s" % search_query._params)
            query = query.filter(GxdIndexRecord.fully_coded==is_coded)
            
            
        if search_query.has_valid_param('_conditionalmutants_key'):
            _conditional_mutants_key = search_query.get_value('_conditionalmutants_key')
            query = query.filter(GxdIndexRecord._conditionalmutants_key==_conditionalmutants_key)
            
            
        if search_query.has_valid_param('_modifiedby_key'):
            _modifiedby_key = search_query.get_value('_modifiedby_key')
            query = query.filter(GxdIndexRecord._modifiedby_key==_modifiedby_key)
        
        if search_query.has_valid_param('_modifiedby_key'):
            _modifiedby_key = search_query.get_value('_modifiedby_key')
            query = query.filter(GxdIndexRecord._modifiedby_key==_modifiedby_key)

        
        
        # eager-load the marker and reference relationships
        query = query.options(db.subqueryload('marker'))
        query = query.options(db.subqueryload('reference'))
        
        
        query = query.order_by(Marker.symbol, Reference.authors)
        
        return query
        
        
