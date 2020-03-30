from mgipython.model import Accession, Synonym, Vocab, VocTerm, VocTermEMAPA, VocTermEMAPS
from mgipython.model import db
from mgipython.parse import emapaStageParser, splitSemicolonInput
from .base_dao import BaseDAO

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
        
        if search_query.has_valid_param("isobsolete"):
            isobsolete = search_query.get_value("isobsolete")
            query = query.filter(VocTerm.isobsolete==isobsolete)
        
        if search_query.has_valid_param("_vocab_key"):
            query = query.filter(VocTerm._vocab_key==search_query.get_value("_vocab_key"))

        if search_query.has_valid_param("_term_key"):
            query = query.filter(VocTerm._term_key==search_query.get_value("_term_key"))
            
            
        if search_query.has_valid_param("term"):
            
            term = search_query.get_value("term")
            term = term.lower()
            
            query = query.filter(db.func.lower(VocTerm.term)==term)
            
            
        if search_query.has_valid_param("vocab_name"):
        
            vocab_name = search_query.get_value("vocab_name")
            vocab_name = vocab_name.lower()
            
            vocab_alias = db.aliased(Vocab)
            query = query.join(vocab_alias, VocTerm.vocab)
            query = query.filter(db.func.lower(vocab_alias.name)==vocab_name)
            
            
            
        # Specific to EMAPA Browser stage searching
        if search_query.has_valid_param('stageSearch'):
            
            stageSearch = search_query.get_value('stageSearch')
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
        
        
        # Specific to EMAPA Browser term searching
        if search_query.has_valid_param('termSearch'):
            
            termSearch = search_query.get_value('termSearch')
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


        # handle sorts
        sorts = []
        if len(search_query.sorts) > 0:
            
            for sort_name in search_query.sorts:
                
                if sort_name == "sequencenum":
                    sorts.append(VocTerm.sequencenum.asc())
                    
                elif sort_name == "term":
                    sorts.append(VocTerm.term.asc())
                    
        else:
            sorts.append(VocTerm.sequencenum.asc())
            
        query = query.order_by(*sorts)

        return query
        
        