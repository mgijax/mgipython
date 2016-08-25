from mgipython.service.helpers.date_helper import DateHelper
from mgipython.model import GxdHTExperiment
from mgipython.model import db
from base_dao import BaseDAO


class GxdHTExperimentDAO(BaseDAO):
    
    model_class = GxdHTExperiment
    
    def _build_search_query(self, search_query):

        query = GxdHTExperiment.query

        if search_query.has_valid_param("name"):
            name = search_query.get_value("name")
            name = name.lower()
            query = query.filter(db.func.lower(GxdHTExperiment.name).like(name))

        if search_query.has_valid_param("description"):
            description = search_query.get_value("description")
            description = description.lower()
            query = query.filter(db.func.lower(GxdHTExperiment.description).like(description))

        if search_query.has_valid_param("release_date"):
            release_date = search_query.get_value("release_date")
            query = DateHelper().build_query_with_date(query, GxdHTExperiment.release_date, release_date)

        if search_query.has_valid_param("creation_date"):
            creation_date = search_query.get_value("creation_date")
            query = DateHelper().build_query_with_date(query, GxdHTExperiment.creation_date, creation_date)

        if search_query.has_valid_param("_TriageState_key"):
            triage_state_key = search_query.get_value("_TriageState_key")
            query = query.filter(GxdHTExperiment._triagestate_key == int(triage_state_key))
            
        #query = query.order_by(GxdHTExperiment._experiment_key)
        
        return query
