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
    genotype_dao = GenotypeDAO()
    mgitype_dao = MGITypeDAO()

    def __init__(self):

        self.evaluation_state_no_term = None
        self.relevance_term_non_mouse = None
        self.relevance_term_yes = None
        self.curation_state_na_term = None
        self.curation_state_notdone_term = None
        self.organism_mouse = None
        self.gender_ns = None
        self.gender_na = None
        self.age_term_ns = None
        self.age_term_na = None
        self.genotype_na = None
        self.genotype_ns = None
    
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
            self.loadEvaluationStates()
            self.loadCurationStates()

            if args["_evaluationstate_key"] == self.evaluation_state_no_term._term_key:
                experiment._curationstate_key = self.curation_state_na_term._term_key
            else:
                experiment._curationstate_key = self.curation_state_notdone_term._term_key

            experiment._evaluationstate_key = args["_evaluationstate_key"]
            experiment._evaluatedby_key = current_user._user_key
            experiment.evaluated_date = datetime.now()

        print "Samples: "
        if len(experiment.samples) == 0:
            self.loadRelevances()
            if len(args["samples"]) > 0:
                print "Creating new samples to save"
                first_key = self.sample_dao.get_next_key()
                for sample in args["samples"]:
                    sample_domain = GxdHTSampleDomain()
                    sample_domain.load_from_dict(sample["domain_sample"])

                    newsample = GxdHTSample()
                    # if sample_domain has key
                    #     do lookup
                    # else:
                    #     newsample._sample_key = first_key
                    #     first_key = first_key + 1
                    newsample._sample_key = first_key
                    first_key = first_key + 1

                    self.loadOrganisms()

                    if sample_domain._organism_key == None:
                        newsample._organism_key = self.organism_mouse._organism_key
                    else:
                        newsample._organism_key = sample_domain._organism_key

                    if sample_domain._relevance_key == None:
                        self.loadRelevances()
                        if newsample._organism_key == self.organism_mouse._organism_key:
                            newsample._relevance_key = self.relevance_term_yes._term_key
                        else:
                            newsample._relevance_key = self.relevance_term_non_mouse._term_key
                    else:
                        newsample._relevance_key = sample_domain._relevance_key

                    if sample_domain.age == None:
                        #self.loadAgeTerms()
                        if newsample._relevance_key == self.relevance_term_yes._term_key:
                            #newsample.age = self.age_term_ns.term
                            newsample.age = "Not Specified"
                        else:
                            #newsample.age = self.age_term_na.term
                            newsample.age = "Not Applicable"
                    else:
                        newsample.age = sample_domain.age

                    if sample_domain._sex_key == None:
                        self.loadGenders()
                        if newsample._relevance_key == self.relevance_term_yes._term_key:
                            newsample._sex_key = self.gender_ns._term_key
                        else:
                            newsample._sex_key = self.gender_na._term_key
                    else:
                        newsample._sex_key = sample_domain._sex_key

                    if sample_domain._genotype_key == None:
                        self.loadGenotypes()
                        if newsample._relevance_key == self.relevance_term_yes._term_key:
                            newsample._genotype_key = self.genotype_ns._genotype_key
                        else:
                            newsample._genotype_key = self.genotype_na._genotype_key
                    else:
                        newsample._genotype_key = sample_domain._genotype_key

                    newsample.name = sample_domain.name
                    newsample._emapa_key = sample_domain._emapa_key
                    newsample._stage_key = sample_domain._stage_key
                    newsample._createdby_key = current_user._user_key
                    newsample.creation_date = datetime.now()
                    newsample._modifiedby_key = current_user._user_key
                    newsample.modification_date = datetime.now()
                    experiment.samples.append(newsample)

            else:
                print "No samples to save"
        else:
            #print args["samples"]
            print "Merge Samples"

        print "Running update on experiment"
        self.gxd_dao.update(experiment)
        print "Finished update on experiment"

        ret_experiment = GxdHTExperimentDomain()
        ret_experiment.load_from_model(experiment)
        self.__init__()
        return ret_experiment

    def delete(self, key):
        experiment = self.gxd_dao.get_by_key(key)
        if not experiment:
            raise NotFoundError("No GXD HT Experiment for _experiment_key=%d" % key)
        self.gxd_dao.delete(experiment)

    def loadEvaluationStates(self):
        if self.evaluation_state_no_term != None:
            return

        evaluation_state_search_query = SearchQuery()
        evaluation_state_search_query.set_param('vocab_name', "GXD HT Evaluation State")
        evaluation_state_search_result = self.vocterm_dao.search(evaluation_state_search_query)
        for evaluation_state in evaluation_state_search_result.items:
            if evaluation_state.term == "No":
                self.evaluation_state_no_term = evaluation_state
                break

    def loadCurationStates(self):
        if self.curation_state_na_term != None and self.curation_state_notdone_term != None:
            return
        curation_state_search_query = SearchQuery()
        curation_state_search_query.set_param('vocab_name', "GXD HT Curation State")
        curation_state_search_result = self.vocterm_dao.search(curation_state_search_query)
        for curation_state in curation_state_search_result.items:
            if curation_state.term == "Not Applicable":
                self.curation_state_na_term = curation_state
            if curation_state.term == "Not Done":
                self.curation_state_notdone_term = curation_state

    def loadRelevances(self):
        if self.relevance_term_non_mouse != None and self.relevance_term_yes != None:
            return
        relevance_search_query = SearchQuery()
        relevance_search_query.set_param('vocab_name', "GXD HT Relevance")
        relevance_search_result = self.vocterm_dao.search(relevance_search_query)

        for relevance in relevance_search_result.items:
            if relevance.term == "Non-mouse sample; no data stored":
                self.relevance_term_non_mouse = relevance
            if relevance.term == "Yes":
                self.relevance_term_yes = relevance

    def loadGenders(self):
        if self.gender_ns != None and self.gender_na != None:
            return
        gender_search_query = SearchQuery()
        gender_search_query.set_param('vocab_name', "Gender")
        gender_search_result = self.vocterm_dao.search(gender_search_query)

        for gender in gender_search_result.items:
            if gender.term == "Not Specified":
                self.gender_ns = gender
            if gender.term == "Not Applicable":
                self.gender_na = gender

    def loadAgeTerms(self):
        age_search_query = SearchQuery()
        age_search_query.set_param('vocab_name', "GXD HT Ages")
        age_search_result = self.vocterm_dao.search(age_search_query)

        for age in age_search_result.items:
            if age.term == "Not Specified":
                self.age_term_ns = age
            if age.term == "Not Applicable":
                self.age_term_na = age

    def loadOrganisms(self):
        if self.organism_mouse != None:
            return
        mgitype_search_query = SearchQuery()
        mgitype_search_query.set_param('name', "GXD HT Sample")
        mgitype_search_result = self.mgitype_dao.search(mgitype_search_query)

        for organism in mgitype_search_result.items[0].organisms:
            if organism.commonname == "mouse, laboratory":
                self.organism_mouse = organism

    def loadGenotypes(self):
        if self.genotype_ns != None and self.genotype_na != None:
            return
        genotype_search_query = SearchQuery()
        genotype_search_query.set_param('mgiid', "MGI:2166310")
        genotype_search_result = self.genotype_dao.search(genotype_search_query)
        self.genotype_ns = genotype_search_result.items[0]

        genotype_search_query = SearchQuery()
        genotype_search_query.set_param('mgiid', "MGI:2166309")
        genotype_search_result = self.genotype_dao.search(genotype_search_query)
        self.genotype_na = genotype_search_result.items[0]

