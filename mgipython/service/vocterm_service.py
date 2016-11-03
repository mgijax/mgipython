from mgipython.dao import *
from mgipython.error import NotFoundError
from mgipython.modelconfig import cache
from mgipython.model.query import batchLoadAttribute, batchLoadAttributeCount
from mgipython.service_schema.search import SearchQuery
from mgipython.domain import *

from mgipython.parse import splitSemicolonInput
from mgipython.parse.highlight import highlightEMAPA

import logging

logger = logging.getLogger('mgipython.service')


class VocTermService():
    
    vocterm_dao = VocTermDAO()
    gxdresult_dao = GxdResultDAO()
    vocterm_emaps_dao = VocTermEMAPSDAO()
    
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
    
    
    def get_emapa_term(self, id):
        term = self.get_by_primary_id(id)
        
        term = convert_models(term, EMAPADetailDomain)
        
        # get results count for structure_id
        term.results_count = self._get_emapa_term_results_count(term.primaryid)
        
        # sort parent_nodes by edge_label, term
        term.parent_nodes.sort(key=lambda x: (x.edge_label, x.term))
        
        return term
    
    def _get_emapa_term_results_count(self, term_id):
        search_query = SearchQuery()
        search_query.set_param("direct_structure_id", term_id)
        count = self.gxdresult_dao.get_search_count(search_query)
        
        return count
    
    
    def search(self, search_query):
        
        search_result = self.vocterm_dao.search(search_query)
        
        # convert results to domain objects
        search_result.items = convert_models(search_result.items, VocTermDomain)

        return search_result

    def search_emaps_terms(self, search_query):
        search_result = self.vocterm_emaps_dao.search(search_query)
        search_result.items = convert_models(search_result.items, VocTermEMAPSDomain)
        return search_result
    
    def search_emapa_terms(self, search_query):
        """
        Search specifically for EMAPA vocterm objects
        """
        
        # don't search obsolete terms by default
        if not search_query.has_valid_param('isobsolete'):
            search_query.set_param('isobsolete', 0)
            
        search_query.set_param('vocab_name', 'EMAPA')
        
        search_result = self.vocterm_dao.search(search_query)
        
        terms = search_result.items
        
        # batch load necessary attributes
        batchLoadAttribute(terms, "emapa_info")
        batchLoadAttribute(terms, "synonyms")
        
        # add term highlights if termSearch
        if search_query.has_valid_param('termSearch'):
            self._add_emapa_highlights(terms, search_query.get_value('termSearch'))
        
        
        search_result.items = convert_models(terms, EMAPATermDomain)
        
        return search_result
    
    def _add_emapa_highlights(self, terms, termSearch):
        """
        add term_highlight and synonym_highlight to each term in terms
        """
        
        # prepare search tokens for highlighting
        termSearchTokens = splitSemicolonInput(termSearch)
                    
        # prepare term_highlight and synonym_highlight
        #    only set synonym_highlight if there is no highlight
        #    on the term
        for term in terms:
            setattr(term, "term_highlight", "")
            setattr(term, "synonym_highlight", "")
            
            term.term_highlight = highlightEMAPA(term.term, termSearchTokens)
            
            # if term could not be highlighted, try synonyms
            if '<mark>' not in term.term_highlight:
                for synonym in term.synonyms:
                
                    # try to highlight each synonym
                    synonym_highlight = highlightEMAPA(synonym.synonym, termSearchTokens)
                    
                    if '<mark>' in synonym_highlight:
                        # set first synonym match and exit
                        term.synonym_highlight = synonym_highlight
                        break
    
    
    
    
