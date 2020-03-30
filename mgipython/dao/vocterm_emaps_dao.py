from mgipython.model import *
from mgipython.model import *
from .base_dao import BaseDAO

class VocTermEMAPSDAO(BaseDAO):

    def _build_search_query(self, search_query):
        query = VocTermEMAPS.query

        if search_query.has_valid_param("emapsid"):
            emapsid = search_query.get_value("emapsid").upper()
            query = query.filter(VocTermEMAPS.primaryid == emapsid)

        if search_query.has_valid_param("_term_key"):
            _term_key = search_query.get_value("_term_key")
            query = query.filter(VocTermEMAPS._term_key == _term_key)

        if search_query.has_valid_param("_emapa_term_key"):
            _emapa_term_key = search_query.get_value("_emapa_term_key")
            query = query.filter(VocTermEMAPS._emapa_term_key == _emapa_term_key)

        if search_query.has_valid_param("_stage_key"):
            _stage_key = search_query.get_value("_stage_key")
            query = query.filter(VocTermEMAPS._stage_key == _stage_key)

        return query
