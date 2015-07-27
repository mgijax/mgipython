#!/usr/bin/env python
"""
Initialize the test database
"""

import sys,os.path
import os
import cmd
# adjust the path for running the tests locally, so that it can find mgipython (i.e. 2 dirs up)
sys.path.insert(1, os.path.join(os.path.dirname(__file__), '../..'))

import argparse
import subprocess
import shlex
import sqlalchemy.exc


#
# prefix appended to source database name
#    when creating testdb
TESTDB_SUFFIX = "__test"

def runCommand(command, expected_retcodes = 0, stdin = None): 
    """run a command and raise an exception if retcode not in expected_retcode""" 

    # we want expected_retcode to be a tuple but will manage integers 
    if type(expected_retcodes) == type(0): 
        expected_retcodes = (expected_retcodes,) 

    # we want the command to be a list, but accomodate when given a string 
    cmd = command 
#     if type(cmd) == type('string'): 
#         cmd = shlex.split(command) 
        
    proc = subprocess.Popen(cmd, 
                            stdin  = stdin, 
                            stdout = subprocess.PIPE, 
                            stderr = subprocess.PIPE,
                            shell=True) 

    out, err = proc.communicate() 

    if proc.returncode not in expected_retcodes: 
        # when nothing gets to stderr, add stdout to Detail 
        if err.strip() == '': 
            err = out 
        
        mesg  = 'Error [%d]: %s' % (proc.returncode, command) 
        mesg += '\nDetail: %s' % err 
        raise Exception, mesg 

    return proc.returncode, out, err 

# Exception classes
class InitializationException(Exception):
    """
    Error on testdb initialization
    """
    
# methods
    
def parseInput():
    """
    Parse the command line input
    returns server and dbname
    """
    parser = argparse.ArgumentParser(
        description='Initialize a test database based on source database'
    )
    parser.add_argument('server', type=str,
        help='Server Name/Host')
    
    parser.add_argument('source_dbname', type=str,
        help='Source Database Name')
    
    parser.add_argument('--rebuild',action='store_true',
        help='Force test database to rebuild from source database')

    args = parser.parse_args()
    return args


def init(sourceServer, sourceDbName, 
         user,
         password,
         forceReinit=False):
    """
    Initializes the test database if
        it does not exist
        unless forceReinit=True
    """
        
    testDbName = sourceDbName + TESTDB_SUFFIX
    
    os.environ['PGPASSWORD'] = password
    
    if forceReinit:
        dropTestDb(sourceServer, sourceDbName, user=user)
    
    
    createDatabaseEngine(server=sourceServer, database=testDbName,
                         user=user,password=password, trace=True)
    
    from mgipython.model import db
    print db.session.bind
    
    dbExists = _testDbExists()
    
    if not dbExists or forceReinit:
        
        createTestDb(sourceServer, sourceDbName, user=user)
        loadTestData()
    
    
    
def _testDbExists():
    """
    Return whether testdb exists
    """
    from mgipython.model import db
    
    try:
        db.session.connection()
    except sqlalchemy.exc.OperationalError,e:
        return False
    
    return True

def dropTestDb(sourceServer, sourceDbName,
               user):
    """
    Drop the test database
    """
    
    testDbName = sourceDbName + TESTDB_SUFFIX
    
    cmd = "psql -q -h %s -d postgres -U %s -c 'drop database if exists %s'" % \
        (sourceServer, user, testDbName)
        
    print cmd
    runCommand(cmd)    
    

def createTestDb(sourceServer, sourceDbName,
                 user,
                 schema='mgd'):
    """
    Create a new test database, based on source database
    """
    
    testDbName = sourceDbName + TESTDB_SUFFIX
    
    # create empty DB
    
    databaseCreateCmd = "psql -q -h %s -d postgres -U %s -c 'create database %s'" % \
        (sourceServer, user, testDbName)
        
    print databaseCreateCmd
    runCommand(databaseCreateCmd)
    
    
    # copy schema from source
    schemaCreateCmd = "pg_dump -h %s -U %s --schema='%s' -s %s | psql -h %s -U %s -d %s" % \
        (sourceServer, user, schema, sourceDbName, sourceServer, user, testDbName)
        
    print schemaCreateCmd
    runCommand(schemaCreateCmd)
    
    # grant perms
    schemaPermsCmd = "psql -q -h %s -d %s -U %s -c 'grant usage on schema %s to mgd_public'" % \
        (sourceServer, testDbName, user, schema)
    print schemaPermsCmd
    runCommand(schemaPermsCmd)
    
    schemaPermsCmd2 = "psql -q -h %s -d %s -U %s -c 'grant select on all tables in schema %s to mgd_public'" % \
        (sourceServer, testDbName, user, schema)
    print schemaPermsCmd2
    runCommand(schemaPermsCmd2)
    

def loadTestData():
    """
    Load the test data
    """
    
    from mgipython.datainput import datainput
    
    sourceDataDir = "data"
    
    inputFileNames = ['bib_reviewstatus.txt',
                  'acc_logicaldb.txt',
                  'acc_mgitype.txt',
                  'acc_accessionmax.txt',
                  'mgi_user.txt',
                  'bib_refs.txt',
                  'voc_vocab.txt',
                  'voc_term.txt']
    
    inputFileNames = ['%s/%s' % (sourceDataDir, f) for f in inputFileNames]
    inputFiles = [open(f,'r') for f in inputFileNames]
    
    try:
        datainput.processFiles(inputFiles, deferConstraints=True)
    finally:
        for f in inputFiles:
            f.close()
    

# setup a database engine
from mgipython.modelconfig import createDatabaseEngine

if __name__ == '__main__':
    
    config = parseInput()
    print config
    server = config.server
    source_dbname = config.source_dbname
    
    user=os.environ['MGD_DBUSER']
    passwordFile=os.environ['MGD_DBPASSWORDFILE']
    password=''
    with open(passwordFile, 'r') as f:
        password = f.readline()
    
    init(sourceServer=server, sourceDbName=source_dbname, 
         user=user,
         password=password, 
         forceReinit=config.rebuild)
    
    
