from base_serializer import Field, Serializer
from mgipython.domain.acc_domains import AccessionDomain
from mgipython.domain.voc_domains import VocTermDomain
from mgipython.domain.mgi_domains import *
#from Property import PropertyDomain
#from Accession import AccessionDomain
#from User import UserDomain
#from VocTerm import VocTermDomain

class GxdHTExperimentDomain(Serializer):

    __fields__ = [
        # Keys
        Field("_experiment_key"),
        Field("_studytype_key"),
        Field("_triagestate_key"),
        Field("_curationstate_key"),

        # Text Fields
        Field("primaryid"),
        Field("name"),
        Field("description"),
        Field("arraydesign"),

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
        Field("curated_date"),
        Field("modification_date"),
        Field("release_date"),
        Field("creation_date"),
        Field("lastupdate_date"),

        Field("source_object", conversion_class=VocTermDomain),
        Field("notes", conversion_class=NoteDomain),

        # User Objects
        Field("evaluatedby_object", conversion_class=UserDomain),
        Field("curatedby_object", conversion_class=UserDomain),
        Field("createdby_object", conversion_class=UserDomain),
        Field("modifiedby_object", conversion_class=UserDomain),

        # Accession
        Field("secondaryids", conversion_class=AccessionDomain),
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
