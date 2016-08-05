# mgipython
Shared python modules and virtual environment installation

## Install

    cp Configuration.default Configuration
    -- make appropriate edits to Configuration 
    -- for Python executable and Postgres environment
    ./Install

1. Creates a virtual python environment locally.
2. Installs into local environment external modules used by MGI, such as Flask and SQLAlchemy.
3. Installs into local environment the mgipython shared library

## mgipython module
* Shared modules used by MGI products.
* Includes SQLAlchemy objects for accessing the MGD schema
* Includes datainput API for modifying MGD data

## Usage

    source Configuration
    source bin/activate
    python
    >import mgipython
    
## Software Requirements
* LD\_LIBRARY\_PATH=/opt/python/lib
* Python built with the following
* ssl
* zlib
    
### Using the model
To use the model you have to setup the modelconfig *before* importing any model or datainput classes. This attaches a database session to each model object.

    source Configuration
    source bin/activate
    python
    >from mgipython import modelconfig
    >modelconfig.createDatabaseEngine(
        server='localhost',
        database='pub',
        user='...',
        password='...')
    >from mgipython.model import Marker
    >marker = Marker.query.first()
    >print marker.symbol