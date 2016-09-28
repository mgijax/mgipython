from mgipython.service.helpers.date_helper import DateHelper
from mgipython.model import GxdHTExperiment
from mgipython.model import GxdHTExperimentVariable
from mgipython.model import Accession
from mgipython.model import MGIUser
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

        if search_query.has_valid_param("evaluated_date"):
            evaluated_date = search_query.get_value("evaluated_date")
            query = DateHelper().build_query_with_date(query, GxdHTExperiment.evaluated_date, evaluated_date)

        if search_query.has_valid_param("initial_curated_date"):
            initial_curated_date = search_query.get_value("initial_curated_date")
            query = DateHelper().build_query_with_date(query, GxdHTExperiment.initial_curated_date, initial_curated_date)

        if search_query.has_valid_param("last_curated_date"):
            last_curated_date = search_query.get_value("last_curated_date")
            query = DateHelper().build_query_with_date(query, GxdHTExperiment.last_curated_date, last_curated_date)

        if search_query.has_valid_param("release_date"):
            release_date = search_query.get_value("release_date")
            query = DateHelper().build_query_with_date(query, GxdHTExperiment.release_date, release_date)

        if search_query.has_valid_param("lastupdate_date"):
            lastupdate_date = search_query.get_value("lastupdate_date")
            query = DateHelper().build_query_with_date(query, GxdHTExperiment.lastupdate_date, lastupdate_date)

        if search_query.has_valid_param("modification_date"):
            modification_date = search_query.get_value("modification_date")
            query = DateHelper().build_query_with_date(query, GxdHTExperiment.modification_date, modification_date)

        if search_query.has_valid_param("creation_date"):
            creation_date = search_query.get_value("creation_date")
            query = DateHelper().build_query_with_date(query, GxdHTExperiment.creation_date, creation_date)

        if search_query.has_valid_param("_evaluationstate_key"):
            evaluationstate_key = search_query.get_value("_evaluationstate_key")
            query = query.filter(GxdHTExperiment._evaluationstate_key == int(evaluationstate_key))

        if search_query.has_valid_param("_experiment_key"):
            experiment_key = search_query.get_value("_experiment_key")
            query = query.filter(GxdHTExperiment._experiment_key == int(experiment_key))

        if search_query.has_valid_param("_curationstate_key"):
            curationstate_key = search_query.get_value("_curationstate_key")
            query = query.filter(GxdHTExperiment._curationstate_key == int(curationstate_key))

        if search_query.has_valid_param("_studytype_key"):
            studytype_key = search_query.get_value("_studytype_key")
            query = query.filter(GxdHTExperiment._studytype_key == int(studytype_key))

        if search_query.has_valid_param("_experimenttype_key"):
            experimenttype_key = search_query.get_value("_experimenttype_key")
            query = query.filter(GxdHTExperiment._experimenttype_key == int(experimenttype_key))

        if search_query.has_valid_param("evaluatedby_object"):
            user = db.aliased(MGIUser)
            evaluatedby_object = search_query.get_value("evaluatedby_object")
            login = evaluatedby_object["login"].lower()
            if len(login) > 0:
                query = query.join(user, GxdHTExperiment.evaluatedby_object).filter(db.func.lower(user.login).like(login))

        if search_query.has_valid_param("initialcuratedby_object"):
            user = db.aliased(MGIUser)
            initialcuratedby_object = search_query.get_value("initialcuratedby_object")
            login = initialcuratedby_object["login"].lower()
            if len(login) > 0:
                query = query.join(user, GxdHTExperiment.initialcuratedby_object).filter(db.func.lower(user.login).like(login))

        if search_query.has_valid_param("lastcuratedby_object"):
            user = db.aliased(MGIUser)
            lastcuratedby_object = search_query.get_value("lastcuratedby_object")
            login = lastcuratedby_object["login"].lower()
            if len(login) > 0:
                query = query.join(user, GxdHTExperiment.lastcuratedby_object).filter(db.func.lower(user.login).like(login))

        if search_query.has_valid_param("primaryid"):
            primaryid = search_query.get_value("primaryid").lower()
            query = query.filter(db.func.lower(GxdHTExperiment.primaryid).like(primaryid))

        if search_query.has_valid_param("secondaryid"):
            accession = db.aliased(Accession)
            secondaryid = search_query.get_value("secondaryid").lower()
            query = query.join(accession, GxdHTExperiment.secondaryid_objects).filter(db.func.lower(accession.accid).like(secondaryid))

        # The next portition of code will break if aliasing of gxd_experiment is used
        if search_query.has_valid_param("experiment_variables"):
            experiment_variables = search_query.get_value("experiment_variables")

            # Or query
            #search_list = []
            #for var in experiment_variables:
            #    search_list.append(var["_term_key"]) 
            #    query = query.join(GxdHTExperimentVariable, GxdHTExperiment.experiment_variables).filter(GxdHTExperimentVariable._term_key.in_(search_list))

            # And Query
            for var in experiment_variables:
                sq = db.session.query(GxdHTExperimentVariable)
                sq = sq.filter(GxdHTExperimentVariable._term_key == var["_term_key"])
                sq = sq.filter(GxdHTExperimentVariable._experiment_key == GxdHTExperiment._experiment_key)
                sq = sq.correlate(GxdHTExperiment)
                query = query.filter(sq.exists())

        return query
