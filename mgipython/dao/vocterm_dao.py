from mgipython.model import VocTerm
from mgipython.model import db
from sqlalchemy_dao import SQLAlchemyDAO

class VocTermDAO(SQLAlchemyDAO):
    
    model_class = VocTerm
    
    def search(self,
               _vocab_key=None
                ):
        """
        Search VocTerm by fields:
            _vocab_key
        """
        query = VocTerm.query
        
        if _vocab_key:
            query = query.filter(VocTerm._vocab_key==_vocab_key)
            
        
        query = query.order_by(VocTerm.term)
        
        return query.all()
    
        
