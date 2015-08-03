"""
Test the datainput Module
"""

import sys
import os
sys.path.insert(1, os.path.join(os.path.dirname(__file__), '..'))
# adjust the path for running the tests locally, so that it can find mgipython (i.e. 3 dirs up)
sys.path.insert(1, os.path.join(os.path.dirname(__file__), '../..'))

import unittest


# TODO(kstone): get testdb setting somewhere
server = os.environ['MGD_DBSERVER']
database = os.environ['MGD_DBNAME']
user = os.environ['MGD_DBUSER']
password = os.environ['MGD_DBSERVER']
user=os.environ['MGD_DBUSER']
passwordFile=os.environ['MGD_DBPASSWORDFILE']
password=''
with open(passwordFile, 'r') as f:
    password = f.readline()


from testdb import init_testdb

from mgipython.datainput import datainput

class DataInputTest(object):
    """
    super class for datainput tests
    """
    
    files = []
    deleteFiles = []
    
    def setUp(self):
        init_testdb.init(sourceServer=server,
                         sourceDbName=database,
                         user=user,
                         password=password)
        self.files = []
        self.deleteFiles = []
 
        
    def tearDown(self):
        
        # remove data
        delFilePointers = [open(f, 'r') for f in self.deleteFiles]
        try:
            datainput.processFiles(delFilePointers, deferConstraints=True)
        finally:
            # close delete files
            for fp in delFilePointers:
                fp.close()
            
            # delete created test files
            for f in self.files:
                os.remove(f)  
                pass
        
    def createUpdateFile(self,fileName,
                         dataRows,
                         columns,
                         modelName,
                         operation='Update',
                         defaultParams={}):
        """
        Creates a file for updating/inserting
        """
        
        # track fileNames for future cleanup/removal
        self.files.append(fileName)
            
        # create test data
        datainput.writeDataFile(fileName=fileName,
                                dataRows=dataRows,
                                columns=columns,
                                modelName=modelName,
                                operation=operation,
                                defaultParams=defaultParams)
        
        
        # if update op, make sure we create a delete file for later cleanup
        delFile = fileName + ".del"
        if operation.lower() == 'update':
            
            # don't create delete file if there are relative keys
            for col in columns:
                if '(' in col:
                    return
                
            self.deleteFiles.append(delFile)
            self.files.append(delFile)
            datainput.writeDataFile(fileName=delFile,
                                dataRows=dataRows,
                                columns=columns,
                                modelName=modelName,
                                operation='Delete',
                                defaultParams=defaultParams)
        
            
    def processFileNames(self, fileNames):
        """
        Run files through datainput processor
        """
        inputFiles = [open(f,'r') for f in fileNames]
        try:
            datainput.processFiles(inputFiles)
        finally:
            for fp in inputFiles:
                fp.close()


