from mgipython.model import db
import logging

logger = logging.getLogger('mgipython.dao')

class SQLAlchemyDAO():
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
    
    
    def save(self, object=None):
        """
        Save object to the database
        flushes database changes
        """
        if object:
            db.session.add(object)
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
    
    