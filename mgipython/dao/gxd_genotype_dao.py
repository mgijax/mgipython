from mgipython.model import *
from .base_dao import BaseDAO

class GenotypeDAO(BaseDAO):

    model_class = Genotype

    def _build_search_query(self, search_query):

        query = Genotype.query

        if search_query.has_valid_param("_genotype_key"):
            genotype_key = search_query.get_value("_genotype_key")
            query = query.filter(Genotype._genotype_key == int(genotype_key))
       
        if search_query.has_valid_param("_strain_key"):
            strain_key = search_query.get_value("_strain_key")
            query = query.filter(Genotype._strain_key == int(strain_key))

        if search_query.has_valid_param("mgiid"):
            accession = db.aliased(Accession)
            mgiid = search_query.get_value("mgiid").upper()
            query = query.join(accession, Genotype._genotype_key == accession._object_key) \
                .filter(accession.accid == mgiid) \
                .filter(accession.preferred == 1) \
                .filter(accession._mgitype_key == 12) \
                .filter(accession._logicaldb_key==1)
            
        return query 
