from mgipython.model import Accession, Synonym, Vocab, VocTerm, VocTermEMAPA, VocTermEMAPS
from mgipython.model import db
from mgipython.parse import emapaStageParser, splitSemicolonInput
from base_dao import BaseDAO

class VocVocabDAO(BaseDAO):
 
    model_class = Vocab

    def _build_search_query(self, search_query):

        query = Vocab.query
        
        if search_query.has_valid_param("name"):
            query = query.filter(Vocab.name==search_query.get_value("name"))

        query = query.order_by(Vocab.name)

        return query

