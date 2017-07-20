# All models for the bib_* tables
from mgipython.modelconfig import db
from ..core import *
from acc import Accession, AccessionReference
from mgipython.domain.reference_domains import WorkflowStatusDomain
from voc import *

AP_GROUP = "AP"                     # workflow group abbreviations
GO_GROUP = "GO"
GXD_GROUP = "GXD"
QTL_GROUP = "QTL"
TUMOR_GROUP = "Tumor"

NOT_ROUTED_STATUS = "Not Routed"    # workflow group statuses
ROUTED_STATUS = "Routed"
CHOSEN_STATUS = "Chosen"
REJECTED_STATUS = "Rejected"
INDEXED_STATUS = "Indexed"
FULLY_CURATED_STATUS = "Fully curated"

class ReferenceCitationCache(db.Model,MGIModel):
    __tablename__ = "bib_citation_cache"
    _refs_key = db.Column(db.Integer, mgi_fk("bib_refs._refs_key"), primary_key=True)
    citation = db.Column(db.String)
    short_citation = db.Column(db.String)
    
class ReferenceNoteChunk(db.Model, MGIModel):
    __tablename__ = "bib_notes"
    _refs_key = db.Column(db.Integer,
                          mgi_fk("bib_refs._refs_key"),
                          primary_key=True)
    sequencenum = db.Column(db.Integer, primary_key=True)
    note = db.Column(db.String())

