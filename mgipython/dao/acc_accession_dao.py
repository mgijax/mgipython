from mgipython.model import *
from .base_dao import BaseDAO

class AccessionDAO(BaseDAO):

    model_class = Accession

    def _build_search_query(self, search_query):
        query = Accession.query

        if search_query.has_valid_param("accid"):
            accid = search_query.get_value("accid").lower()
            query = query.filter(db.func.lower(Accession.accid) == accid)

        if search_query.has_valid_param("preferred"):
            preferred = search_query.get_value("preferred")
            query = query.filter(Accession.preferred == preferred)

        if search_query.has_valid_param("_mgitype_key"):
            _mgitype_key = search_query.get_value("_mgitype_key")
            query = query.filter(Accession._mgitype_key == _mgitype_key)

        if search_query.has_valid_param("_logicaldb_key"):
            _logicaldb_key = search_query.get_value("_logicaldb_key")
            query = query.filter(Accession._logicaldb_key == _logicaldb_key)

        return query
