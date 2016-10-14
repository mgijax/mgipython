# All models for the mgi_* tables
from mgipython.modelconfig import db
from ..core import *
from datetime import datetime

class Set(db.Model, MGIModel):
    __tablename__ = "mgi_set"
    _set_key = db.Column(db.Integer, primary_key=True)
    _mgitype_key = db.Column(db.Integer)
    name = db.Column(db.String())
    sequencenum = db.Column(db.Integer)
    _createdby_key = db.Column(db.Integer, default=1001)


class SetMember(db.Model, MGIModel):
    __tablename__ = "mgi_setmember"
    _setmember_key = db.Column(db.Integer, primary_key=True)
    _set_key = db.Column(db.Integer, mgi_fk("mgi_set._set_key"))
    _object_key = db.Column(db.Integer)
    sequencenum = db.Column(db.Integer)
    _createdby_key = db.Column(db.Integer, mgi_fk("mgi_user._user_key"))
    _modifiedby_key = db.Column(db.Integer, mgi_fk("mgi_user._user_key"))
    
    # constants
    _emapa_term_set_key = 1046
    
    # relationships
    emapa = db.relationship("SetMemberEMAPA",
        cascade="save-update, delete",
        uselist=False)
    
    emapa_term = db.relationship("VocTerm",
        primaryjoin="and_(VocTerm._term_key==SetMember._object_key,"
            "SetMember._set_key==%d)" % _emapa_term_set_key,
        foreign_keys="[SetMember._object_key]",
        uselist=False)


class SetMemberEMAPA(db.Model, MGIModel):
    __tablename__ = "mgi_setmember_emapa"
    _setmember_emapa_key = db.Column(db.Integer, primary_key=True)
    _setmember_key = db.Column(db.Integer, mgi_fk("mgi_setmember._setmember_key"))
    _stage_key = db.Column(db.Integer)
    _createdby_key = db.Column(db.Integer, default=1001)
    _modifiedby_key = db.Column(db.Integer, mgi_fk("mgi_user._user_key"))
    

class EmapSMapping(db.Model, MGIModel):
    __tablename__ = "mgi_emaps_mapping"
    _mapping_key = db.Column(db.Integer, primary_key=True)
    accid = db.Column(db.String())
    emapsid = db.Column(db.String())

class NoteType(db.Model,MGIModel):
    __tablename__ = "mgi_notetype"
    _notetype_key = db.Column(db.Integer,primary_key=True)
    notetype = db.Column(db.String())
    
class Note(db.Model,MGIModel):
    __tablename__ = "mgi_note"
    _note_key = db.Column(db.Integer,primary_key=True)
    _object_key = db.Column(db.Integer)
    _mgitype_key = db.Column(db.Integer)
    _notetype_key = db.Column(db.Integer)

    notetype = db.column_property(
                db.select([NoteType.notetype]).
                where(NoteType._notetype_key==_notetype_key)
        )  

    chunks = db.relationship("NoteChunk",
        order_by="NoteChunk.sequencenum")

    @property
    def text(self):
        return ''.join([c.note for c in self.chunks])

    def __repr__(self):
        return self.text
    
class NoteChunk(db.Model,MGIModel):
    __tablename__ = "mgi_notechunk"
    _note_key = db.Column(db.Integer,mgi_fk("mgi_note._note_key"),primary_key=True)
    sequencenum = db.Column(db.Integer,primary_key=True)
    #note = db.Column(db.String())
    note = db.Column(db.String(convert_unicode='force',unicode_error="ignore"))
    
    def __repr__(self):
        return self.note

class MGITypeOrganism(db.Model,MGIModel):
    __tablename__ = "mgi_organism_mgitype"
    _mgitype_key = db.Column(db.Integer, mgi_fk("acc_mgitype._mgitype_key"), primary_key=True)
    _organism_key = db.Column(db.Integer, mgi_fk("mgi_organism._organism_key"), primary_key=True)

class Organism(db.Model,MGIModel):
    __tablename__="mgi_organism"
    _organism_key = db.Column(db.Integer,primary_key=True)
    commonname = db.Column(db.String())
    mgitypes = db.relationship("MGIType", secondary=MGITypeOrganism.__table__, backref="organisms")

class ReferenceAssoc(db.Model, MGIModel):
    __tablename__ = "mgi_reference_assoc"
    _assoc_key = db.Column(db.Integer, primary_key=True)
    _refs_key = db.Column(db.Integer, mgi_fk("bib_refs._refs_key"))
    _object_key = db.Column(db.Integer)
    _mgitype_key = db.Column(db.Integer)
    _refassoctype_key = db.Column(db.Integer)

    reference = db.relationship("Reference",
        uselist=False
    )

