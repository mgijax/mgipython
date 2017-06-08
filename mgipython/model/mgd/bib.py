# All models for the bib_* tables
from mgipython.modelconfig import db
from ..core import *
from acc import Accession, AccessionReference
from voc import *

class ReferenceCitationCache(db.Model,MGIModel):
    __tablename__ = "bib_citation_cache"
    _refs_key = db.Column(db.Integer, mgi_fk("bib_refs._refs_key"), primary_key=True)
    citation = db.Column(db.String)
    short_citation = db.Column(db.String)
    

class Reference(db.Model,MGIModel):
    __tablename__ = "bib_refs"
    _refs_key = db.Column(db.Integer, primary_key=True)
    _referencetype_key = db.Column(db.Integer())
    authors = db.Column(db.String())
    _primary = db.Column(db.String())
    title = db.Column(db.String())
    # this is a way to fix unicode.decode errors, but has a slight performance cost
    abstract = db.Column(db.String(convert_unicode='force',unicode_error="ignore"))
    journal = db.Column(db.String())
    year = db.Column(db.Integer())
    date = db.Column(db.Integer())
    isreviewarticle = db.Column(db.Integer())
    #date.quote=False
    vol = db.Column(db.Integer())
    issue = db.Column(db.Integer())
    pgs = db.Column(db.Integer())
    
    # constants
    _mgitype_key=1    
    expressionImageClass = "6481781"
    _referencetype_vocab_key = 131

    # mapped columns

    # must use db.relationship or unit test will fail
    reftype = db.relationship("VocTerm",
                primaryjoin="Reference._referencetype_key==VocTerm._term_key",
                foreign_keys="[VocTerm._term_key]",
                uselist=False)

    jnumid = db.column_property(
        db.select([Accession.accid]). \
        where(db.and_(Accession._mgitype_key==_mgitype_key, 
            Accession.prefixpart=='J:', 
            Accession._object_key==_refs_key)) 
    )

    pubmedid = db.column_property(
         db.select([Accession.accid]). \
         where(db.and_(Accession._mgitype_key==_mgitype_key, 
             Accession._logicaldb_key==29, 
             Accession._object_key==_refs_key)) 
    )
    
    # Relationships
    
    # accessions
    # backref defined in Accession class
    
    citation_cache = db.relationship("ReferenceCitationCache", uselist=False)

    gxd_images = db.relationship("Image",
        primaryjoin="and_(Image._refs_key==Reference._refs_key, "
                        "Image._imageclass_key == %s) " % expressionImageClass,
        foreign_keys="[Image._refs_key]"
    )
    
    jnumid_object = db.relationship("Accession",
            primaryjoin="and_(Accession._object_key==Reference._refs_key,"
                            "Accession.prefixpart=='J:',"
                            "Accession.preferred==1,"
                            "Accession._logicaldb_key==1,"
                            "Accession._mgitype_key==%d)" % _mgitype_key,
            foreign_keys="[Accession._object_key]",
            uselist=False)
    
    pubmedid_object = db.relationship("Accession",
            primaryjoin="and_(Accession._object_key==Reference._refs_key,"
                            "Accession.preferred==1,"
                            "Accession._logicaldb_key==29,"
                            "Accession._mgitype_key==%d)" % _mgitype_key,
            foreign_keys="[Accession._object_key]",
            uselist=False)
    
    # explicit_alleles
    # backref defined in Allele class
    
    # explicit_markers
    # backref defined in Marker class
    
    # all_markers
    # backref defined in Marker class
    
    experiment_notechunks = db.relationship("MLDReferenceNoteChunk")
    
    expression_assays = db.relationship("Assay",
        primaryjoin="Reference._refs_key==Assay._refs_key",
        foreign_keys="[Assay._refs_key]",
        backref=db.backref("reference", uselist=False))
    
    # mapping_experiments
    # backref in MappingExperiment class
    
    # antibodypreps
    # backref in AntibodyPrep class

    @property
    def volume(self):
        return self.vol

    @property
    def primaryAuthor(self):
        return self._primary

    @property
    def citation(self):
        authors = self.authors or ''
        title = self.title or ''
        journal = self.journal or ''
        rdate = self.date or ''
        vol = self.vol or ''
        issue = self.issue or ''
        pgs = self.pgs or ''
        
        return "%s, %s, %s %s;%s(%s):%s"% \
            (authors,title,journal, \
            rdate,vol,issue,pgs)
            
    @property
    def experimentnote(self):
        return "".join([nc.note for nc in self.experiment_notechunks])
            
    @property
    def short_citation(self):
        primary = self._primary or ''
        journal = self.journal or ''
        rdate = self.date or ''
        vol = self.vol or ''
        issue = self.issue or ''
        pgs = self.pgs or ''
        return "%s, %s %s;%s(%s):%s" % (primary, journal,
                rdate, vol, issue, pgs)

    def __repr__(self):
        return "<Reference %s,%s>"%(self.title,self.authors)
