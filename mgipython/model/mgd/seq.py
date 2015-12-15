# All models for the seq_* tables
from mgipython.modelconfig import db
from ..core import *

from voc import VocTerm


class SeqMarkerCache(db.Model,MGIModel):
    __tablename__ = "seq_marker_cache"
    
    _cache_key = db.Column(db.Integer, primary_key=True)
    _sequence_key = db.Column(db.Integer, mgi_fk("seq_sequence._sequence_key"))
    _marker_key = db.Column(db.Integer, mgi_fk("mrk_marker._marker_key"))
    _organism_key = db.Column(db.Integer)
    _logicaldb_key = db.Column(db.Integer, mgi_fk("acc_logicaldb._logicaldb_key"))
    accid = db.Column(db.String())
    rawbiotype = db.Column(db.String())
    _sequenceprovider_key = db.Column(db.Integer)
    _biotypeconflict_key = db.Column(db.Integer, mgi_fk("voc_term._term_key"))
    annotation_date = db.Column(db.DateTime)
    
    # constants
    # the biotype conflict term
    _biotypeconflict_yes_key = 5420767
    
    
    # column properties
    sequenceprovider = db.column_property(
                db.select([VocTerm.term]).
                where(VocTerm._term_key==_sequenceprovider_key)
        )
    
    
    marker = db.relationship("Marker")
    
    logicaldb_obj = db.relationship("LogicalDb")
    
    @property
    def sequence_url(self):
        """
        This requires loading logicaldb_obj
            and logicaldb_obj.actualdb
        """
        url = ""
        if self.logicaldb_obj and \
            self.logicaldb_obj.actualdb:
            
            url = self.logicaldb_obj.actualdb.url.replace("@@@@", self.accid)
        
        return url
    

class SeqSourceAssoc(db.Model,MGIModel):
    __tablename__ = "seq_source_assoc"
    _assoc_key = db.Column(db.Integer, primary_key=True)
    _sequence_key = db.Column(db.Integer, mgi_fk("seq_sequence._sequence_key"))
    _source_key = db.Column(db.Integer, mgi_fk("prb_source._source_key"))    
                  
    
class Sequence(db.Model,MGIModel):
    __tablename__ = "seq_sequence"
    _sequence_key = db.Column(db.Integer, primary_key=True)
    _sequencetype_key = db.Column(db.Integer)
    _sequencequality_key = db.Column(db.Integer)
    _sequencestatus_key = db.Column(db.Integer)
    _sequenceprovider_key = db.Column(db.Integer)
    _organism_key = db.Column(db.Integer, mgi_fk("mgi_organism._organism_key"))
    
    length = db.Column(db.String())
    description = db.Column(db.String())
    version = db.Column(db.String())
    division = db.Column(db.String())
    
    # constants
    _mgitype_key = 19
    
    
    # column definitions
    type = db.column_property(
                db.select([VocTerm.term]).
                where(VocTerm._term_key==_sequencetype_key)
        )
    
    
    #relationships
    markers = db.relationship("Marker",
        secondary=SeqMarkerCache.__table__,
        primaryjoin="Sequence._sequence_key==SeqMarkerCache._sequence_key",
        secondaryjoin="SeqMarkerCache._marker_key==Marker._marker_key",
        foreign_keys="[Sequence._sequence_key,Marker._marker_key]",
        backref="sequences"
    )
    
    # sequence can have multiple IDs
    accession_objects = db.relationship("Accession",
        primaryjoin="and_(Accession._object_key==Sequence._sequence_key,"
                    "Accession.preferred==1,"
                    "Accession._mgitype_key==%s)" % (_mgitype_key),
        foreign_keys="[Accession._object_key]",
        order_by="Accession.accid"
    )
    
    source = db.relationship("ProbeSource",
        secondary=SeqSourceAssoc.__table__,
        uselist=False
    )
    
    
    