class Property(db.Model,MGIModel):
    __tablename__ = "mgi_property"
    _property_key = db.Column(db.Integer, primary_key=True)
    _propertytype_key = db.Column(db.Integer, mgi_fk("voc_term._term_key"))
    type_object = db.relationship("VocTerm", primaryjoin="and_(Property._propertytype_key==VocTerm._term_key)", foreign_keys = "[VocTerm._term_key]", uselist=False)
    _propertyterm_key = db.Column(db.Integer, mgi_fk("voc_term._term_key"))
    term_object = db.relationship("VocTerm", primaryjoin="Property._propertyterm_key==VocTerm._term_key", foreign_keys = "[VocTerm._term_key]", uselist=False)
    _object_key = db.Column(db.Integer)
    _mgitype_key = db.Column(db.Integer)
    value = db.Column(db.String())
    sequencenum = db.Column(db.Integer)

class Synonym(db.Model,MGIModel):
    __tablename__ = "mgi_synonym"
    _synonym_key = db.Column(db.Integer,primary_key=True)
    _object_key = db.Column(db.Integer)
    _mgitype_key = db.Column(db.Integer)
    _synonymtype_key = db.Column(db.Integer)
    _refs_key = db.Column(db.Integer)
    synonym = db.Column(db.String())
    
    def __repr__(self):
        return self.synonym
    
class MGIUser(db.Model, MGIModel):
    __tablename__ = "mgi_user"
    _user_key = db.Column(db.Integer, primary_key=True)
    _usertype_key = db.Column(db.Integer, mgi_fk("voc_term._term_key"))
    _userstatus_key = db.Column(db.Integer, mgi_fk("voc_term._term_key"))
    login = db.Column(db.String())
    name = db.Column(db.String())
    #orcid = db.Column(db.String())
    _createdby_key = db.Column(db.Integer, default=1001)
    _modifiedby_key = db.Column(db.Integer, default=1001)
    creation_date = db.Column(db.DateTime, default=datetime.now)
    modification_date = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    
    usertype_object = db.relationship("VocTerm",
        primaryjoin="VocTerm._term_key==MGIUser._usertype_key",
        uselist=False)
    
    userstatus_object = db.relationship("VocTerm",
        primaryjoin="VocTerm._term_key==MGIUser._userstatus_key",
        uselist=False)
    
    user_roles = db.relationship("MGIRole",
        primaryjoin="MGIUser._user_key == MGIRole._user_key")
    
    # Properties for Flask-Login functionality
    def is_authenticated(self):
        return True
    
    def is_active(self):
        return True
    
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return self.login

class MGIRole(db.Model, MGIModel):

    __tablename__ = "mgi_userrole"
    _userrole_key = db.Column(db.Integer, primary_key=True)
    _role_key = db.Column(db.Integer, mgi_fk("voc_term._term_key"))
    _user_key = db.Column(db.Integer, mgi_fk("mgi_user._user_key"))
    
    role_object = db.relationship("VocTerm",
        primaryjoin="VocTerm._term_key==MGIRole._role_key",
        uselist=False)

    user_tasks = db.relationship("MGITask",
        primaryjoin="MGIRole._role_key == MGITask._role_key",
        foreign_keys="MGITask._role_key")

class MGITask(db.Model, MGIModel):
    __tablename__ = "mgi_roletask"
    _roletask_key = db.Column(db.Integer, primary_key=True)
    _role_key = db.Column(db.Integer, mgi_fk("voc_term._term_key"))
    _task_key = db.Column(db.Integer, mgi_fk("voc_term._term_key"))

    role_object = db.relationship("VocTerm",
        primaryjoin="VocTerm._term_key==MGITask._role_key",
        uselist=False)

    task_object = db.relationship("VocTerm",
        primaryjoin="VocTerm._term_key==MGITask._task_key",
        uselist=False)
   
    
class DbInfo(db.Model, MGIModel):
    __tablename__ = "mgi_dbinfo"
    public_version = db.Column(db.String(), primary_key=True)
    product_name = db.Column(db.String())
    schema_version = db.Column(db.String())
    snp_schema_version = db.Column(db.String())
    snp_data_version = db.Column(db.String())
    lastdump_date = db.Column(db.DateTime)
    creation_date = db.Column(db.DateTime, onupdate=datetime.now)
    modification_date = db.Column(db.DateTime, onupdate=datetime.now)
    
