"""
    Takes a VocTerm object for a given DAG
    and builds a structure of tree nodes 
    compatible with an mgitreeview browser
"""

from mgipython.model.query import batchLoadAttribute, batchLoadAttributeExists

def buildTreeView(vocTerm, 
                  dag=None, 
                  ignoreObsoletes=True):
    """
    Builds a tree views based on the given
        vocTerm.
        
    dag param not implemented yet.
    
    """
    
    tree = []
    
    startNode = {
        'id' : vocTerm.primaryid,
        'label' : vocTerm.term,
        'oc': 'open'
    }
        
    # expand startNode one level down
    children = buildChildNodes(vocTerm, ignoreObsoletes)
    if children:
        startNode['children'] = children
    
    superParentNode = buildParentNodes(vocTerm, startNode)
    
    tree = [superParentNode]
    return tree


def buildParentNodes(vocTerm, nodeObj, 
                     ignoreObsoletes=True):
    """
    returns parentNode, with all children
    filled in down to vocTerm
    
    recurses upward until we reach the top DAG node
    """
    
    defaultParent = None
    
    # check for a default parent
    if vocTerm.emapa_info:
        defaultParent = vocTerm.emapa_info.defaultparent
    elif vocTerm.emaps_info:
        defaultParent = vocTerm.emaps_info.defaultparent
    else:
        if vocTerm.dagnode and vocTerm.dagnode.parent_edges:
            defaultParent = vocTerm.dagnode.parent_edges[0].parent_node.vocterm
            
    if not defaultParent:
        # we have no parents, so must be at the top
        # return current nodeObj
        return nodeObj
        
    # now create new parent node and attach the child
    newNode = {
        'id': defaultParent.primaryid,
        'label': defaultParent.term,
        'oc': 'open'
    }
    
    children = buildChildNodes(defaultParent, ignoreObsoletes)
    if children:
        newNode['children'] = children
        
        # if we have siblings loaded, we have to 
        #    reset this child with the currently active node
        for i in range(len(children)):
            if children[i]['id'] == nodeObj['id']:
                children[i] = nodeObj
    else:
        newNode['children'] = [vocTerm]
    
    return buildParentNodes(defaultParent, newNode)
    
    


def buildChildNodes(vocTerm, 
                    ignoreObsoletes=True):
    """
    returns list of child nodes for given parent vocTerm
    """
    children = []
    # expand startNode one level down
    if vocTerm.dagnode:
        
        if vocTerm.dagnode.child_edges:
                        
            # pre-load needed relationships
            batchLoadAttribute(vocTerm.dagnode.child_edges, "child_node")
            batchLoadAttribute(vocTerm.dagnode.child_edges, "child_node.vocterm")
            childNodes = [edge.child_node for edge in vocTerm.dagnode.child_edges]
            batchLoadAttributeExists(childNodes, ["child_edges"])
                        
            childNodes.sort(key=lambda x: x.vocterm.term)
            
            for childNode in childNodes:
                childTerm = childNode.vocterm
                
                # skip if obsolete
                if ignoreObsoletes and childTerm.isobsolete:
                    continue
                
                children.append({
                    'id': childTerm.primaryid,
                    'label': childTerm.term
                })
                
                # check for future children expansion
                if (childNode.has_child_edges):
                    # set child node as expandable
                    children[-1]['ex'] = True
    

    return children

    