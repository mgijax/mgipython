from mgipython.dao.gxd_ht_experiment_dao import GxdHTExperimentDAO
from mgipython.model import GxdHTExperiment
from mgipython.model.query import batchLoadAttribute
from mgipython.error import NotFoundError
from mgipython.modelconfig import cache

class GxdHTExperimentService():
    
    gxd_dao = GxdHTExperimentDAO()
    
    def get_by_key(self, key):
        experiment = self.gxd_dao.get_by_key(key)
        self.loadAttributes(experiment)
        if not experiment:
            raise NotFoundError("No GxdHTExperiment for _experiment_key=%d" % key)
        return experiment
    
    def search(self, search_query):
        search_result = self.gxd_dao.search(search_query)
        print search_result
        for experiment in search_result.items:
            self.loadAttributes(experiment)
        return search_result

    def edit(self, key, args):
        experiment = self.gxd_dao.get_by_key(key)
        if not experiment:
            raise NotFoundError("No GxdHTExperiment for _experiment_key=%d" % key)
        experiment.name = args.name
        experiment.description = args.description
        
        self.gxd_dao.save(experiment)
        return experiment

    def create(self, args):
        experiment = GxdHTExperiment()
        experiment.name = args.name
        experiment.description = args.description
        self.gxd_dao.save(experiment)
        return experiment

    def delete(self, key):
        experiment = self.gxd_dao.get_by_key(key)
        if not experiment:
            raise NotFoundError("No GXD HT Experiment for _experiment_key=%d" % key)
        self.gxd_dao.delete(experiment)

    def loadAttributes(self, experiment):
        batchLoadAttribute([experiment], "source_object")
        batchLoadAttribute([experiment], "triagestate_object")
        batchLoadAttribute([experiment], "curationstate_object")
        batchLoadAttribute([experiment], "studytype_object")
        batchLoadAttribute([experiment], "notes")
        #batchLoadAttribute([experiment], "experiment_variables")

        #batchLoadAttribute([experiment], "assay_count.value")
        #batchLoadAttribute([experiment], "pubmed_ids")

        #batchLoadAttribute([experiment], "experimental_factors")
        #batchLoadAttribute([experiment], "experiment_designs")
        #batchLoadAttribute([experiment], "experiment_types")
        #batchLoadAttribute([experiment], "provider_contact_names")
        #batchLoadAttribute([experiment], "sample_count")
        #batchLoadAttribute([experiment], "assay_designs")
        batchLoadAttribute([experiment], "primaryid_object")
        batchLoadAttribute([experiment], "secondaryids")

