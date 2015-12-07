# All models for the seq_* tables
from mgipython.modelconfig import db
from ..core import *

from voc import VocTerm


class SeqMarkerCache(db.Model,MGIModel):
    __tablename__ = "seq_marker_cache"
    
    _cache_key = db.Column(db.Integer, primary_key=True)
    _sequence_key = db.Column(db.Integer)
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
    