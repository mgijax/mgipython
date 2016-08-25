from mgipython.dao.gxd_ht_experiment_dao import GxdHTExperimentDAO
from mgipython.model import GxdHTExperiment
from mgipython.model.query import batchLoadAttribute
from mgipython.error import NotFoundError
from mgipython.error import DateFormatError
from mgipython.modelconfig import cache
from dateutil import parser
import sys

class GxdHTExperimentService():
    
    gxd_dao = GxdHTExperimentDAO()
    
    def search(self, search_query):

        for dateField in [ 'release_date', 'created_date' ]:
            if search_query.has_valid_param(dateField):
                self.validate_date(search_query.get_value(dateField))

        search_result = self.gxd_dao.search(search_query)
        self.loadAttributes(search_result.items)
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
        batchLoadAttribute(objects, "source_object")
        batchLoadAttribute(objects, "triagestate_object")
        batchLoadAttribute(objects, "curationstate_object")
        batchLoadAttribute(objects, "studytype_object")
        batchLoadAttribute(objects, "notes")
        batchLoadAttribute(objects, "experiment_variables")

        #batchLoadAttribute([experiment], "all_properties")
        batchLoadAttribute(objects, "assay_count")
        batchLoadAttribute(objects, "pubmed_ids")
        batchLoadAttribute(objects, "experimental_factors")
        batchLoadAttribute(objects, "experiment_designs")
        batchLoadAttribute(objects, "experiment_types")
        batchLoadAttribute(objects, "provider_contact_names")
        batchLoadAttribute(objects, "sample_count")
        batchLoadAttribute(objects, "primaryid_object")
        batchLoadAttribute(objects, "secondaryids")

        batchLoadAttribute(objects, "evaluatedby_object")
        batchLoadAttribute(objects, "curatedby_object")
        batchLoadAttribute(objects, "createdby_object")
        batchLoadAttribute(objects, "modifiedby_object")


    def validate_date(self, date):
        try:
            if " " in date:
                [operator, check_date] = date.split(" ")
                parser.parse(check_date)
            elif ".." in date:
                [date1, date2] = date.split("..")
                parser.parse(date1)
                parser.parse(date2)
            else:
                parser.parse(date)
        except:
            e = sys.exc_info()[0]
            raise DateFormatError("Invalid Date format: %s" % str(e))
 
