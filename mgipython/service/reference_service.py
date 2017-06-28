from mgipython.dao.reference_dao import ReferenceDAO
from mgipython.model import GxdIndexRecord
from mgipython.model.query import batchLoadAttributeExists
from mgipython.error import NotFoundError
from mgipython.modelconfig import cache
from mgipython.domain.reference_domains import SmallReference, ReferenceDomain, ReferenceFullDomain
from mgipython.domain import convert_models
from mgipython.parse import parse_jnumber

class ReferenceService():
    
    reference_dao = ReferenceDAO()
    
    def get_by_key(self, _refs_key):
        reference = self.reference_dao.get_by_key(_refs_key)
        if not reference:
            raise NotFoundError("No Reference for _refs_key=%d" % _refs_key)
    
        return reference
    
    def get_domain_by_key(self, _refs_key):
        # first load model object and hit a lazy-loaded field to make sure it's populated
        # before serialization
        reference = self.get_by_key(_refs_key)
        cws = reference.current_workflow_statuses
        rt = reference.reftype.term

        # then use it to populate a domain object
        referenceFull = ReferenceFullDomain()
        referenceFull.load_from_model(reference)

        return referenceFull
    
    
    def get_by_jnum_id(self, jnum_id):
        """
        Retrieve a single reference by jnum_id
        """
        reference = self.reference_dao.get_by_jnum_id(jnum_id)
        if not reference:
            raise NotFoundError("No Reference for J Number=%s" % jnum_id)
        
        # load citation_cache
        reference.citation_cache
        
        return reference
    
    def get_by_jnumber(self, jnumber):
        """
        Retrieve a single reference by jnumber (without J: prefix)
        returns SmallReference
        """
        jnum_id = parse_jnumber(jnumber)
        reference = self.get_by_jnum_id(jnum_id)
        return convert_models(reference, SmallReference)
  
  
    def search(self, search_query):
        """
        search references by fields in search_query object
        """
        
        search_result = self.reference_dao.search(search_query)
        newitems = []
        for item in search_result.items:
            newitem = ReferenceDomain()
            newitem.load_from_model(item)
            newitems.append(newitem)
        search_result.items = newitems
        return search_result
    
    
    def search_for_summary(self, form):
        """
        Searches references with form object,
        populates has_* exists attributes for reference
        summary
        """
        references = self.reference_dao.search_old(
            accids=form.accids.data,
            primeAuthor=form.primeAuthor.data,
            authors=form.authors.data,
            journal=form.journal.data,
            title=form.title.data,
            volume=form.volume.data,
            year=form.year.data,
            marker_id=form.marker_id.data,
            allele_id=form.allele_id.data,
            limit=form.reference_limit.data
        )
        

        # load any exists attributes for associated data links
        batchLoadAttributeExists(references, ['all_markers', 
                                          'expression_assays', 
                                          'gxdindex_records',
                                          'explicit_alleles',
                                          'antibodies',
                                          'probes',
                                          'specimens',
                                          'gxd_images',
                                          'mapping_experiments'])


        return references




