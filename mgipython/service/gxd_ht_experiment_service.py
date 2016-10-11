from flask_login import current_user
from mgipython.model.query import batchLoadAttribute
from mgipython.service_schema import *
from mgipython.service.helpers import *
from mgipython.model import *
from mgipython.dao import *
from mgipython.domain import *
from mgipython.error import *
from dateutil import parser
from datetime import datetime

class GxdHTExperimentService():
    
    gxd_dao = GxdHTExperimentDAO()
    gxd_var_dao = GxdHTExperimentVariableDAO();
    sample_dao = GxdHTSampleDAO()
    raw_sample_dao = GxdHTRawSampleDAO()
    vocterm_dao = VocTermDAO()
    
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
                raw_domain_sample.domain_sample._experiment_key = int(key)
                raw_domain_sample.domain_sample.name = raw_domain_sample.source["name"]
                newItems.append(raw_domain_sample)

            search_result.items = SampleGrouper().group_samples(newItems)

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

        #gxd_var_dao.save(args["experiment_variables"])

        if len(args["experiment_variables"]) > 0:
            for var in experiment.experiment_variables:
                self.gxd_var_dao.delete(var)

            variables = []
            first_key = self.gxd_var_dao.get_next_key()
            for var in args["experiment_variables"]:
                newvar = GxdHTExperimentVariable()
                newvar._experimentvariable_key = first_key
                first_key = first_key + 1
                newvar._experiment_key = experiment._experiment_key
                newvar._term_key = var["_term_key"]
                variables.append(newvar)
            experiment.experiment_variables = variables
        else:
            pass

        experiment._modifiedby_key = current_user._user_key
        experiment.modification_date = datetime.now()

        if experiment._evaluationstate_key != args["_evaluationstate_key"]:
            search_query1 = SearchQuery()
            search_query1.set_param('vocab_name', "GXD HT Evaluation State")
            search_result1 = self.vocterm_dao.search(search_query1)
            search_query2 = SearchQuery()
            search_query2.set_param('vocab_name', "GXD HT Curation State")
            search_result2 = self.vocterm_dao.search(search_query2)

            for es in search_result1.items:
                 if es._term_key == args["_evaluationstate_key"] and es.term == "No":
                     for cs in search_result2.items:
                         if cs.term == "Not Applicable":
                             experiment._curationstate_key = cs._term_key
                 if es._term_key == args["_evaluationstate_key"] and es.term != "No":
                     for cs in search_result2.items:
                         if cs.term == "Not Done":
                             experiment._curationstate_key = cs._term_key

            experiment._evaluationstate_key = args["_evaluationstate_key"]
            experiment._evaluatedby_key = current_user._user_key
            experiment.evaluated_date = datetime.now()

        self.gxd_dao.update(experiment)
        ret_experiment = GxdHTExperimentDomain()
        ret_experiment.load_from_model(experiment)
        return ret_experiment

    def delete(self, key):
        experiment = self.gxd_dao.get_by_key(key)
        if not experiment:
            raise NotFoundError("No GXD HT Experiment for _experiment_key=%d" % key)
        self.gxd_dao.delete(experiment)