class DataInputGenericTest(DataInputTest, unittest.TestCase ):
    """
    Test the generic handler API
    """
        
    def testSimpleInsertDelete(self):
        
        
        from mgipython.model import DbInfo
        
        fileName = "test1.data.tmp"
        
        columns = ['public_version',
                 'product_name',
                 'schema_version',
                 'snp_schema_version',
                 'snp_data_version']
        
        dataRows = [['Test Version',
                  'Test Product',
                  'Test Schema',
                  'Test SNP',
                  'Test SNP Data Version']
                    ]
        
        model = 'DbInfo'
        
        self.createUpdateFile(fileName, dataRows, columns, model)

        # insert data
        self.processFileNames([fileName])
        
        # check data was inserted
        dbInfos = DbInfo.query.filter_by(public_version='Test Version').all()
        self.assertEquals(1, len(dbInfos))
        dbInfo = dbInfos[0]
        self.assertEquals('Test Product', dbInfo.product_name)
        self.assertEquals('Test Schema', dbInfo.schema_version)
        self.assertEquals('Test SNP', dbInfo.snp_schema_version)
        self.assertEquals('Test SNP Data Version', dbInfo.snp_data_version)
        
        # create delete file
        fileName = "test1.del.tmp"
        self.createUpdateFile(fileName, dataRows, columns, model, operation="Delete")
        
         # delete data
        self.processFileNames([fileName])
        
        # check data was removed
        dbInfos = DbInfo.query.filter_by(public_version='Test Version').all()
        self.assertEquals(0, len(dbInfos))
        
    def testSimpleInsertColumnOrderDifferent(self):
        
        
        from mgipython.model import DbInfo
        
        fileName = "test2.data.tmp"
        
        columns = ['snp_data_version',
                 'schema_version',
                 'snp_schema_version',
                 'product_name',
                 'public_version']
        
        dataRows = [[
                  'Test SNP Data Version',
                  'Test Schema',
                  'Test SNP',
                  'Test Product',
                  'Test Version']
                    ]
        
        model = 'DbInfo'
        
        # create test data
        self.createUpdateFile(fileName, dataRows, columns, model)

        # insert data
        self.processFileNames([fileName])
        
        # check data was inserted
        dbInfos = DbInfo.query.filter_by(public_version='Test Version').all()
        self.assertEquals(1, len(dbInfos))
        dbInfo = dbInfos[0]
        self.assertEquals('Test Product', dbInfo.product_name)
        self.assertEquals('Test Schema', dbInfo.schema_version)
        self.assertEquals('Test SNP', dbInfo.snp_schema_version)
        self.assertEquals('Test SNP Data Version', dbInfo.snp_data_version)
        
        
    def testSimpleInsertDefaultValues(self):
        
        
        from mgipython.model import DbInfo
        
        fileName = "test3.data.tmp"
        
        columns = [
                 'public_version',
                 'product_name',
                 'schema_version',
                 ]
        
        dataRows = [['Test Version',
                  'Test Product',
                  'Test Schema',]
                    ]
        
        model = 'DbInfo'
        
        defaultParams = {'snp_schema_version': 'Test SNP', 
                         'snp_data_version': 'Test SNP Data Version'}
        
        # create test data
        self.createUpdateFile(fileName, dataRows, columns, model,
                              defaultParams=defaultParams)

        # insert data
        self.processFileNames([fileName])
        
        # check data was inserted
        dbInfos = DbInfo.query.filter_by(public_version='Test Version').all()
        self.assertEquals(1, len(dbInfos))
        dbInfo = dbInfos[0]
        self.assertEquals('Test Product', dbInfo.product_name)
        self.assertEquals('Test Schema', dbInfo.schema_version)
        self.assertEquals('Test SNP', dbInfo.snp_schema_version)
        self.assertEquals('Test SNP Data Version', dbInfo.snp_data_version)
        
        
    def testSimpleInsertMultiples(self):
        
        
        from mgipython.model import DbInfo
        
        fileName = "test4.data.tmp"
        
        columns = ['public_version',
                 'product_name',
                 'schema_version',
                 'snp_schema_version',
                 'snp_data_version']
        
        dataRows = [['Test Version',
                  'Test Product',
                  'Test Schema',
                  'Test SNP',
                  'Test SNP Data Version'],
                    ['Test Version2',
                  'Test Product2',
                  'Test Schema2',
                  'Test SNP2',
                  'Test SNP Data Version2'],
                    ['Test Version3',
                  'Test Product3',
                  'Test Schema3',
                  'Test SNP3',
                  'Test SNP Data Version3']
                    ]
        
        model = 'DbInfo'
        
        self.createUpdateFile(fileName, dataRows, columns, model)

        # insert data
        self.processFileNames([fileName])
        
        # check data was inserted
        dbInfos = DbInfo.query. \
                filter(DbInfo.public_version.like('Test Version%')). \
                order_by(DbInfo.public_version). \
                all()
                    
        self.assertEquals(3, len(dbInfos))
        dbInfo = dbInfos[0]
        self.assertEquals('Test Product', dbInfo.product_name)
        self.assertEquals('Test Schema', dbInfo.schema_version)
        self.assertEquals('Test SNP', dbInfo.snp_schema_version)
        self.assertEquals('Test SNP Data Version', dbInfo.snp_data_version)
        dbInfo = dbInfos[1]
        self.assertEquals('Test Product2', dbInfo.product_name)
        self.assertEquals('Test Schema2', dbInfo.schema_version)
        self.assertEquals('Test SNP2', dbInfo.snp_schema_version)
        self.assertEquals('Test SNP Data Version2', dbInfo.snp_data_version)
        dbInfo = dbInfos[2]
        self.assertEquals('Test Product3', dbInfo.product_name)
        self.assertEquals('Test Schema3', dbInfo.schema_version)
        self.assertEquals('Test SNP3', dbInfo.snp_schema_version)
        self.assertEquals('Test SNP Data Version3', dbInfo.snp_data_version)
        
    def testSimpleUpdate(self):
        
        
        from mgipython.model import DbInfo
        
        fileName = "test5.data.tmp"
        
        columns = ['public_version',
                 'product_name',
                 'schema_version',
                 'snp_schema_version',
                 'snp_data_version']
        
        dataRows = [['Test Version',
                  'Test Product',
                  'Test Schema',
                  'Test SNP',
                  'Test SNP Data Version']
                    ]
        
        model = 'DbInfo'
        
        self.createUpdateFile(fileName, dataRows, columns, model)

        # insert data
        self.processFileNames([fileName])
        
        newDataRows = [['Test Version',
                  'Test Product UP',
                  'Test Schema UP',
                  'Test SNP UP',
                  'Test SNP Data Version UP']
                    ]
        
        fileName = "test5.update.tmp"
        
        self.createUpdateFile(fileName, newDataRows, columns, model)

        # update data
        self.processFileNames([fileName])
        
        # check data was inserted
        dbInfos = DbInfo.query.filter_by(public_version='Test Version').all()
        self.assertEquals(1, len(dbInfos))
        dbInfo = dbInfos[0]
        self.assertEquals('Test Product UP', dbInfo.product_name)
        self.assertEquals('Test Schema UP', dbInfo.schema_version)
        self.assertEquals('Test SNP UP', dbInfo.snp_schema_version)
        self.assertEquals('Test SNP Data Version UP', dbInfo.snp_data_version)
    
   
   
