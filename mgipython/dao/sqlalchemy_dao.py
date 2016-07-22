from mgipython.model import db

class SQLAlchemyDAO():
    """
    Base class for all DAOs
    """
    
    # All sub classes must set model_class
    model_class = None
    
    def get_by_key(self, key):
        """
        Return object by primary key
        
        NOTE: Only supports DAOs with a single primary key
            NotImplementedError is thrown for more complex DAOs
        """
        
        # Reflect the correct primary key column for the current model_class
        pkNames = [pk.key for pk in self.model_class.__mapper__.primary_key]
        
        if len(pkNames) > 1:
            raise NotImplementedError("%s object does not have a single primary key. Found keys: %s" 
                                      % (self.model_class, pkNames)
            )
            
        pkName = pkNames[0]
        return self.model_class.query.filter(getattr(self.model_class, pkName)).first()
    
    
    def save(self, object):
        """
        Save object to the database
        """
        db.session.add(object)
    
    def delete(self, object):
        """
        Delete object from the database
        """
        db.session.delete(object)
        
    
    def get_next_key(self):
        """
        Return next primary key value for the model_class
        """
         # Reflect the correct primary key column for the current model_class
        pkNames = [pk.key for pk in self.model_class.__mapper__.primary_key]
        
        if len(pkNames) > 1:
            raise NotImplementedError("%s object does not have a single primary key. Found keys: %s" 
                                      % (self.model_class, pkNames)
            )
            
        pkName = pkNames[0]
        
        next_key = db.session.query(db.func.max(getattr(self.model_class, pkName)).label("max_key")) \
                .one().max_key + 1
        return next_key
    
    