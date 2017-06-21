from mgipython.model import Accession, Allele, Marker, Reference
from mgipython.service_schema.search import SearchQuery
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

    def _build_search_query(self, search_query):
        query = Reference.query
        
        if search_query.has_valid_param("issue"):
            issue = search_query.get_value("issue").lower()
            query = query.filter(db.func.lower(Reference.issue).like(issue))
            
        if search_query.has_valid_param("pages"):
            pages = search_query.get_value("pages").lower()
            query = query.filter(db.func.lower(Reference.pgs).like(pages))
            
        if search_query.has_valid_param("date"):
            date = search_query.get_value("date").lower()
            query = query.filter(db.func.lower(Reference.date).like(date))
            
        if search_query.has_valid_param("abstract"):
            abstract = search_query.get_value("abstract").lower()
            query = query.filter(db.func.lower(Reference.abstract).like(abstract))
            
#        if search_query.has_valid_param("notes"):
#            notes = search_query.get_value("notes").lower()
#            query = query.filter(db.func.lower(Reference.experiment_notechunks).like(notes))
            
        if search_query.has_valid_param("reference_type"):
            referenceType = search_query.get_value("reference_type").lower()
            query = query.filter(db.func.lower(Reference.reftype).like(referenceType))
            
        if search_query.has_valid_param("is_review"):
            if int(search_query.get_value("is_review")) > 0:
                query = query.filter(Reference.isreviewarticle == int(search_query.get_value("is_review")))
            
        if search_query.has_valid_param("title"):
            title = search_query.get_value("title").lower()
            query = query.filter(db.func.lower(Reference.title).like(title))
            
        if search_query.has_valid_param("authors"):
            authors = search_query.get_value("authors").lower()
            query = query.filter(db.func.lower(Reference.authors).like(authors))
            
        if search_query.has_valid_param("primary_author"):
            primaryAuthor = search_query.get_value("primary_author").lower()
            query = query.filter(db.func.lower(Reference._primary).like(primaryAuthor))
            
        if search_query.has_valid_param("journal"):
            journal = search_query.get_value("journal").lower()
            query = query.filter(db.func.lower(Reference.journal).like(journal))
            
        if search_query.has_valid_param("volume"):
            volume = search_query.get_value("volume").lower()
            query = query.filter(db.func.lower(Reference.vol) == volume)
            
        if search_query.has_valid_param("year"):
            if int(search_query.get_value("year")) > 0:
                query = query.filter(Reference.year == int(search_query.get_value("year")))

        # ID of marker related to the reference
        if search_query.has_valid_param("marker_id"):
            marker_id = search_query.get_value("marker_id")
            if marker_id.strip() != '':
                marker_accession = db.aliased(Accession)
                sub_reference = db.aliased(Reference)
            
                # doing this in a subquery
                sq = db.session.query(sub_reference) \
                    .join(sub_reference.all_markers) \
                    .join(marker_accession, Marker.mgiid_object) \
                    .filter(marker_accession.accid==marker_id) \
                    .filter(sub_reference._refs_key==Reference._refs_key) \
                    .correlate(Reference)
                    
                query = query.filter(sq.exists())
            
        # ID of allele related to the reference
        if search_query.has_valid_param("allele_id"):
            allele_id = search_query.get_value("allele_id")
            if allele_id.strip() != '':
                allele_accession = db.aliased(Accession)
                sub_reference = db.aliased(Reference)
            
                # doing this in a subquery
                sq = db.session.query(sub_reference) \
                    .join(sub_reference.explicit_alleles) \
                    .join(allele_accession, Allele.mgiid_object) \
                    .filter(allele_accession.accid==allele_id) \
                    .filter(sub_reference._refs_key==Reference._refs_key) \
                    .correlate(Reference)
                
                query = query.filter(sq.exists())
            
        # any IDs associated with the reference
        if search_query.has_valid_param("accids") and (search_query.get_value("accids").strip() != ''):
            # split and prep the IDs
            accidsToSearch = splitCommaInput(search_query.get_value("accids").lower())
            
            # subquery for searching by J#
            jnum_accession = db.aliased(Accession)
            sub_ref1 = db.aliased(Reference)
            ref_sq = db.session.query(sub_ref1) \
                    .join(jnum_accession, sub_ref1.jnumid_object) \
                    .filter(db.func.lower(jnum_accession.accid).in_(accidsToSearch)) \
                    .filter(sub_ref1._refs_key==Reference._refs_key) \
                    .correlate(Reference)

            query1 = query.filter(ref_sq.exists())

            # subquery for searching by PubMed ID        
            pmed_accession = db.aliased(Accession)
            sub_ref2 = db.aliased(Reference)
            pmed_sq = db.session.query(sub_ref2) \
                    .join(pmed_accession, sub_ref2.pubmedid_object) \
                    .filter(db.func.lower(pmed_accession.accid).in_(accidsToSearch)) \
                    .filter(sub_ref2._refs_key==Reference._refs_key) \
                    .correlate(Reference)
            
            query2 = query.filter(pmed_sq.exists())
            
            # pull the two subqueries together into the main query using a union
            query = query1.union(query2)
                            
        # setting sort, roughly bringing newer references to the top
        query = query.order_by(Reference._refs_key.desc())
    
        # setting limit on number of returned references, if specified
        if search_query.has_valid_param("limit"):
            query = query.limit(int(search_query.get_value("limit"))) 

        return query

    def search_old(self, accids=None, 
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
        
        query = Reference.query
        search_query = SearchQuery()
        
        if authors:
            search_query.set_param("authors", authors)
    
        if primeAuthor:
            search_query.set_param("primary_author", primeAuthor)
    
        if journal:
            search_query.set_param("journal", journal)
            
        if title:
            search_query.set_param("title", title)
    
        if volume:
            search_query.set_param("volume", volume)
    
        if year:
            search_query.set_param("year", year)
    
        if marker_id:
            search_query.set_param("marker_id", marker_id)
            
        if allele_id:
            search_query.set_param("allele_id", allele_id)
            
        if accids:
            search_query.set_param("accids", accids)
           
        return self.search(search_query).items
    