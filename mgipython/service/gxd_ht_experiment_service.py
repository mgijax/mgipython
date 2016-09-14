from flask_login import current_user
from mgipython.dao.gxd_ht_experiment_dao import GxdHTExperimentDAO
from mgipython.model import GxdHTExperiment
from mgipython.model.query import batchLoadAttribute
from mgipython.error import NotFoundError
from mgipython.service.helpers.date_helper import DateHelper
from mgipython.service_schema.search import SearchResults
from mgipython.domain.gxd_domains import *
from mgipython.modelconfig import cache
from dateutil import parser
from datetime import datetime

class GxdHTExperimentService():
    
    gxd_dao = GxdHTExperimentDAO()
    
    def search(self, search_query):

        for dateField in [ 'release_date', 'lastupdate_date', 'evaluated_date', 'curated_date', 'creation_date', 'modification_date' ]:
            if search_query.has_valid_param(dateField):
                DateHelper().validate_date(search_query.get_value(dateField))

        search_result = self.gxd_dao.search(search_query)
        newitems = []
        for item in search_result.items:
            newitem = GxdHTExperimentDomain()
            newitem.load_from_model(item)
            newitems.append(newitem)
        search_result.items = newitems
        return search_result

    def summary_search(self, search_query):
        for dateField in [ 'release_date', 'lastupdate_date', 'evaluated_date', 'curated_date', 'creation_date', 'modification_date' ]:
            if search_query.has_valid_param(dateField):
                DateHelper().validate_date(search_query.get_value(dateField))

        search_result = self.gxd_dao.search(search_query)
        newitems = []
        for item in search_result.items:
            newitem = GxdHTExperimentSummaryDomain()
            newitem.load_from_model(item)
            newitems.append(newitem)
        search_result.items = newitems
        return search_result


    def create(self, args):
        experiment = GxdHTExperiment()
        experiment.name = args["name"]
        experiment.description = args["description"]
        self.gxd_dao.save(experiment)
        return GxdHTExperimentDomain(experiment)

    # Read
    def get(self, key):
        experiment = self.gxd_dao.get_by_key(key)
        if not experiment:
            raise NotFoundError("No GxdHTExperiment for _experiment_key=%d" % key)

        ret_experiment = GxdHTExperimentDomain()
        ret_experiment.load_from_model(experiment)
        return ret_experiment
 
    # Update
    def save(self, key, args):
        experiment = self.gxd_dao.get_by_key(key)
        if not experiment:
            raise NotFoundError("No GxdHTExperiment for _experiment_key=%d" % key)

        experiment.name = args["name"]
        experiment.description = args["description"]
        print experiment._evaluationstate_key
        print args["_evaluationstate_key"]
        if experiment._evaluationstate_key != args["_evaluationstate_key"]:
            experiment._evaluationstate_key = args["_evaluationstate_key"]
            experiment._evaluatedby_key = current_user._user_key
            experiment.evaluated_date = datetime.now()

        self.gxd_dao.save(experiment)
        ret_experiment = GxdHTExperimentDomain()
        ret_experiment.load_from_model(experiment)
        return ret_experiment

    def delete(self, key):
        experiment = self.gxd_dao.get_by_key(key)
        if not experiment:
            raise NotFoundError("No GXD HT Experiment for _experiment_key=%d" % key)
        self.gxd_dao.delete(experiment)
