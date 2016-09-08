from mgipython.dao.vocterm_dao import VocTermDAO
from mgipython.dao.vocvocab_dao import VocVocabDAO
from mgipython.error import NotFoundError
from mgipython.modelconfig import cache
from mgipython.model.query import batchLoadAttribute
from mgipython.service_schema.search import SearchQuery
from mgipython.domain.vocab_domains import VocTermChoiceList
from mgipython.domain.voc_domains import VocTermDomain
import logging

logger = logging.getLogger('mgipython.service')


class VocTermService():
    
    vocterm_dao = VocTermDAO()
    
    def get_by_key(self, _term_key):
        term = self.vocterm_dao.get_by_key(_term_key)
        if not term:
            raise NotFoundError("No VocTerm for _term_key=%d" % _term_key)
        return term
    
    def get_by_primary_id(self, id):
        term = self.vocterm_dao.get_by_primary_id(id)
        if not term:
            raise NotFoundError("No VocTerm with id=%s" % id)
        return term
    
    
    def search(self, search_query):
        if search_query.has_valid_param("vocab_name"):
            vocvocab_dao = VocVocabDAO()
            search_query_vocab = SearchQuery()
            search_query_vocab.set_param("name", search_query.get_value("vocab_name"))
            search_result_vocab = vocvocab_dao.search(search_query_vocab)
            search_query.clear_param("vocab_name")
            search_query.set_param("_vocab_key", search_result_vocab.items[0]._vocab_key)

        search_result = self.vocterm_dao.search(search_query)
        newitems = []
        for item in search_result.items:
            newitem = VocTermDomain()
            newitem.load_from_model(item)
            newitems.append(newitem)
        search_result.items = newitems
        return search_result
    
    def search_emapa_terms(self,
                         termSearch="",
                         stageSearch="",
                         isobsolete=0,
                         limit=None):
        """
        Search specifically for EMAPA vocterm objects
        """
        terms = self.vocterm_dao.search_emapa_terms(
             termSearch=termSearch,
             stageSearch=stageSearch,
             isobsolete=isobsolete,
             limit=limit
        )
        
        # batch load necessary attributes
        batchLoadAttribute(terms, "emapa_info")
        
        return terms

    def get_term_choices_by_vocab_key(self, _vocab_key):
        """
        Get all possible term choices
        for the given _vocab_key
        return format is a VocTermChoiceList object
        """
        search_query = SearchQuery()
        search_query.set_param("_vocab_key", _vocab_key)
        search_result = self.vocterm_dao.search(search_query)
        terms = search_result.items
        
        # convert to choice list
        choice_list = VocTermChoiceList()
        choice_list.load_from_model(terms)
        
        return choice_list
    
    
