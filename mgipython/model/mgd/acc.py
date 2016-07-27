# All models for the acc_* tables
from mgipython.modelconfig import db
from ..core import *

class ActualDb(db.Model,MGIModel):
    __tablename__ = "acc_actualdb"
    _actualdb_key = db.Column(db.Integer, primary_key=True)
    _logicaldb_key = db.Column(db.Integer, mgi_fk("acc_logicaldb._logicaldb_key"))
    name = db.Column(db.String())
    url = db.Column(db.String())


class LogicalDb(db.Model,MGIModel):
    __tablename__ = "acc_logicaldb"
    _logicaldb_key = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    
    actualdbs = db.relationship("ActualDb")
    
    @property
    def actualdb(self):
        """
        Returns the first actualdb object
        """
        return self.actualdbs and self.actualdbs[0] or None
    
    
class AccessionReference(db.Model,MGIModel):
    __tablename__ = "acc_accessionreference"
    _accession_key = db.Column(db.Integer,
                        mgi_fk("acc_accession._accession_key"),
                        primary_key=True)
    _refs_key = db.Column(db.Integer,
                        mgi_fk("bib_refs._refs_key"),
                        primary_key=True)
    accession = db.relationship("Accession",
        uselist=False)
    
class Accession(db.Model,MGIModel):
    __tablename__ = "acc_accession"
    _accession_key = db.Column(db.Integer,primary_key=True)
    accid = db.Column(db.String())
    prefixpart = db.Column(db.String())
    numericpart = db.Column(db.Integer())
    _logicaldb_key = db.Column(db.Integer(), mgi_fk("acc_logicaldb._logicaldb_key"))
    _object_key = db.Column(db.Integer())
    _mgitype_key = db.Column(db.Integer())
    private = db.Column(db.Integer())
    preferred = db.Column(db.Integer())
    _createdby_key = db.Column(db.Integer())
    _modifiedby_key = db.Column(db.Integer())
    
    logicaldb = db.column_property(
            db.select([LogicalDb.name]).
            where(LogicalDb._logicaldb_key==_logicaldb_key)
    )
    
    
    # relationships
    
    logicaldb_object = db.relationship("LogicalDb",
        uselist=False)
    
    mgitype = db.relationship("MGIType",
        uselist=False,
        primaryjoin="MGIType._mgitype_key==Accession._mgitype_key",
        foreign_keys="[MGIType._mgitype_key]")
    
    marker = db.relationship("Marker",
                primaryjoin="Marker._marker_key==Accession._object_key",
                foreign_keys="Marker._marker_key",
                uselist=False
    )
    
    references = db.relationship("Reference",
                secondary=AccessionReference.__table__,
                backref="accessions")
    
    vocterm = db.relationship("VocTerm",
        primaryjoin="VocTerm._term_key==Accession._object_key",
        foreign_keys="VocTerm._term_key",
        uselist=False
    )
    
    def __repr__(self):
        return "<AccID %s>"%(self.accid,)
    
class MGIType(db.Model,MGIModel):
    __tablename__ = "acc_mgitype"
    _mgitype_key = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String())
    tablename = db.Column(db.String())
    primarykeyname = db.Column(db.String())
    
class AccessionMax(db.Model,MGIModel):
    __tablename__ = "acc_accessionmax"
    prefixpart = db.Column(db.String(),primary_key=True)
    maxnumericpart = db.Column(db.Integer())