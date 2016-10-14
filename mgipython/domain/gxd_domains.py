from base_serializer import Field, Serializer
from mgipython.domain.acc_domains import AccessionDomain
from mgipython.domain.voc_domains import VocTermDomain
from mgipython.domain.mgi_domains import *
#from Property import PropertyDomain
#from Accession import AccessionDomain
#from User import UserDomain
#from VocTerm import VocTermDomain

class GxdHTExperimentSummaryDomain(Serializer):

    __fields__ = [
        Field("_experiment_key"),
        Field("primaryid"),
    ]

class GxdHTSampleDomain(Serializer):
    __fields__ = [
        Field("_sample_key"),
        Field("_experiment_key"),

        Field("name"),
        Field("age"),

        Field("_organism_key"),
        Field("_sex_key"),
        Field("_emapa_key"),
        Field("_stage_key"),
        Field("_genotype_key"),
        Field("_relevance_key"),

    ]

class GxdHTVariableDomain(Serializer):
    __fields__ = [
        # Keys
        Field("_experimentvariable_key"),
        Field("_experiment_key"),
        Field("_term_key"),
        Field("term_object", conversion_class=VocTermDomain),
    ]

class GxdHTRawSampleDomain(Serializer):
    __fields__ = [
        Field("assay"),
        Field("characteristic"),

        Field("name"),

        Field("extract"),
        Field("file"),
        Field("labeled-extract"),
        Field("scan"),
        Field("source"),

        Field("variable"),
        Field("domain_sample", conversion_class=GxdHTSampleDomain),
    ]

    def getKey(self):
        return self.source["name"]

class GxdHTExperimentDomain(Serializer):

    __fields__ = [
        # Keys
        Field("_experiment_key"),
        Field("_studytype_key"),
        Field("_evaluationstate_key"),
        Field("_curationstate_key"),
        Field("_experimenttype_key"),

        # Text Fields
        Field("primaryid"),
        Field("name"),
        Field("description"),

        # Properties
        Field("assay_count"),
        Field("sample_count"),
        Field("provider_contact_names"),
        Field("pubmed_ids"),
        Field("experimental_factors"),
        Field("experiment_designs"),
        Field("experiment_types"),
 
        # Date
        Field("evaluated_date"),
        Field("initial_curated_date"),
        Field("last_curated_date"),
        Field("release_date"),
        Field("lastupdate_date"),

        Field("modification_date"),
        Field("creation_date"),

        Field("source_object", conversion_class=VocTermDomain),
        Field("notes", conversion_class=NoteDomain),
        Field("samples", conversion_class=GxdHTSampleDomain),

        # User Objects
        Field("evaluatedby_object", conversion_class=UserDomain),
        Field("initialcuratedby_object", conversion_class=UserDomain),
        Field("lastcuratedby_object", conversion_class=UserDomain),

        Field("createdby_object", conversion_class=UserDomain),
        Field("modifiedby_object", conversion_class=UserDomain),

        # Accession
        Field("secondaryid_objects", conversion_class=AccessionDomain),
        Field("experiment_variables", conversion_class=GxdHTVariableDomain),
    ]

    def get_assay_count(self, experiment):
        for prop in experiment.all_properties:
            if prop.term_object.term == "raw assay count":
                return prop.value

    def get_sample_count(self, experiment):
        for prop in experiment.all_properties:
            if prop.term_object.term == "raw sample count":
                return prop.value

    def get_provider_contact_names(self, experiment):
        list = []
        for prop in experiment.all_properties:
            if prop.term_object.term == "raw contact name":
                list.append(prop.value)
        return list

    def get_pubmed_ids(self, experiment):
        list = []
        for prop in experiment.all_properties:
            if prop.term_object.term == "PubMed ID":
                list.append(prop.value)
        return list

    def get_experimental_factors(self, experiment):
        list = []
        for prop in experiment.all_properties:
            if prop.term_object.term == "raw experimental factor":
                list.append(prop.value)
        return list

    def get_experiment_designs(self, experiment):
        list = []
        for prop in experiment.all_properties:
            if prop.term_object.term == "raw experiment design":
                list.append(prop.value)
        return list

    def get_experiment_types(self, experiment):
        list = []
        for prop in experiment.all_properties:
            if prop.term_object.term == "raw experiment type":
                list.append(prop.value)
        return list