class WorkflowStatus(db.Model, MGIModel):
    __tablename__ = 'bib_workflow_status'

    # constants
    workflow_group_vocab_key = 127
    workflow_status_vocab_key = 128

    # fields from database
    _assoc_key = db.Column(db.Integer, primary_key=True)
    _refs_key = db.Column(db.Integer, mgi_fk("bib_refs._refs_key"))
    iscurrent = db.Column(db.Integer)
    _group_key = db.Column(db.Integer)
    _status_key = db.Column(db.Integer)
    loaded = False
    
    # associated vocabulary terms
    groupVT = db.relationship("VocTerm",
        primaryjoin="and_(VocTerm._term_key==WorkflowStatus._group_key, "
            "VocTerm._vocab_key == %d) " % workflow_group_vocab_key,
        foreign_keys="[VocTerm._term_key]",
        uselist=False
    )

    statusVT = db.relationship("VocTerm",
        primaryjoin="and_(VocTerm._term_key==WorkflowStatus._status_key, "
            "VocTerm._vocab_key == %d) " % workflow_status_vocab_key,
        foreign_keys="[VocTerm._term_key]",
        uselist=False
    )
    
    def loadTerms(self):
        if not self.loaded:
            self.group = self.groupVT.term
            self.status = self.statusVT.term
            self.groupAbbreviation = self.groupVT.abbreviation
            self.loaded = True
        return

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
            Accession._logicaldb_key==1,
            Accession._object_key==_refs_key)) 
    )

    mgiid = db.column_property(
        db.select([Accession.accid]). \
        where(db.and_(Accession._mgitype_key==_mgitype_key, 
            Accession.prefixpart=='MGI:', 
            Accession._logicaldb_key==1,
            Accession._object_key==_refs_key)) 
    )

    pubmedid = db.column_property(
         db.select([Accession.accid]). \
         where(db.and_(Accession._mgitype_key==_mgitype_key, 
             Accession._logicaldb_key==29, 
             Accession._object_key==_refs_key)) 
    )

    doiid = db.column_property(
         db.select([Accession.accid]). \
         where(db.and_(Accession._mgitype_key==_mgitype_key, 
             Accession._logicaldb_key==65, 
             Accession._object_key==_refs_key)) 
    )
    
    gorefid = db.column_property(
         db.select([Accession.accid]). \
         where(db.and_(Accession._mgitype_key==_mgitype_key, 
             Accession._logicaldb_key==185, 
             Accession.private==1,
             Accession.preferred==0,
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
    
    doiid_object = db.relationship("Accession",
            primaryjoin="and_(Accession._object_key==Reference._refs_key,"
                            "Accession.preferred==1,"
                            "Accession._logicaldb_key==65,"
                            "Accession._mgitype_key==%d)" % _mgitype_key,
            foreign_keys="[Accession._object_key]",
            uselist=False)
    
    # note that GO_REF IDs are private and not preferred
    gorefid_object = db.relationship("Accession",
            primaryjoin="and_(Accession._object_key==Reference._refs_key,"
                            "Accession.private==1,"
                            "Accession.preferred==0,"
                            "Accession._logicaldb_key==185,"
                            "Accession._mgitype_key==%d)" % _mgitype_key,
            foreign_keys="[Accession._object_key]",
            uselist=False)
    
    mgiid_object = db.relationship("Accession",
            primaryjoin="and_(Accession._object_key==Reference._refs_key,"
                            "Accession.prefixpart=='MGI:',"
                            "Accession.preferred==1,"
                            "Accession._logicaldb_key==1,"
                            "Accession._mgitype_key==%d)" % _mgitype_key,
            foreign_keys="[Accession._object_key]",
            uselist=False)
    
    @property
    def reference_type(self):
        return self.reftype.term
 
    ###--- methods for getting the current status for each workflow group (for summary display) ---###
    
    current_statuses = db.relationship("WorkflowStatus",
            primaryjoin="and_(WorkflowStatus._refs_key==Reference._refs_key,"
                "WorkflowStatus.iscurrent == 1)",
            foreign_keys="[WorkflowStatus._refs_key]",
            uselist=True)

    @property
    def current_workflow_statuses(self):
        statuses = []
        for wfStatus in self.current_statuses:
            wfStatus.loadTerms()
            
            dom = WorkflowStatusDomain()
            dom.load_from_model(wfStatus)
            statuses.append(dom.serialize())
        return statuses
    
    def get_current_status(self, abbrev):
        for wfStatus in self.current_statuses:
            wfStatus.loadTerms()

            if wfStatus.groupAbbreviation == abbrev:
                return wfStatus.status
        return None
    
    @property
    def go_status(self):
        return self.get_current_status(GO_GROUP)

    @property
    def ap_status(self):
        return self.get_current_status(AP_GROUP)

    @property
    def qtl_status(self):
        return self.get_current_status(QTL_GROUP)

    @property
    def gxd_status(self):
        return self.get_current_status(GXD_GROUP)

    @property
    def tumor_status(self):
        return self.get_current_status(TUMOR_GROUP)

    ###--- methods for retrieving 1/0 flag for each status/workflow group pair (for detail display) ---###
    
    def group_has_status(self, abbrev, status):
        # returns 1 if the workflow group with the given abbreviation currently has the given status, 0 if not
        
        if self.get_current_status(abbrev) == status:
            return 1
        return 0
    
    # Fields for workflow status are formatted like status_<group abbreviation>_<status>, where the status has
    # spaces replaced by underscores.  A 1 value for one of these fields indicates the status is current for that
    # workflow group, while a 0 indicates it is not.

    @property
    def status_AP_Not_Routed(self):
        return self.group_has_status(AP_GROUP, NOT_ROUTED_STATUS)

    @property
    def status_AP_Routed(self):
        return self.group_has_status(AP_GROUP, ROUTED_STATUS)

    @property
    def status_AP_Chosen(self):
        return self.group_has_status(AP_GROUP, CHOSEN_STATUS)

    @property
    def status_AP_Rejected(self):
        return self.group_has_status(AP_GROUP, REJECTED_STATUS)

    @property
    def status_AP_Indexed(self):
        return self.group_has_status(AP_GROUP, INDEXED_STATUS)

    @property
    def status_AP_Fully_curated(self):
        return self.group_has_status(AP_GROUP, FULLY_CURATED_STATUS)

    @property
    def status_GO_Not_Routed(self):
        return self.group_has_status(GO_GROUP, NOT_ROUTED_STATUS)

    @property
    def status_GO_Routed(self):
        return self.group_has_status(GO_GROUP, ROUTED_STATUS)

    @property
    def status_GO_Chosen(self):
        return self.group_has_status(GO_GROUP, CHOSEN_STATUS)

    @property
    def status_GO_Rejected(self):
        return self.group_has_status(GO_GROUP, REJECTED_STATUS)

    @property
    def status_GO_Indexed(self):
        return self.group_has_status(GO_GROUP, INDEXED_STATUS)

    @property
    def status_GO_Fully_curated(self):
        return self.group_has_status(GO_GROUP, FULLY_CURATED_STATUS)

    @property
    def status_GXD_Not_Routed(self):
        return self.group_has_status(GXD_GROUP, NOT_ROUTED_STATUS)

    @property
    def status_GXD_Routed(self):
        return self.group_has_status(GXD_GROUP, ROUTED_STATUS)

    @property
    def status_GXD_Chosen(self):
        return self.group_has_status(GXD_GROUP, CHOSEN_STATUS)

    @property
    def status_GXD_Rejected(self):
        return self.group_has_status(GXD_GROUP, REJECTED_STATUS)

    @property
    def status_GXD_Indexed(self):
        return self.group_has_status(GXD_GROUP, INDEXED_STATUS)

    @property
    def status_GXD_Fully_curated(self):
        return self.group_has_status(GXD_GROUP, FULLY_CURATED_STATUS)

    @property
    def status_QTL_Not_Routed(self):
        return self.group_has_status(QTL_GROUP, NOT_ROUTED_STATUS)

    @property
    def status_QTL_Routed(self):
        return self.group_has_status(QTL_GROUP, ROUTED_STATUS)

    @property
    def status_QTL_Chosen(self):
        return self.group_has_status(QTL_GROUP, CHOSEN_STATUS)

    @property
    def status_QTL_Rejected(self):
        return self.group_has_status(QTL_GROUP, REJECTED_STATUS)

    @property
    def status_QTL_Indexed(self):
        return self.group_has_status(QTL_GROUP, INDEXED_STATUS)

    @property
    def status_QTL_Fully_curated(self):
        return self.group_has_status(QTL_GROUP, FULLY_CURATED_STATUS)

    @property
    def status_Tumor_Not_Routed(self):
        return self.group_has_status(TUMOR_GROUP, NOT_ROUTED_STATUS)

    @property
    def status_Tumor_Routed(self):
        return self.group_has_status(TUMOR_GROUP, ROUTED_STATUS)

    @property
    def status_Tumor_Chosen(self):
        return self.group_has_status(TUMOR_GROUP, CHOSEN_STATUS)

    @property
    def status_Tumor_Rejected(self):
        return self.group_has_status(TUMOR_GROUP, REJECTED_STATUS)

    @property
    def status_Tumor_Indexed(self):
        return self.group_has_status(TUMOR_GROUP, INDEXED_STATUS)

    @property
    def status_Tumor_Fully_curated(self):
        return self.group_has_status(TUMOR_GROUP, FULLY_CURATED_STATUS)

    # explicit_alleles
    # backref defined in Allele class
    
    # explicit_markers
    # backref defined in Marker class
    
    # all_markers
    # backref defined in Marker class
    
    experiment_notechunks = db.relationship("MLDReferenceNoteChunk")
    reference_notechunks = db.relationship("ReferenceNoteChunk")
    
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
    def pages(self):
        return self.pgs
    
    @property
    def experimentnote(self):
        return "".join([nc.note for nc in self.experiment_notechunks])
            
    @property
    def referencenote(self):
        return "".join([nc.note for nc in self.reference_notechunks])
            
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

    @property
    def isreviewarticleYN(self):
        if self.isreviewarticle == 0:
            return 'No'
        return 'Yes'


    def __repr__(self):
        return "<Reference %s,%s>"%(self.title,self.authors)
