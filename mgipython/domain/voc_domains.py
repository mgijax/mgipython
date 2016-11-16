from base_serializer import Field, Serializer
import logging

logger = logging.getLogger("mgipython.domain")

class VocTermDomain(Serializer):
    """
    Represents a choice in a vocabulary select list
    """    
    __fields__ = [
      Field("_term_key"),
      Field("abbreviation"),
      Field("term")
    ]

class VocTermEMAPSDomain(Serializer):
    __fields__ = [
      Field("_term_key"),
      Field("_emapa_term_key"),
      Field("_stage_key"),
      Field("emapa_term", conversion_class=VocTermDomain),
      Field("primaryid")
    ]

class EMAPATermDomain(Serializer):
    """
    Represents an EMAPA term for the EMAPA browser
    """
    
    __fields__ = [
      Field("_term_key"),
      Field("term"),
      Field("primaryid"),
      
      # computed fields
      Field("startstage"),
      Field("endstage"),
      
      # only used in search results
      Field("term_highlight"),
      Field("synonym_highlight")
    ]
    
    def get_startstage(self, term):
        return term.emapa_info.startstage
    
    def get_endstage(self, term):
        return term.emapa_info.endstage
    
    def get_term_highlight(self, term):
        
        # default to using raw term value
        term_highlight = term.term
        
        if hasattr(term, "term_highlight") and term.term_highlight:
            term_highlight = term.term_highlight
            
        return term_highlight
    
    
    
class DagNodeDomain(Serializer):
    """
    Represents a VocTerm in a DAG relationship
        consists of term info plus DAG edge label
    """
    
    __fields__ = [
      Field("_term_key"),
      Field("term"),
      Field("primaryid"),
      Field("edge_label")
    ]
    
    
    
    
class EMAPADetailDomain(Serializer):
    """
    Represents an EMAPA/S term detail for the EMAPA browser
    """
    
    __fields__ = [
      Field("_term_key"),
      Field("term"),
      Field("primaryid"),
      Field("vocabname"),
      Field("results_count"),
      
      # computed fields
      Field("startstage"),
      Field("endstage"),
      Field("theilerstage"),
      Field("dpcmin"),
      Field("dpcmax"),
      Field("synonyms"),
      Field("parent_nodes")
    ]
    
    def get_startstage(self, term):
        startstage = None
        if term.emapa_info:
            startstage =  term.emapa_info.startstage
        elif term.emaps_info:
            startstage = term.emaps_info.emapa_info.startstage
        return startstage
    
    def get_endstage(self, term):
        endstage = None
        if term.emapa_info:
            endstage =  term.emapa_info.endstage
        elif term.emaps_info:
            endstage = term.emaps_info.emapa_info.endstage
        return endstage
    
    def get_theilerstage(self, term):
        stage = None
        if term.emaps_info:
            stage = term.emaps_info._stage_key
        return stage
    
    def get_dpcmin(self, term):
        dpcmin = None
        if term.emaps_info:
            dpcmin = term.emaps_info.theilerstage.dpcmin
        return dpcmin
    
    def get_dpcmax(self, term):
        dpcmax = None
        if term.emaps_info:
            dpcmax = term.emaps_info.theilerstage.dpcmax
        return dpcmax
    
    def get_synonyms(self, term):
        return [s.synonym for s in term.synonyms]
    
    def get_parent_nodes(self, term):
        parent_nodes = []
        
        if term.dagnodes:
            dagnode = term.dagnodes[0]
            parent_edges = dagnode.parent_edges
            
            for edge in parent_edges:
                parent_node = edge.parent_node
                parent_term = parent_node.vocterm
                node = DagNodeDomain()
                node._term_key = parent_term._term_key
                node.term = parent_term.term
                node.edge_label = edge.label
                node.primaryid = parent_term.primaryid
                parent_nodes.append(node)
            
        return parent_nodes
        
    
    
    
