from Handler import *
from AccessionHandler import *
from AccessionReferenceHandler import *
from VocabHandler import *
from VocTermHandler import *
from VocAnnotHandler import *
from VocEvidenceHandler import *
from VocEvidencePropertyHandler import *
from MarkerTypeHandler import *
from mgipython import model
from mgipython.model.core import MGIModel

from sqlalchemy.orm.attributes import InstrumentedAttribute
import inspect


# init default model maps
for key,clazz in model.__dict__.items():
        
    if inspect.isclass(clazz)  \
        and clazz != MGIModel \
        and issubclass(clazz, MGIModel):
        
        # create generic handler
        
        # create column defs
        colDefs = []
        for prop in clazz.__dict__.values():
            # only map actual table columns, not relationships
            if type(prop) == InstrumentedAttribute \
                and hasattr(prop.property, 'columns') \
                and type(prop.property.columns[0]) == db.Column:
                colDef = ColumnDef(prop)
                colDefs.append(colDef)
            
        # create unique key settings
        unique_keys = []
        for column in clazz.__table__.primary_key.columns:
            unique_keys.append(column.key)
        
        genericHandler = type(key + "Handler",
                              (Handler,),
                              {
                               'DATA_TYPE': key,
                               'MODEL': clazz,
                               'COLUMNS': colDefs,
                               'UNIQUE_KEYS': unique_keys
                               })
        
        HANDLER_TYPE_MAP[key] = genericHandler

# init the Handler override maps

for handler in [AccessionHandler, AccessionReferenceHandler, 
                VocabHandler, VocTermHandler, MarkerTypeHandler,
                VocAnnotHandler, VocEvidenceHandler,VocEvidencePropertyHandler]:
    HANDLER_TYPE_MAP[handler.DATA_TYPE] = handler

