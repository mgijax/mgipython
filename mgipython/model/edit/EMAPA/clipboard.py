""" 
Edit the EMAPA clipboard

  Uses the Set, SetMember, and SetMemberEMAPA objects
"""
from mgipython.modelconfig import db
from ...core import *
from ...mgd import *
from ...query import batchLoadAttribute, performQuery
from mgipython.util.sort import smartAlphaCompare


# constants
EMAPA_CLIPBOARD_SET_KEY = 1046


def insertItem(_user_key, 
               _term_key, 
               _stage_key):
    """
    Inserts an EMAPA clipboard item
    """
    
    # create a new set member
    setMember = SetMember()
    
    ## set columns
    setMember._createdby_key = _user_key
    setMember._modifiedby_key = _user_key
    setMember._set_key = EMAPA_CLIPBOARD_SET_KEY
    setMember._object_key = _term_key
    
    ## get max key and sequencenum
    setMember._setmember_key = db.session.query(
                db.func.max(SetMember._setmember_key)+1) \
                .one()[0] or 1
        
    setMember.sequencenum = db.session.query(
                db.func.max(SetMember.sequencenum)+1) \
                .filter(SetMember._set_key==EMAPA_CLIPBOARD_SET_KEY) \
                .filter(SetMember._createdby_key==_user_key) \
                .one()[0] or 1
    

    # create a new set member EMAPA
    setMemberEMAPA = SetMemberEMAPA()
    
    ## set columns
    setMemberEMAPA._stage_key = _stage_key
    setMemberEMAPA._createdby_key = _user_key
    setMemberEMAPA._modifiedby_key = _user_key
    setMemberEMAPA._setmember_key = setMember._setmember_key
    
    ## get max key
    setMemberEMAPA._setmember_emapa_key = db.session.query(
                db.func.max(SetMemberEMAPA._setmember_emapa_key)+1) \
                .one()[0] or 1
    
    # add EMAPA to set member
    setMember.emapa = setMemberEMAPA
    
    db.session.add(setMember)
    db.session.flush()
    
    
def deleteItem(_setmember_key, _user_key=None):
    """
    Deletes an EMAPA clipboard item
    
    Also filters by _user_key if provided
    """
    
    query = SetMember.query.filter_by(_setmember_key=_setmember_key)
    
    if _user_key:
        query = query.filter_by(_createdby_key=_user_key)
    
    setMember = query.first()
    
    if setMember:
        
        setMember._object_key = None
        db.session.delete(setMember)
        db.session.flush()
    
    
    
def normalizeSequencenums(_user_key):
    """
    Normalizes all the sequencenum fields in
    the MGI_SetMember table for EMAPA
    
    This is necessary after you've done any number of 
        adds or deletes, because it can leave holes
        in the sequencenum order 
        e.g [1,2,5,9,10] becomes [1,2,3,4,5]
    """
    
    performQuery("""
        select MGI_resetSequenceNum(
                'MGI_SetMember',
                %d,
                %d
            )
    """ % (EMAPA_CLIPBOARD_SET_KEY, _user_key))
    
    
    
def sortItemsByAlpha(_user_key):
    """
    Sorts all EMAPA clipboard items
        where _createdby_key == _user_key
        
    Sort is by stage, then alpha on term
    """
    
    items = SetMember.query.filter_by(_set_key=EMAPA_CLIPBOARD_SET_KEY) \
        .filter_by(_createdby_key=_user_key) \
        .all()
        
    batchLoadAttribute(items, "emapa")
    batchLoadAttribute(items, "emapa_term")
        
    # sort
    _sortItemsByAlpha(items)
    
    
    db.session.add_all(items)
    db.session.flush()
    
    
    
# function for testing
def _sortItemsByAlpha(items):
    """
    Sort clipboard items by alpha
    returns nothing.
    
    Assigns new sequencenum for each item
    """
    
    # define the compare function
    def stageTermCompare(a, b):
        
        if a.emapa._stage_key != b.emapa._stage_key:
            return cmp(a.emapa._stage_key, b.emapa._stage_key)
        
        # user smart alpha for the term
        return smartAlphaCompare(a.emapa_term.term, b.emapa_term.term)
        
    # apply the sort
    items.sort(stageTermCompare)
    
    # assign sequencenum
    newSeqnum = 0
    for item in items:
        
        newSeqnum += 1
        item.sequencenum = newSeqnum
        
        