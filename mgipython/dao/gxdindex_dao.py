from mgipython.model import GxdIndexRecord, GxdIndexStage, \
                    Marker, Reference, ReferenceCitationCache

from mgipython.model import db
from base_dao import BaseDAO


class GxdIndexDAO(BaseDAO):
    
    model_class = GxdIndexRecord
    
    def search(self,
               _refs_key=None,
               short_citation=None,
               _marker_key=None,
               _priority_key=None,
               _conditionalmutants_key=None,
               comments=None,
               _createdby_key=None,
               _modifiedby_key=None,
               limit=2000
                ):
        """
        Search MGIUser by fields:
            _refs_key
            _marker_key
            _priority_key
            _conditionalmutants_key
            comments
            _createdby_key
            _modifiedby_key
            
            limit is 2000 by default
        """
        query = GxdIndexRecord.query
                
        # join to Marker for sorting
        query = query.join(GxdIndexRecord.marker)
        
        # join to Reference for sorting
        # also for query
        query = query.join(GxdIndexRecord.reference)
        
        if _refs_key:
            query = query.filter(GxdIndexRecord._refs_key==_refs_key)
            
        if short_citation:
            short_citation = short_citation.lower()
            
            query = query.join(Reference.citation_cache)
            query = query.filter(
                db.func.lower(ReferenceCitationCache.short_citation).like(short_citation)
            )
            
        if _marker_key:
            query = query.filter(GxdIndexRecord._marker_key==_marker_key)
            
        if _priority_key:
            query = query.filter(GxdIndexRecord._priority_key==_priority_key)
            
        if comments:
            comments = comments.lower()
            query = query.filter(db.func.lower(GxdIndexRecord.comments).like(comments))
            
        if _conditionalmutants_key:
            query = query.filter(GxdIndexRecord._conditionalmutants_key==_conditionalmutants_key)
            
            
        if _createdby_key:
            query = query.filter(GxdIndexRecord._createdby_key==_createdby_key)
        if _modifiedby_key:
            query = query.filter(GxdIndexRecord._modifiedby_key==_modifiedby_key)

        
        
        # eager-load the marker and reference relationships
        query = query.options(db.subqueryload('marker'))
        query = query.options(db.subqueryload('reference'))
        
        
        query = query.order_by(Marker.symbol, Reference.authors)
        
        query = query.limit(limit)
        
        return query.all()
        
        
