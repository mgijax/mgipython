"""
cache of marker feature type 
DAG Tree
"""
from mgipython.model import VocTerm, DagNode
from mgipython.util.dag import DagBuilder
from mgipython.modelconfig import db

# constants
FEATURE_TYPE_VOCAB_NAME = "Marker Category"
FEATURE_TYPE_ROOT = "all feature types"


def getFeatureTypeDag():
    
    return _loadFeatureTypeDag()
    
def _loadFeatureTypeDag():
    """
    Loads the Feature Type DAG terms
    and builds a DAG tree
    """
    dagtree = None
    
    # get root term
    rootTerm = VocTerm.query.filter_by(
                    vocabname=FEATURE_TYPE_VOCAB_NAME,
                    term=FEATURE_TYPE_ROOT).first()
    
    if rootTerm and rootTerm.dagnodes:
        dagtree = DagBuilder.buildDagTreeFromRoot(rootTerm.dagnodes[0])

	for node in dagtree['root'].tree_list:
	    db.session.expunge(node.dagnode)
	    db.session.expunge(node.dagnode.vocterm)
    
    return dagtree
    
