from mgipython.dao.reference_dao import ReferenceDAO
from mgipython.model import GxdIndexRecord
from mgipython.model.query import batchLoadAttributeExists
from mgipython.error import NotFoundError
from mgipython.modelconfig import cache

class ReferenceService():
    
    reference_dao = ReferenceDAO()
    
    def get_by_key(self, _refs_key):
        reference = self.reference_dao.get_by_key(_refs_key)
        if not reference:
            raise NotFoundError("No Reference for _refs_key=%d" % _refs_key)
    
        return reference
    
    
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
        """
        return self.get_by_jnum_id("J:%s" % jnumber)
  
  
    def search(self, args):
        """
        search references by args object
        """
        
        references = self.reference_dao.search(
            accids=args.accids,
            journal=args.journal,
            title=args.title,
            authors=args.authors,
            primeAuthor=args.primeAuthor,
            volume=args.volume,
            year=args.year,
            marker_id=args.marker_id,
            allele_id=args.allele_id,
            limit=args.limit
        )
        
        return references
    
    
    def search_for_summary(self, form):
        """
        Searches references with form object,
        populates has_* exists attributes for reference
        summary
        """
        references = self.reference_dao.search(
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




