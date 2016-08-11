"""
This must be set up before using the model module
"""

from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_cache import Cache


#
# Global database engine
# this must be set before importing from model
#
db = None
# create a null cache by default
cache = Cache()


def createDatabaseEngine(server, database,
                         user, password,
                         trace=False):
    """
    Initializes a db engine using the provided 
        server, database, user, and password
        
    Used outside the context of a webapp
    """
    dburi = "postgresql+psycopg2://%s:%s@%s/%s"%(user,password,
        server,database)
    
    dummyApp = _createDummyAppFromUri(dburi, trace=trace)
    
    createDatabaseEngineFromApp(dummyApp)
    
    
def createDatabaseEngineFromApp(app, appCache=None):
    """
    Initializes a db engine using the provided 
        Flask app
        which should be configured by setting the
        app.config['SQLALCHEMY_DATABASE_URI']
        
    Used within context of a webapp
    
    Optionally pass in a Flask Cache object as appCache
    """
    global db
    global cache
    db = SQLAlchemy(app)
    if cache:
        cache = appCache
    
    
def createMockDatabaseEngine(trace=False):
    """
    Create a mock database engine for unit tests
    """
    dburi = 'sqlite://'
    
    dummyApp = _createDummyAppFromUri(dburi, trace=trace)
    
    createDatabaseEngineFromApp(dummyApp)
    
    
def _createDummyAppFromUri(dburi,trace=False):
    """
    Creates a dummy Flask app from a given dburi
    """
    # create a dummy app to attach to FlaskSQLAlchemy
    dummyApp = Flask("dummy")
    
    dummyApp.config['SQLALCHEMY_DATABASE_URI'] = dburi
    dummyApp.config['SQLALCHEMY_BINDS'] = {
        "mgd": dburi,
    }
    if trace:
        dummyApp.config['SQLALCHEMY_ECHO'] = True
        
    return dummyApp


