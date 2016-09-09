from mgipython.service.helpers.date_helper import DateHelper
from mgipython.model import GxdHTExperiment
from mgipython.model import db
from base_dao import BaseDAO


class GxdHTExperimentDAO(BaseDAO):
    
    model_class = GxdHTExperiment
    
    def _build_search_query(self, search_query):

        query = GxdHTExperiment.query

        if search_query.has_valid_param("name"):
            name = search_query.get_value("name").lower()
            query = query.filter(db.func.lower(GxdHTExperiment.name).like(name))

        if search_query.has_valid_param("description"):
            description = search_query.get_value("description").lower()
            query = query.filter(db.func.lower(GxdHTExperiment.description).like(description))

        if search_query.has_valid_param("release_date"):
            release_date = search_query.get_value("release_date")
            query = DateHelper().build_query_with_date(query, GxdHTExperiment.release_date, release_date)

        if search_query.has_valid_param("creation_date"):
            creation_date = search_query.get_value("creation_date")
            query = DateHelper().build_query_with_date(query, GxdHTExperiment.creation_date, creation_date)

        if search_query.has_valid_param("modification_date"):
            modification_date = search_query.get_value("modification_date")
            query = DateHelper().build_query_with_date(query, GxdHTExperiment.modification_date, modification_date)

        if search_query.has_valid_param("evaluated_date"):
            evaluated_date = search_query.get_value("evaluated_date")
            query = DateHelper().build_query_with_date(query, GxdHTExperiment.evaluated_date, evaluated_date)

        if search_query.has_valid_param("curated_date"):
            curated_date = search_query.get_value("curated_date")
            query = DateHelper().build_query_with_date(query, GxdHTExperiment.curated_date, curated_date)

        if search_query.has_valid_param("lastupdate_date"):
            lastupdate_date = search_query.get_value("lastupdate_date")
            query = DateHelper().build_query_with_date(query, GxdHTExperiment.lastupdate_date, lastupdate_date)

        if search_query.has_valid_param("_triagestate_key"):
            triage_state_key = search_query.get_value("_triagestate_key")
            query = query.filter(GxdHTExperiment._triagestate_key == int(triage_state_key))

        if search_query.has_valid_param("_experiment_key"):
            experiment_key = search_query.get_value("_experiment_key")
            query = query.filter(GxdHTExperiment._experiment_key == int(experiment_key))

        if search_query.has_valid_param("primaryid"):
            primaryid = search_query.get_value("primaryid")
            query = query.filter(GxdHTExperiment.primaryid == primaryid)

        return query
