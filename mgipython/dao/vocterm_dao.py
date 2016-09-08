from mgipython.model import Accession, Synonym, Vocab, VocTerm, VocTermEMAPA, VocTermEMAPS
from mgipython.model import db
from mgipython.parse import emapaStageParser, splitSemicolonInput
from base_dao import BaseDAO

class VocTermDAO(BaseDAO):
    
    model_class = VocTerm
    
    def get_by_primary_id(self, id):
        """
        Returns a VocTerm object using its primary ID 
        (Not necessarily an MGI ID, could be MP: or GO:, etc
        """
        id = id.upper()
        #return VocTerm.query.filter_by(primaryid=id).first()
        accAlias = db.aliased(Accession)
        return VocTerm.query.join(accAlias, VocTerm.primaryid_object) \
                .filter(accAlias.accid==id).first()

    def _build_search_query(self, search_query):

        query = VocTerm.query
        
        if search_query.has_valid_param("_vocab_key"):
            query = query.filter(VocTerm._vocab_key==search_query.get_value("_vocab_key"))

        if search_query.has_valid_param("_term_key"):
            query = query.filter(VocTerm._term_key==search_query.get_value("_term_key"))

        query = query.order_by(VocTerm.term)
        
        return query
        
    def search_emapa_terms(self,
                         termSearch="",
                         stageSearch="",
                         isobsolete=0,
                         limit=None):
        """
        Default is to ignore obsolete terms
        """
        
        
        emapaVocabName = "EMAPA"
        
        query = VocTerm.query
        
        if isobsolete != None:
            query = query.filter(VocTerm.isobsolete==isobsolete)
        
        # Filter only EMAPA terms
        vocab_alias = db.aliased(Vocab)
        query = query.join(vocab_alias, VocTerm.vocab).filter(vocab_alias.name==emapaVocabName)
        
        if stageSearch:
            
            stages = emapaStageParser(stageSearch)
            
            if stages:
                
                stages = [int(stage) for stage in stages]
                
                emapa_alias = db.aliased(VocTermEMAPA)
                emaps_alias = db.aliased(VocTermEMAPS)
                sub_term = db.aliased(VocTerm)
                
                sq = db.session.query(sub_term) \
                    .join(emapa_alias, sub_term.emapa_info) \
                    .join(emaps_alias, emapa_alias.emaps_infos) \
                    .filter(emaps_alias._stage_key.in_(stages)) \
                    .filter(sub_term._term_key==VocTerm._term_key) \
                    .correlate(VocTerm)
                
                query = query.filter(sq.exists())
        
        
        if termSearch:
            
            # do something
            
            termSearch = termSearch.lower()
            termsToSearch = splitSemicolonInput(termSearch)
            
            # query IDs, terms, and synonyms then UNION all
            
            # search accession ID
            accession_alias = db.aliased(Accession)
            sub_term1 = db.aliased(VocTerm)
            
            id_sq = db.session.query(sub_term1) \
                    .join(accession_alias, sub_term1.all_accession_ids) \
                    .filter(db.func.lower(accession_alias.accid).in_(termsToSearch)) \
                    .filter(sub_term1._term_key==VocTerm._term_key) \
                    .correlate(VocTerm)
            
            # search terms
            sub_term2 = db.aliased(VocTerm)
            term_sq = db.session.query(sub_term2) \
                    .filter(db.or_(
                                   db.func.lower(VocTerm.term).like(term) for term in termsToSearch \
                            )) \
                    .filter(sub_term2._term_key==VocTerm._term_key) \
                    .correlate(VocTerm)
            
            # search synonyms
            synonym_alias = db.aliased(Synonym)
            sub_term3 = db.aliased(VocTerm)
                    
            synonym_sq = db.session.query(sub_term3) \
                    .join(synonym_alias, sub_term3.synonyms) \
                    .filter(db.or_(
                                   db.func.lower(synonym_alias.synonym).like(term) for term in termsToSearch \
                            )) \
                    .filter(sub_term3._term_key==VocTerm._term_key) \
                    .correlate(VocTerm)
            
            # perform union
            query1 = query.filter(id_sq.exists())
            query2 = query.filter(term_sq.exists())
            query3 = query.filter(synonym_sq.exists())
            query = query1.union(query2).union(query3)
            #query = query2
        
        # setting sort
        query = query.order_by(VocTerm.term.asc())
            
        # setting limit on number of returned references
        if limit:
            query = query.limit(limit) 
                       
        terms = query.all()
        
        return terms
    
