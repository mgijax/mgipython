from mgipython.model import Accession, Allele, Marker, Reference
from mgipython.service_schema.search import SearchQuery
from mgipython.model import db, MLDReferenceNoteChunk, VocTerm, ReferenceNoteChunk
from mgipython.parse.parser import splitCommaInput
from base_dao import BaseDAO
import re

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
            
        if search_query.has_valid_param("notes"):
            notes = search_query.get_value("notes").lower()
            query = query.join(ReferenceNoteChunk, Reference.reference_notechunks).filter(db.func.lower(ReferenceNoteChunk.note).like(notes))
            
        if search_query.has_valid_param("reference_type"):
            referenceType = search_query.get_value("reference_type").lower()
            query = query.join(Reference.reftype)
            query = query.filter(db.func.lower(VocTerm.term).like(referenceType))
            
        if search_query.has_valid_param("is_review"):
            if search_query.get_value("is_review").upper() in ('Y', 'N'):
                isReviewInt = 0
                if search_query.get_value("is_review").upper() == 'Y':
                    isReviewInt = 1
                query = query.filter(Reference.isreviewarticle == isReviewInt)
            
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
            query = query.filter(db.func.lower(Reference.vol).like(volume))
            
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
            # split and prep the IDs; eliminate extra spaces, replacing them with commas
            idString = re.sub('[\s,]+', ',', search_query.get_value("accids").lower())
            accidsToSearch = splitCommaInput(idString)
            
            # Searching by accession ID is valid for J: numbers, MGI IDs, PubMed IDs, GO_REF IDs,
            # and DOI (Journal Link) IDs.  Each of these is currently handled in a subquery, but
            # for performance reasons, we try to include only those that are relevant to a given
            # set of input IDs.
            
            subqueries = []
            
            # subquery for searching by J# (if j: present in string)
            if idString.find("j:") >= 0:
                jnum_accession = db.aliased(Accession)
                sub_ref1 = db.aliased(Reference)
                ref_sq = db.session.query(sub_ref1) \
                    .join(jnum_accession, sub_ref1.jnumid_object) \
                    .filter(db.func.lower(jnum_accession.accid).in_(accidsToSearch)) \
                    .filter(sub_ref1._refs_key==Reference._refs_key) \
                    .correlate(Reference)

                subqueries.append(query.filter(ref_sq.exists()))

            # subquery for searching by PubMed ID (if only digits in at least one ID)
            digitsOnly = False              # True if at least one ID has only digits
            for accid in accidsToSearch:
                if re.match('^[0-9]+$', accid):
                    digitsOnly = True
                    break
                
            if digitsOnly:
                pmed_accession = db.aliased(Accession)
                sub_ref2 = db.aliased(Reference)
                pmed_sq = db.session.query(sub_ref2) \
                    .join(pmed_accession, sub_ref2.pubmedid_object) \
                    .filter(db.func.lower(pmed_accession.accid).in_(accidsToSearch)) \
                    .filter(sub_ref2._refs_key==Reference._refs_key) \
                    .correlate(Reference)
            
                subqueries.append(query.filter(pmed_sq.exists()))
            
            # subquery for searching by MGI ID (if mgi: present in string)
            if idString.find("mgi:") >= 0:
                mgi_accession = db.aliased(Accession)
                sub_ref3 = db.aliased(Reference)
                mgi_sq = db.session.query(sub_ref3) \
                    .join(mgi_accession, sub_ref3.mgiid_object) \
                    .filter(db.func.lower(mgi_accession.accid).in_(accidsToSearch)) \
                    .filter(sub_ref3._refs_key==Reference._refs_key) \
                    .correlate(Reference)

                subqueries.append(query.filter(mgi_sq.exists()))

            # subquery for searching by DOI ID (if at least one ID begins with 10.)
            beginsTen = False              # True if at least one ID begins with 10.
            for accid in accidsToSearch:
                if accid.startswith('10.'):
                    beginsTen = True
                    break
                
            if beginsTen:
                doi_accession = db.aliased(Accession)
                sub_ref4 = db.aliased(Reference)
                doi_sq = db.session.query(sub_ref4) \
                    .join(doi_accession, sub_ref4.doiid_object) \
                    .filter(db.func.lower(doi_accession.accid).in_(accidsToSearch)) \
                    .filter(sub_ref4._refs_key==Reference._refs_key) \
                    .correlate(Reference)
            
                subqueries.append(query.filter(doi_sq.exists()))
            
            # subquery for GO_REF ID (if the ID string contains with go_ref:)
            if idString.find("go_ref:") >= 0:
                goref_accession = db.aliased(Accession)
                sub_ref5 = db.aliased(Reference)
                goref_sq = db.session.query(sub_ref5) \
                    .join(goref_accession, sub_ref5.gorefid_object) \
                    .filter(db.func.lower(goref_accession.accid).in_(accidsToSearch)) \
                    .filter(sub_ref5._refs_key==Reference._refs_key) \
                    .correlate(Reference)

                subqueries.append(query.filter(goref_sq.exists())) 
            
            # pull the two subqueries together into the main query using a union
            if subqueries:
                query = subqueries[0]
                for subquery in subqueries[1:]:
                    query = query.union(subquery)
                            
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
    