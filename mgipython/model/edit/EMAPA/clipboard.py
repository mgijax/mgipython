""" 
Edit the EMAPA clipboard

  Uses the Set, SetMember, and SetMemberEMAPA objects
"""
from mgipython.modelconfig import db
from ...core import *
from ...mgd import *


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
    
