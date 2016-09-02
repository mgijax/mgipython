from Property import PropertyDomain
from Accession import AccessionDomain
from User import UserDomain

class GxdHTExperimentDomain():

    def __init__(self, db_object=None):

        if db_object != None:
            self.primaryid = db_object.primaryid
            self.key = db_object._experiment_key
            self.name = db_object.name
            self.description = db_object.description

            self.provider_contact_names = []
            self.pubmed_ids = []
            self.experimental_factors = []
            self.experiment_designs = []
            self.experiment_types = []
            for prop in db_object.all_properties:
                if prop.term_object.term == "raw contact name":
                    self.provider_contact_names.append(prop.value)
                if prop.term_object.term == "PubMed ID":
                    self.pubmed_ids.append(PropertyDomain(prop))
                if prop.term_object.term == "raw assay count":
                    self.assay_count = prop.value
                if prop.term_object.term == "raw sample count":
                    self.sample_count = prop.value
                if prop.term_object.term == "raw experimental factor":
                    self.experimental_factors.append(prop.value)
                if prop.term_object.term == "raw experiment design":
                    self.experiment_designs.append(prop.value)
                if prop.term_object.term == "raw experiment type":
                    self.experiment_types.append(prop.value)
            if db_object.arraydesign != None:
                self.arraydesign = db_object.arraydesign

            if db_object.createdby_object != None:
                self.createdby = UserDomain(db_object.createdby_object)
            if db_object.curatedby_object != None:
                self.curatedby = UserDomain(db_object.curatedby_object)
            if db_object.evaluatedby_object != None:
                self.evaluatedby = UserDomain(db_object.evaluatedby_object)
            if db_object.modifiedby_object != None:
                self.modifiedby = UserDomain(db_object.modifiedby_object)

            if db_object.evaluated_date != None:
                self.evaluated_date = db_object.evaluated_date
            if db_object.curated_date != None:
                self.curated_date = db_object.curated_date
            if db_object.creation_date != None:
                self.creation_date = db_object.creation_date
            if db_object.modification_date != None:
                self.modification_date = db_object.modification_date
            if db_object.release_date != None:
                self.release_date = db_object.release_date
            if db_object.lastupdate_date != None:
                self.lastupdate_date = db_object.lastupdate_date

            self.secondaryaccession = []
            for accession in db_object.secondaryids:
                self.secondaryaccession.append(AccessionDomain(accession))
