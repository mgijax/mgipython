from mgipython.model import Accession, Reference
from mgipython.model import db
from mgipython.parse.parser import splitCommaInput
from base_dao import BaseDAO

import logging

logger = logging.getLogger("mgipython.dao")


class ReferenceDAO(BaseDAO):
    
    model_class = Reference
    
    
    def get_by_jnum_id(self, jnum_id):
        """
        Return a reference by jnum_id
        """
        jnum_id = jnum_id.upper()
        
        sub_ref = db.aliased(Reference)
        accession_model = db.aliased(Accession)
        
        sq = db.session.query(sub_ref)
        sq = sq.join(accession_model, sub_ref.jnumid_object)
        sq = sq.filter(accession_model.accid==jnum_id)
        sq = sq.filter(sub_ref._refs_key==Reference._refs_key)
        sq = sq.correlate(Reference)
        
        
        query = Reference.query
        
        return query.filter( sq.exists() ).first()


    def search(self, accids=None, 
                     journal=None, 
                     title=None,
                     authors=None, 
                     primeAuthor=None, 
                     volume=None, 
                     year=None, 
                     marker_id=None, 
                     allele_id=None,
                     limit=None):
        """
        Search references by
            accids,
            journal,
            title,
            authors,
            primAuthor,
            volume,
            year,
            marker_id,
            allele_id
        """
        
        logger.debug('In ReferenceDAO - calling search')
        
        query = Reference.query
        
        if authors:
            authors = authors.lower()
            query = query.filter(
                db.func.lower(Reference.authors).like(authors),
            )
    
        if primeAuthor:
            primeAuthor = primeAuthor.lower()
            query = query.filter(
                db.func.lower(Reference._primary).like(primeAuthor),
            )
    
        if journal:
            journal = journal.lower()
            query = query.filter(
                db.func.lower(Reference.journal).like(journal),
            )
            
        if title:
            title = title.lower()
            query = query.filter(
                db.func.lower(Reference.title).like(title),
            )
    
        if volume:
            volume = volume.lower()
            query = query.filter(db.func.lower(Reference.vol)==volume)
    
        if year:
            query = query.filter(Reference.year==int(year))
    
        if marker_id:
            marker_accession = db.aliased(Accession)
            sub_reference = db.aliased(Reference)
            sq = db.session.query(sub_reference) \
                    .join(sub_reference.all_markers) \
                    .join(marker_accession, Marker.mgiid_object) \
                    .filter(marker_accession.accid==marker_id) \
                    .filter(sub_reference._refs_key==Reference._refs_key) \
                    .correlate(Reference)
                    
            query = query.filter(
                    sq.exists()     
            )
            
        if allele_id:
            allele_accession = db.aliased(Accession)
            sub_reference = db.aliased(Reference)
            sq = db.session.query(sub_reference) \
                    .join(sub_reference.explicit_alleles) \
                    .join(allele_accession, Allele.mgiid_object) \
                    .filter(allele_accession.accid==allele_id) \
                    .filter(sub_reference._refs_key==Reference._refs_key) \
                    .correlate(Reference)
                
            query = query.filter(
                    sq.exists()
            )
            
            
        if accids:
            # split and prep the IDs
            accids = accids.lower()
            accidsToSearch = splitCommaInput(accids)
            
            jnum_accession = db.aliased(Accession)
            sub_ref1 = db.aliased(Reference)
            
            ref_sq = db.session.query(sub_ref1) \
                    .join(jnum_accession, sub_ref1.jnumid_object) \
                    .filter(db.func.lower(jnum_accession.accid).in_(accidsToSearch)) \
                    .filter(sub_ref1._refs_key==Reference._refs_key) \
                    .correlate(Reference)
                    
            pmed_accession = db.aliased(Accession)
            sub_ref2 = db.aliased(Reference)
                    
            pmed_sq = db.session.query(sub_ref2) \
                    .join(pmed_accession, sub_ref2.pubmedid_object) \
                    .filter(db.func.lower(pmed_accession.accid).in_(accidsToSearch)) \
                    .filter(sub_ref2._refs_key==Reference._refs_key) \
                    .correlate(Reference)
            
        query1 = query.filter(ref_sq.exists())
        query2 = query.filter(pmed_sq.exists())
            
        query = query1.union(query2)
                            
        # setting sort
        query = query.order_by(Reference._refs_key.desc())
    
        # setting limit on number of returned references
        if limit:
            query = query.limit(limit) 
                       
        references = query.all()
           
        return references
    
    