from mgipython.model import GxdIndexRecord, GxdIndexStage, \
                    Marker, MGIUser, Reference, ReferenceCitationCache, \
                    Result

from mgipython.model import db
from base_dao import BaseDAO
from mgipython.service.helpers.date_helper import DateHelper
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
        
        hasRefsKeySearch = search_query.has_valid_param('_refs_key')
        if hasRefsKeySearch:
            _refs_key = search_query.get_value('_refs_key')
            query = query.filter(GxdIndexRecord._refs_key==_refs_key)
            
            
        if not hasRefsKeySearch:
            
            # reference-related searches only need to occur if we did not 
            #  also search a specific _Refs_key
            
            if search_query.has_valid_param('short_citation'):
                short_citation = search_query.get_value('short_citation')
                short_citation = short_citation.lower()
                
                query = query.join(Reference.citation_cache)
                query = query.filter(
                    db.func.lower(ReferenceCitationCache.short_citation).like(short_citation)
                )
            
        hasMarkerKeySearch = search_query.has_valid_param('_marker_key')
        if hasMarkerKeySearch:
            _marker_key = search_query.get_value('_marker_key')
            query = query.filter(GxdIndexRecord._marker_key==_marker_key)
            
            
        if not hasMarkerKeySearch:
            
            # marker-related searches only needs to occur if we did not
            #  also search a specific _marker_key
            
            if search_query.has_valid_param('marker_symbol'):
                marker_symbol = search_query.get_value('marker_symbol')
                marker_symbol = marker_symbol.lower()
                
                query = query.filter(
                    db.func.lower(Marker.symbol).like(marker_symbol)
                )
            
        if search_query.has_valid_param('_priority_key'):
            _priority_key = search_query.get_value('_priority_key')
            query = query.filter(GxdIndexRecord._priority_key==_priority_key)
            
        if search_query.has_valid_param('comments'):
            comments = search_query.get_value('comments')
            comments = comments.lower()
            query = query.filter(db.func.lower(GxdIndexRecord.comments).like(comments))
            
            
        if search_query.has_valid_param('is_coded'):
            is_coded = search_query.get_value('is_coded')
            
            query = query.filter(GxdIndexRecord.fully_coded==is_coded)
            
            
        if search_query.has_valid_param('_conditionalmutants_key'):
            _conditionalmutants_key = search_query.get_value('_conditionalmutants_key')
            query = query.filter(GxdIndexRecord._conditionalmutants_key==_conditionalmutants_key)
            
            
        if search_query.has_valid_param('_createdby_key'):
            _createdby_key = search_query.get_value('_createdby_key')
            query = query.filter(GxdIndexRecord._createdby_key==_createdby_key)
            
        if search_query.has_valid_param('createdby_login'):
            login = search_query.get_value('createdby_login')
            login = login.lower()
            createdby_alias = db.aliased(MGIUser)
            query = query.join(createdby_alias, GxdIndexRecord.createdby)
            query = query.filter(db.func.lower(createdby_alias.login).like(login))
        
        if search_query.has_valid_param('_modifiedby_key'):
            _modifiedby_key = search_query.get_value('_modifiedby_key')
            query = query.filter(GxdIndexRecord._modifiedby_key==_modifiedby_key)
            
        if search_query.has_valid_param('modifiedby_login'):
            login = search_query.get_value('modifiedby_login')
            login = login.lower()
            modifiedby_alias = db.aliased(MGIUser)
            query = query.join(modifiedby_alias, GxdIndexRecord.modifiedby)
            query = query.filter(db.func.lower(modifiedby_alias.login).like(login))
            
        if search_query.has_valid_param('creation_date'):
            creation_date = search_query.get_value('creation_date')
            query = DateHelper().build_query_with_date(query, GxdIndexRecord.creation_date, creation_date)

        if search_query.has_valid_param('modification_date'):
            modification_date = search_query.get_value('modification_date')
            query = DateHelper().build_query_with_date(query, GxdIndexRecord.modification_date, modification_date)
            
            
        if search_query.has_valid_param('indexstages'):
            indexstages = search_query.get_value('indexstages')
            
            # AND the stages together
#             logger.debug("Querying indexstages = %s" % indexstages)
#             for indexstage in indexstages:
#                 sub_indexrecord = db.aliased(GxdIndexRecord)
#                 sub_indexstage = db.aliased(GxdIndexStage)
#                 sq = db.session.query(sub_indexrecord)
#                 sq = sq.join(sub_indexstage, sub_indexrecord.indexstages)
#                 sq = sq.filter(sub_indexstage._stageid_key==indexstage['_stageid_key'])
#                 sq = sq.filter(sub_indexstage._indexassay_key==indexstage['_indexassay_key'])
#                 sq = sq.filter(sub_indexrecord._index_key==GxdIndexRecord._index_key)
#                 sq.correlate(GxdIndexRecord)
#                 
#                 query = query.filter(sq.exists())
                
            # OR the stages together
            sqs = []
            for indexstage in indexstages:
                sub_indexrecord = db.aliased(GxdIndexRecord)
                sub_indexstage = db.aliased(GxdIndexStage)
                sq = db.session.query(sub_indexrecord)
                sq = sq.join(sub_indexstage, sub_indexrecord.indexstages)
                sq = sq.filter(sub_indexstage._stageid_key==indexstage['_stageid_key'])
                sq = sq.filter(sub_indexstage._indexassay_key==indexstage['_indexassay_key'])
                sq = sq.filter(sub_indexrecord._index_key==GxdIndexRecord._index_key)
                sq.correlate(GxdIndexRecord)
                
                sqs.append(sq.exists())
                
            query = query.filter(db.or_(*sqs))

        
        
        # eager-load the marker and reference relationships
        query = query.options(db.subqueryload('marker'))
        query = query.options(db.subqueryload('reference'))
        
        
        query = query.order_by(Marker.symbol, Reference.authors)
        
        return query
        
        
