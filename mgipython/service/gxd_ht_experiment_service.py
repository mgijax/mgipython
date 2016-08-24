from mgipython.dao.gxd_ht_experiment_dao import GxdHTExperimentDAO
from mgipython.model import GxdHTExperiment
from mgipython.model.query import batchLoadAttribute
from mgipython.error import NotFoundError
from mgipython.service.helpers.date_helper import DateHelper
from mgipython.modelconfig import cache
from dateutil import parser

class GxdHTExperimentService():
    
    gxd_dao = GxdHTExperimentDAO()
    
    def search(self, search_query):

        if search_query.has_valid_param("release_date"):
            DateHelper().validate_date(search_query.get_value("release_date"))

        search_result = self.gxd_dao.search(search_query)
        #self.loadAttributes(search_result.items)
        return search_result

    def create(self, args):
        experiment = GxdHTExperiment()
        experiment.name = args["name"]
        experiment.description = args["description"]
        self.gxd_dao.save(experiment)
        return experiment

    # Read
    def get(self, key):
        experiment = self.gxd_dao.get_by_key(key)
        self.loadAttributes([experiment])
        if not experiment:
            raise NotFoundError("No GxdHTExperiment for _experiment_key=%d" % key)
        return experiment
 
    # Update
    def save(self, key, args):
        experiment = self.gxd_dao.get_by_key(key)
        if not experiment:
            raise NotFoundError("No GxdHTExperiment for _experiment_key=%d" % key)
        experiment.name = args["name"]
        experiment.description = args["description"]
        self.gxd_dao.save(experiment)
        return experiment

    def delete(self, key):
        experiment = self.gxd_dao.get_by_key(key)
        if not experiment:
            raise NotFoundError("No GXD HT Experiment for _experiment_key=%d" % key)
        self.gxd_dao.delete(experiment)

    def loadAttributes(self, objects):
        batchLoadAttribute(objects, "source_object", 1000, True)
        batchLoadAttribute(objects, "triagestate_object", 1000, True)
        batchLoadAttribute(objects, "curationstate_object", 1000, True)
        batchLoadAttribute(objects, "studytype_object", 1000, True)
        batchLoadAttribute(objects, "notes", 1000, True)
        #batchLoadAttribute(objects, "experiment_variables", 1000, True)

        batchLoadAttribute(objects, "all_properties", 1000, True)

        #batchLoadAttribute(objects, "assay_count", 1000, True)
        #batchLoadAttribute(objects, "pubmed_ids", 1000, True)
        #batchLoadAttribute(objects, "experimental_factors", 1000, True)
        #batchLoadAttribute(objects, "experiment_designs", 1000, True)
        #batchLoadAttribute(objects, "experiment_types", 1000, True)
        #batchLoadAttribute(objects, "provider_contact_names", 1000, True)
        #batchLoadAttribute(objects, "sample_count", 1000, True)
        batchLoadAttribute(objects, "primaryid_object", 1000, True)
        batchLoadAttribute(objects, "secondaryids", 1000, True)

        batchLoadAttribute(objects, "evaluatedby_object", 1000, True)
        batchLoadAttribute(objects, "curatedby_object", 1000, True)
        batchLoadAttribute(objects, "createdby_object", 1000, True)
        batchLoadAttribute(objects, "modifiedby_object", 1000, True)