class DataInputAutoKeyTest(DataInputTest, unittest.TestCase ):
    """
    Test the primary key autoincrementing features 
    """
    def testGenPrimaryKey(self):
        
        
        from mgipython.model import MarkerType
        from mgipython.model import db
        
        # get maxKey before-hand
        maxKey = db.session.query(db.func.max(MarkerType._marker_type_key)).scalar() or 0
        
        fileName = "test6.data.tmp"
        
        columns = ['name']
        
        dataRows = [['Test Type1'],
                     ['Test Type2']
                    ]
        
        model = 'MarkerType'
        
        self.createUpdateFile(fileName, dataRows, columns, model)

        # insert data
        self.processFileNames([fileName])
        
        # check data was inserted
        mTypes = MarkerType.query.filter(MarkerType.name.like('Test Type%')).all()
        self.assertEquals(2, len(mTypes))
        self.assertEquals(maxKey + 1, mTypes[0]._marker_type_key)
        self.assertEquals('Test Type1', mTypes[0].name)
        self.assertEquals(maxKey + 2, mTypes[1]._marker_type_key)
        self.assertEquals('Test Type2', mTypes[1].name)
        
        
class DataInputUseAutoKeyTest(DataInputTest, unittest.TestCase ):
    """
    Test referencing generated primary keys
    """
    
    def setUp(self):
        DataInputTest.setUp(self)
        self.deleteFuncs = []
    
    def tearDown(self):
        DataInputTest.tearDown(self)
        
        from mgipython.model import db
        
        # do any extra tearDown deletes
        
        for deleteFunc in self.deleteFuncs:
            deleteFunc()
        
        db.session.commit()
        
    
    def testUseGeneratedKey(self):
        
        from mgipython.model import Vocab,VocTerm
        from mgipython.model import db
        
        def deleteFunc():
            # cleanup testUseGeneratedKey
            query = VocTerm.query.filter_by(term='TestGen Term1')
            query.delete(synchronize_session=False)
            
            query = Vocab.query.filter_by(name='TestGen Vocab')
            query.delete(synchronize_session=False)
            
        self.deleteFuncs.append(deleteFunc)
        
        # get maxKey before-hand
        maxKey = db.session.query(db.func.max(Vocab._vocab_key)).scalar() or 0
        newVocabKey = maxKey + 1
        
        vocabFile = "test7.vocab.tmp"
        
        vocabCols = ['_vocab_key(R)',
                   '_refs_key',
                   '_logicaldb_key',
                   'name']
        
        vocabRows = [[99,-1,-1,'TestGen Vocab'],
                    ]
        
        vocModel = 'Vocab'
        
        self.createUpdateFile(vocabFile, vocabRows, vocabCols, vocModel)
        
        termFile = "test7.vocterm.tmp"
        
        termCols = ['_vocab_key(R)',
                   'term']
        
        termRows = [[99,'TestGen Term1'],
                    ]
        
        termModel = 'VocTerm'
        
        self.createUpdateFile(termFile, termRows, termCols, termModel)

        # insert data
        self.processFileNames([vocabFile, termFile])
        
        # check data was inserted
        vocabs = Vocab.query.filter(Vocab.name=='TestGen Vocab').all()
        self.assertEquals(1, len(vocabs))
        self.assertEquals(newVocabKey, vocabs[0]._vocab_key)
        
        terms = VocTerm.query.filter(VocTerm.term=='TestGen Term1').all()
        self.assertEquals(newVocabKey, terms[0]._vocab_key)
        
    
    
        
def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(DataInputGenericTest))
    suite.addTest(unittest.makeSuite(DataInputAutoKeyTest))
    suite.addTest(unittest.makeSuite(DataInputUseAutoKeyTest))
    # add future test suites here
    return suite

if __name__ == '__main__':
    unittest.main()
