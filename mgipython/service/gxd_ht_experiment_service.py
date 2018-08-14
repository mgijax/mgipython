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
import helpers.symbolsort
import re

class GxdHTExperimentService():
    
    gxd_dao = GxdHTExperimentDAO()
    gxd_var_dao = GxdHTExperimentVariableDAO();
    sample_dao = GxdHTSampleDAO()
    raw_sample_dao = GxdHTRawSampleDAO()
    vocterm_dao = VocTermDAO()
    genotype_dao = GenotypeDAO()
    mgitype_dao = MGITypeDAO()
    accession_dao = AccessionDAO()
    emaps_dao = VocTermEMAPSDAO()

    def __init__(self):

        self.evaluation_state_no_term_key = None
        self.relevance_term_non_mouse_key = None
        self.relevance_term_yes_key = None
        self.curation_state_na_term_key = None
        self.curation_state_notdone_term_key = None
        self.curation_state_done_term_key = None
        self.organism_mouse_key = None
        self.gender_ns_key = None
        self.gender_na_key = None
        self.age_term_na_term = None
        self.age_term_ns_term = None
        self.genotype_na_key = None
        self.genotype_ns_key = None
        self.accession_key_cache = {}
    
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
        self._smartAlphaSortSummary(newitems)
        search_result.items = newitems
        return search_result

    def _smartAlphaSortSummary(self, experimentList):
        def idCompare(a, b):
            return symbolsort.nomenCompare(a.primaryid, b.primaryid)
        experimentList.sort(idCompare)
        return

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
 
    def get_samples(self, key, consolidate_rows):
        experiment = self.gxd_dao.get_by_key(key)
        if not experiment:
            raise NotFoundError("No GxdHTExperiment for _experiment_key=%d" % key)

        search_result = self.raw_sample_dao.download_raw_samples(experiment.primaryid)

        newItems = []
        for sample in search_result.items:
            collection = GxdHTSampleCollection()
            raw_domain_sample = GxdHTRawSampleDomain()
            raw_domain_sample.load_from_dict(sample)
            collection.raw_sample = raw_domain_sample

            #domain_sample = GxdHTSampleDomain()
            #domain_sample = domain_sample
            #domain_sample._experiment_key = int(key)
            #domain_sample.name = raw_domain_sample.source["name"]
            #collection.domain_sample = domain_sample
            if not raw_domain_sample.source:
                raw_domain_sample.source = {} 

            if "name" not in raw_domain_sample.source:
                if raw_domain_sample.assay and "name" in raw_domain_sample.assay:
                    raw_domain_sample.source["name"] = raw_domain_sample.assay["name"]
                   
            if "name" in raw_domain_sample.source:
                collection.name = raw_domain_sample.source["name"]

            if "name" in raw_domain_sample.source or consolidate_rows:
                newItems.append(collection)

        #search_result.items = newItems
        search_result.items = SampleGrouper().group_raw_samples(newItems, consolidate_rows)
        search_result.total_count = len(newItems)

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

        _note_key_index = BaseDAO()._get_next_key(Note)

        if "notetext" in args and len(args["notetext"]) > 0:
            if len(experiment.notes) > 0:
                if len(experiment.notes[0].chunks) > 0:
                    experiment.notes[0].chunks[0].note = args["notetext"]
                else:
                    notechunk = NoteChunk()
                    notechunk._note_key = experiment.notes[0]._note_key
                    notechunk.sequencenum = 1
                    notechunk.note = args["notetext"]
                    experiment.notes[0].chunks.append(notechunk)
            else:
                newnote = Note()
                newnote._note_key = _note_key_index
                _note_key_index = _note_key_index + 1
                newnote._object_key = experiment._experiment_key
                newnote._mgitype_key = 42
                newnote._notetype_key = 1047

                notechunk = NoteChunk()
                notechunk._note_key = newnote._note_key
                notechunk.sequencenum = 1
                notechunk.note = args["notetext"]

                newnote.chunks.append(notechunk)
                experiment.notes.append(newnote)

        else:
            if len(experiment.notes) > 0:
                self.gxd_dao.delete(experiment.notes[0])
                experiment.notes = []

        experiment._modifiedby_key = current_user._user_key
        experiment.modification_date = datetime.now()

        if experiment._evaluationstate_key != args["_evaluationstate_key"]:
            self.loadEvaluationStates()
            self.loadCurationStates()

            if args["_evaluationstate_key"] == self.evaluation_state_no_term_key:
                experiment._curationstate_key = self.curation_state_na_term_key
            else:
                experiment._curationstate_key = self.curation_state_notdone_term_key

            experiment._evaluationstate_key = args["_evaluationstate_key"]
            experiment._evaluatedby_key = current_user._user_key
            experiment.evaluated_date = datetime.now()

        experiment_sample_count = len(experiment.samples)

        if len(args["samples"]) > 0:

            self.loadRelevances()
            first_key = self.sample_dao.get_next_key()
            for sample in args["samples"]:
                sample_collection = GxdHTSampleCollection()
                sample_collection.load_from_dict(sample)

                if sample_collection.sample_domain != None:

                    if sample_collection.sample_domain._sample_key != None:
                        newsample = self.sample_dao.get_by_key(sample_collection.sample_domain._sample_key)
                    else:
                        newsample = GxdHTSample()
                        experiment.samples.append(newsample)
                        newsample._sample_key = first_key
                        first_key = first_key + 1

                    if sample_collection.sample_domain != None:
                        self.loadOrganisms()

                        if sample_collection.sample_domain.notes != None and len(sample_collection.sample_domain.notes) > 0 and sample_collection.sample_domain.notes[0].text != None and len(sample_collection.sample_domain.notes[0].text) > 0:
                            
                            if len(newsample.notes) > 0:
                                if len(newsample.notes[0].chunks) > 0:
                                    print "Modify Sample Note"
                                    newsample.notes[0].chunks[0].note = sample_collection.sample_domain.notes[0].text
                                else:
                                    print "Create Sample Note"
                                    notechunk = NoteChunk()
                                    notechunk._note_key = newsample.notes[0]._note_key
                                    notechunk.sequencenum = 1
                                    notechunk.note = sample_collection.sample_domain.notes[0].text
                                    newsample.notes[0].chunks.append(notechunk)
                            else:
                                newnote = Note()
                                newnote._note_key = _note_key_index
                                _note_key_index = _note_key_index + 1
                                newnote._object_key = newsample._sample_key
                                newnote._mgitype_key = 43
                                newnote._notetype_key = 1048

                                notechunk = NoteChunk()
                                notechunk._note_key = newnote._note_key
                                notechunk.sequencenum = 1
                                notechunk.note = sample_collection.sample_domain.notes[0].text

                                print "Create Sample Note"
                                print "Modify Sample Note"
                                newnote.chunks.append(notechunk)
                                newsample.notes.append(newnote)

                        else:
                            if len(newsample.notes) > 0:
                                print "Delete note chunk, note for this sample"
                                self.sample_dao.delete(newsample.notes[0])
                                newsample.notes = []

                        if sample_collection.sample_domain._organism_key == None:
                            newsample._organism_key = self.organism_mouse_key
                        else:
                            newsample._organism_key = sample_collection.sample_domain._organism_key

                        if sample_collection.sample_domain._relevance_key == None:
                            self.loadRelevances()
                            if newsample._organism_key == self.organism_mouse_key:
                                newsample._relevance_key = self.relevance_term_yes_key
                            else:
                                newsample._relevance_key = self.relevance_term_non_mouse_key
                        else:
                            newsample._relevance_key = sample_collection.sample_domain._relevance_key

                        if sample_collection.sample_domain.ageunit == None:
                            self.loadAgeTerms()
                            if newsample._relevance_key == self.relevance_term_yes_key:
                                newsample.age = self.age_term_ns_term
                            else:
                                newsample.age = self.age_term_na_term
                        else:
                            newsample.age = str(sample_collection.sample_domain.ageunit)
                            if sample_collection.sample_domain.agerange != None and len(sample_collection.sample_domain.agerange) > 0:
                                newsample.age = newsample.age + " " + str(sample_collection.sample_domain.agerange)

                        if sample_collection.sample_domain._sex_key == None:
                            self.loadGenders()
                            if newsample._relevance_key == self.relevance_term_yes_key:
                                newsample._sex_key = self.gender_ns_key
                            else:
                                newsample._sex_key = self.gender_na_key
                        else:
                            newsample._sex_key = sample_collection.sample_domain._sex_key

                        self.loadGenotypes()
                        if sample_collection.sample_domain._genotype_key == None:
                            if newsample._relevance_key == self.relevance_term_yes_key:
                                newsample._genotype_key = self.genotype_ns_key
                            else:
                                newsample._genotype_key = self.genotype_na_key
                        else:
                            accession_object_key = self.lookupAccessionKey(sample_collection.sample_domain._genotype_key)
                            if(accession_object_key != None):
                                newsample._genotype_key = accession_object_key
                            else:
                                if newsample._relevance_key == self.relevance_term_yes_key:
                                    newsample._genotype_key = self.genotype_ns_key
                                else:
                                    newsample._genotype_key = self.genotype_na_key

                        newsample.name = sample_collection.sample_domain.name

                        if sample_collection.sample_domain._emapa_key:
                            if sample_collection.sample_domain.emaps_object and sample_collection.sample_domain.emaps_object.primaryid == sample_collection.sample_domain._emapa_key:
                                emaps_object = sample_collection.sample_domain.emaps_object
                            else:
                                emaps_object = self.lookupEMAPSObject(sample_collection.sample_domain._emapa_key)

                            if emaps_object != None:
                                newsample._emapa_key = emaps_object._emapa_term_key
                                newsample._stage_key = emaps_object._stage_key
                            else:
                                newsample._emapa_key = None
                                newsample._stage_key = None
                        else:
                            newsample._emapa_key = None
                            newsample._stage_key = None

                        newsample._createdby_key = current_user._user_key
                        newsample.creation_date = datetime.now()
                        newsample._modifiedby_key = current_user._user_key
                        newsample.modification_date = datetime.now()

        else:
            if experiment_sample_count > 0:
                for sample in experiment.samples:
                    if len(sample.notes) > 0:
                        print "Delete Note: " + str(sample.notes[0]._note_key)
                        self.sample_dao.delete(sample.notes[0])
                    print "Delete Sample: " + str(sample._sample_key)
                    self.sample_dao.delete(sample)
                experiment.samples = []

        if len(experiment.samples) > 0:
            self.loadCurationStates()
            experiment._curationstate_key = self.curation_state_done_term_key
            experiment._lastcuratedby_key = current_user._user_key
            experiment.last_curated_date = datetime.now()
            if experiment_sample_count == 0:
                experiment._initialcuratedby_key = current_user._user_key
                experiment.initial_curated_date = datetime.now()

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

    def lookupAccessionKey(self, mgiid):
        pattern = re.compile(re.escape('mgi:'), re.IGNORECASE)
        mgiid = pattern.sub('', mgiid)
        mgiid = "MGI:" + mgiid
        if mgiid in self.accession_key_cache:
            return self.accession_key_cache[mgiid]
        else:
            genotype_search_query = SearchQuery()
            genotype_search_query.set_param('accid', mgiid)
            genotype_search_query.set_param('preferred', 1)
            genotype_search_query.set_param('_mgitype_key', 12)
            genotype_search_query.set_param('_logicaldb_key', 1)
            genotype_search_result = self.accession_dao.search(genotype_search_query)
            if len(genotype_search_result.items) > 0:
                self.accession_key_cache[mgiid] = genotype_search_result.items[0]._object_key
                return self.accession_key_cache[mgiid]
            else:
                return None

    def lookupEMAPSObject(self, emapsid):
        emaps_search_query = SearchQuery()
        emaps_search_query.set_param('emapsid', emapsid)
        emaps_search_result = self.emaps_dao.search(emaps_search_query)
        if len(emaps_search_result.items) > 0:
            return emaps_search_result.items[0]
        else:
            return None

    def loadEvaluationStates(self):
        if self.evaluation_state_no_term_key != None:
            return

        evaluation_state_search_query = SearchQuery()
        evaluation_state_search_query.set_param('vocab_name', "GXD HT Evaluation State")
        evaluation_state_search_result = self.vocterm_dao.search(evaluation_state_search_query)
        for evaluation_state in evaluation_state_search_result.items:
            if evaluation_state.term == "No":
                self.evaluation_state_no_term_key = evaluation_state._term_key
                break

    def loadCurationStates(self):
        if self.curation_state_na_term_key != None and self.curation_state_notdone_term_key != None and self.curation_state_done_term_key != None:
            return
        curation_state_search_query = SearchQuery()
        curation_state_search_query.set_param('vocab_name', "GXD HT Curation State")
        curation_state_search_result = self.vocterm_dao.search(curation_state_search_query)
        for curation_state in curation_state_search_result.items:
            if curation_state.term == "Not Applicable":
                self.curation_state_na_term_key = curation_state._term_key
            if curation_state.term == "Not Done":
                self.curation_state_notdone_term_key = curation_state._term_key
            if curation_state.term == "Done":
                self.curation_state_done_term_key = curation_state._term_key

    def loadRelevances(self):
        if self.relevance_term_non_mouse_key != None and self.relevance_term_yes_key != None:
            return
        relevance_search_query = SearchQuery()
        relevance_search_query.set_param('vocab_name', "GXD HT Relevance")
        relevance_search_result = self.vocterm_dao.search(relevance_search_query)

        for relevance in relevance_search_result.items:
            if relevance.term == "Non-mouse sample; no data stored":
                self.relevance_term_non_mouse_key = relevance._term_key
            if relevance.term == "Yes":
                self.relevance_term_yes_key = relevance._term_key

    def loadGenders(self):
        if self.gender_ns_key != None and self.gender_na_key != None:
            return
        gender_search_query = SearchQuery()
        gender_search_query.set_param('vocab_name', "Gender")
        gender_search_result = self.vocterm_dao.search(gender_search_query)

        for gender in gender_search_result.items:
            if gender.term == "Not Specified":
                self.gender_ns_key = gender._term_key
            if gender.term == "Not Applicable":
                self.gender_na_key = gender._term_key

    def loadAgeTerms(self):
        if self.age_term_na_term != None and self.age_term_ns_term != None:
            return

        age_search_query = SearchQuery()
        age_search_query.set_param('vocab_name', "GXD HT Age")
        age_search_result = self.vocterm_dao.search(age_search_query)
        for age in age_search_result.items:
            if age.term == "Not Applicable":
                self.age_term_na_term = age.term
            if age.term == "Not Specified":
                self.age_term_ns_term = age.term

    def loadOrganisms(self):
        if self.organism_mouse_key != None:
            return
        mgitype_search_query = SearchQuery()
        mgitype_search_query.set_param('name', "GXD HT Sample")
        mgitype_search_result = self.mgitype_dao.search(mgitype_search_query)

        for organism in mgitype_search_result.items[0].organisms:
            if organism.commonname == "mouse, laboratory":
                self.organism_mouse_key = organism._organism_key

    def loadGenotypes(self):
        if self.genotype_ns_key != None and self.genotype_na_key != None:
            return
        self.genotype_ns_key = self.lookupAccessionKey("MGI:2166310")
        self.genotype_na_key = self.lookupAccessionKey("MGI:2166309")
