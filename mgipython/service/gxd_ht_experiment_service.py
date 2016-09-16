from flask_login import current_user
from mgipython.dao.gxd_ht_experiment_dao import GxdHTExperimentDAO
from mgipython.model import GxdHTExperiment
from mgipython.model.query import batchLoadAttribute
from mgipython.error import NotFoundError
from mgipython.service.helpers.date_helper import DateHelper
from mgipython.service_schema.search import SearchResults
from mgipython.dao.gxd_ht_sample_dao import GxdHTSampleDAO
from mgipython.dao.gxd_ht_raw_sample_dao import GxdHTRawSampleDAO
from mgipython.domain.gxd_domains import *
from mgipython.modelconfig import cache
from dateutil import parser
from datetime import datetime

class GxdHTExperimentService():
    
    gxd_dao = GxdHTExperimentDAO()
    sample_dao = GxdHTSampleDAO()
    raw_sample_dao = GxdHTRawSampleDAO()
    
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


    def total_count(self):
        return self.gxd_dao.get_total_count()


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
 
    def get_samples(self, key):
        experiment = self.gxd_dao.get_by_key(key)
        if not experiment:
            raise NotFoundError("No GxdHTExperiment for _experiment_key=%d" % key)

        if len(experiment.samples) > 0:
        #    try to hook up each raw sample to a domain sample via source name
            pass
        else:
            search_result = self.raw_sample_dao.download_raw_samples(experiment.primaryid)
            newItems = []
            for sample in search_result.items:
                domain_sample = GxdHTSampleDomain()
                raw_domain_sample = GxdHTRawSampleDomain()
                raw_domain_sample.load_from_dict(sample)
                raw_domain_sample.domain_sample = domain_sample
                newItems.append(raw_domain_sample)
            search_result.items = newItems

        return search_result

    # Update
    def save(self, key, args):
        experiment = self.gxd_dao.get_by_key(key)
        if not experiment:
            raise NotFoundError("No GxdHTExperiment for _experiment_key=%d" % key)

        experiment.name = args["name"]
        experiment.description = args["description"]
        experiment._studytype_key = args["_studytype_key"]
        experiment._experimenttype_key = args["_experimenttype_key"]

        experiment._modifiedby_key = current_user._user_key
        experiment.modification_date = datetime.now()

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
