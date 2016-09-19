from mgipython.model import db
from mgipython.service_schema.search import SearchResults
import logging

logger = logging.getLogger('mgipython.dao')

class BaseDAO():
    """
    Base class for all DAOs
    """
    
    # All sub classes must set model_class
    model_class = None
    
    def get_by_key(self, key, model_class=None):
        """
        Return object by primary key
        
        NOTE: Only supports DAOs with a single primary key
            NotImplementedError is thrown for more complex DAOs
            
        uses self.model_class by default
        """
        if not model_class:
            model_class = self.model_class
            
        return self._get_by_key(key, model_class)
    
    def _get_by_key(self, key, model_class):
        
        # Reflect the correct primary key column for the current model_class
        pkNames = [pk.key for pk in model_class.__mapper__.primary_key]
        
        if len(pkNames) > 1:
            raise NotImplementedError("%s object does not have a single primary key. Found keys: %s" 
                                      % (model_class, pkNames)
            )
            
        pkName = pkNames[0]
        return model_class.query.filter(getattr(model_class, pkName)==key).first()
    
    
    def get_total_count(self):
        """
        Retrieve total count of the model_class table
        """
        return self.model_class.query.count()
    
    def create(self, object=None):
        """
        Creates new object in the database
        and flushes database changes
        """
        if object:
            db.session.add(object)
        db.session.flush()
    
    def update(self, object=None):
        """
        Update all modified sqa objects to the database
        by flushing database changes
        """
        if object:
            db.session.flush()
        
    def save_all(self, objects=[]):
        """
        Save list of objects to the database
        flushes database changes
        """
        if objects:
            logger.debug('calling save_all on objects: %s' % objects)
            db.session.add_all(objects)
        db.session.flush()
    
    def delete(self, object):
        """
        Delete object from the database
        flushes database changes
        """
        db.session.delete(object)
        db.session.flush()
        
    
    def get_next_key(self, model_class=None):
        """
        Return next primary key value for the model_class
        Uses self.model_class by default
        """
        if not model_class:
            model_class = self.model_class
            
        return self._get_next_key(model_class)
        
    def _get_next_key(self, model_class):
         # Reflect the correct primary key column for the current model_class
        pkNames = [pk.key for pk in model_class.__mapper__.primary_key]
        
        if len(pkNames) > 1:
            raise NotImplementedError("%s object does not have a single primary key. Found keys: %s" 
                                      % (model_class, pkNames)
            )
            
        pkName = pkNames[0]
        
        next_key = db.session.query(db.func.max(getattr(model_class, pkName)).label("max_key")) \
                .one().max_key + 1
        return next_key
    
    
    def search(self, search_query):
        """
        Take SearchQuery, 
            build query,
            runs query
        Return SearchResults
        """
        sqa_query = self._build_search_query(search_query)
        search_results = self._run_query_or_paginate(search_query, sqa_query)
        return search_results
    
    
    def _build_search_query(self, search_query):
        """
        Method to override for building SQLAlchemy query
        must return an SQLALchemy query
        """
        raise NotImplementedError("_build_search_query must be implemented in DAO subclass")
        
        
    def _run_query_or_paginate(self, search_query, sqa_query):
        """
        Run the given query object or call paginate based
            on given search_query object
            
        search_query is SearchQuery object
        sqa_query is SQLAlchemy query object
        
        return SearchResults object
        """
        if search_query.paginator and search_query.paginator.page_size:
            search_results = self._run_paginated_query(
                sqa_query, search_query.paginator
            )
        else:
            search_results = self._run_query(sqa_query)
            
        return search_results
    
    
    def _run_paginated_query(self, sqa_query, paginator):
        """
        run SQLAlchemy query.paginate(),
        return SearchResults
        set paginator on SearchResults
        """
        search_results = SearchResults()
        logger.debug("running paginated query, page_num=%s, page_size=%s" \
                     % (paginator.page_num, paginator.page_size))
        pagination = sqa_query.paginate(
                paginator.page_num,
                paginator.page_size,
                False
        )
        search_results.items = pagination.items
        search_results.total_count = pagination.total
        search_results.paginator = paginator
        
        return search_results
        
    def _run_query(self, sqa_query):
        """
        run SQLAlachemy query, 
        return SearchResults
        """
        search_results = SearchResults()
        search_results.items = sqa_query.all()
        search_results.total_count = len(search_results.items)
        return search_results
    
    
    
