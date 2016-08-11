from mgipython.model import GxdIndexRecord, GxdIndexStage, Marker, Reference

from mgipython.model import db
from base_dao import BaseDAO


class GxdIndexDAO(BaseDAO):
    
    model_class = GxdIndexRecord
    
    def search(self,
               _refs_key=None,
               _marker_key=None,
               _priority_key=None,
               _conditionalmutants_key=None,
               comments=None,
               _createdby_key=None,
               _modifiedby_key=None
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
        """
        query = GxdIndexRecord.query
        
        if _refs_key:
            query = query.filter(GxdIndexRecord._refs_key==_refs_key)
            
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
        
        
        # join to Marker for sorting
        query = query.join(GxdIndexRecord.marker)
        
        # join to Reference for sorting
        query = query.join(GxdIndexRecord.reference)
        
        
        # eager-load the marker and reference relationships
        query = query.options(db.subqueryload('marker'))
        query = query.options(db.subqueryload('reference'))
        
        
        query = query.order_by(Marker.symbol, Reference.authors)
        
        return query.all()
        
        
