"""
    Defines an interface for
        handling data input files
"""

from mgipython.datainput.exception import FileInputException
from mgipython.modelconfig import db
from mgipython.util import batch_list

HANDLER_TYPE_MAP = {}

        
def getHandler(dataType, **kwargs):
    """
    Retrieve the correct handler based on dataType
    """
    handlerClass = HANDLER_TYPE_MAP[dataType]
    
    return handlerClass(**kwargs)


class Handler(object):
    """
    Defines how to load a data input file
    """
    
    # constants
    COLUMNS = []
    
    DATA_TYPE = None
    
    INSERT = 'insert'
    UPDATE = 'update'
    DELETE = 'delete'
    
    
    def __init__(self, filePointer,
                 columnDelim,
                 columnOrder,
                 defaultParams={},
                 opType='update',
                 relativeKeyMap={}):
        """
        setup the handler config
        """
        
        self.filePointer = filePointer
        self.columnDelim = columnDelim
        self.columnOrder = columnOrder
        self.defaultParams = defaultParams
        self.opType = opType
        self.colMap = []
        self.ops = []
        self.unified = False
        
        # map of relative columns, and their mapping from file keys
        #    to generated keys
        # ex:
        #    A file with _vocab_key(R) and values 1, 2, etc
        #    and max(_vocab_key) in DB of 98 
        #    would yield the following map:
        #    {"_vocab_key": {1: 99, 2: 100, etc}}
        self.relativeKeyMap = relativeKeyMap
        
        self._setup_colmap()
    
    def _setup_colmap(self):
        """
        setup the file column mapping
        """
        self.colMap = []
        for i in range(len(self.columnOrder)):
            colName = self.columnOrder[i]
            isRelative = False
            if '(R)' in colName:
                isRelative = True
                colName = colName[:-3]
            
            columnDef = None
            for colDefObject in self.COLUMNS:
                if colDefObject.name == colName:
                    columnDef = colDefObject
                    columnDef.lineNum = i
                    columnDef.isRelative = isRelative
            

            if not columnDef:
                raise FileInputException('Could not map \'%s\' to a %s Column Definition' % 
                                         (colName, self.DATA_TYPE))
                
            self.colMap.append(columnDef)
        
        for colName, value in self.defaultParams.items():
            if value:
                columnDef = None
                isRelative = False
                if '(R)' in colName:
                    isRelative = True
                    colName = colName[:-3]
                        
                for colDefObject in self.COLUMNS:
                    if colDefObject.name == colName:
                        columnDef = colDefObject
                        columnDef.default = value
                        columnDef.lineNum = -1
                        columnDef.isRelative = isRelative
            
                if not columnDef:
                    raise FileInputException('Could not map \'%s\' to a %s Column Definition' % 
                                         (key, self.DATA_TYPE))
                    
            self.colMap.append(columnDef)
    
    def validate(self):
        """
        Validate every row in the input file
            that has a config column
        """
        
        self.fileLength = 0
        
        uniqueKeys = self.getUniqueKeys()
        
        for row in self.filePointer:
            self.fileLength += 1
            l = row.split(self.columnDelim)
            for i in range(len(self.colMap)):
                colDef = self.colMap[i]
                colDef.validate(l)
                
        # reset the file pointer
        self.filePointer.seek(0)
        next(self.filePointer)
        next(self.filePointer)
        next(self.filePointer)
        
    def getUniqueKeys(self):
        """
        Return first set of uniqueKeys that is valid for this input file
        """
        
        
        
        #print "relMap = %s" % self.relativeKeyMap
        
        uniqueKeys = []
        availableColumns = []
        for c in self.columnOrder:
            if '(R)' in c:
                name = c.replace('(R)','')
                if name in self.relativeKeyMap:
                    availableColumns.append(name)
            else:
                availableColumns.append(c)
                
        availableColumns.extend([c for c in self.defaultParams.keys()])
        availableColumns = set(availableColumns)
        
        for uniqueKey in self.UNIQUE_KEYS:
            hasAllKeys = True
            if type(uniqueKey) == str:
                uniqueKey = [uniqueKey]
                
            for col in uniqueKey:
                hasAllKeys = hasAllKeys \
                    and (col in availableColumns)
                    
                    
            if hasAllKeys:
                uniqueKeys = uniqueKey
                break
        
        # map unique key names to column defs
        keyCols = []
        for uniqueKey in uniqueKeys:
            columnDef = None
            for colDefObject in self.COLUMNS:
                if colDefObject.name == uniqueKey:
                    columnDef = colDefObject
        
            if not columnDef:
                raise FileInputException('Could not map \'%s\' to a %s Column Definition' % 
                                     (colName, self.DATA_TYPE))
                
            keyCols.append(columnDef)
                    
        if not keyCols:
            # TODO(kstone): nonspecific exception handling
            raise FileInputException("""No valid set of unique columns for %s
                Need one of the following column/column sets:
                %s
                But only found %s""" % (self.filePointer.name, self.UNIQUE_KEYS, self.columnOrder))
            
        return keyCols
        
    def unify(self):
        """
        calculate database diff with file to see what needs
            to be added and what needs updates
        """
        
        self.ops = []
        
        # no need to unify delete operations
        if 'delete' in self.opType.lower():
            
            for i in range(self.fileLength):
                self.ops.append([self.DELETE, i])
            
            return
        
        batchSize = 100
        
        primaryCols = self.getUniqueKeys()
        
        for startIdx in range(0, self.fileLength, batchSize):
            endIdx = min(startIdx + batchSize, self.fileLength)
            
            pkLineMap = {}
            
            for i in range(startIdx, endIdx):
                
                row = next(self.filePointer).split(self.columnDelim)
                
                row = [c.strip() for c in row]
                
                row = self.assignRelativeKeys(row)
                
                # create the unique key for this row
                rowKey = None
                input = []
                for colDef in primaryCols:
                    val = colDef.val(row)
                    if colDef.isRelative and colDef.name not in self.relativeKeyMap:
                        continue
                        
                    if colDef.isDbType(db.String):
                        val = val.lower()
                    input.append(val)
                rowKey = tuple(input)
                
                pkLineMap[rowKey] = (i, row)
            
            # query all primary cols for data
            valueLists = []
            query = db.session.query(self.MODEL)
            for colDef in primaryCols:
                valueList = []
                
                for num, row in pkLineMap.values():
                    val = colDef.val(row)
                    if colDef.isDbType(db.String):
                        val = val.lower()
                        
                    if colDef.isRelative and colDef.name not in self.relativeKeyMap:
                        continue

                    valueList.append(val)
                    
                #print "%s valueList = %s" % (colDef.name, valueList)
                if colDef.isDbType(db.String):
                    query = query.filter(db.func.lower(colDef.column).in_(valueList))
                else:
                    query = query.filter(colDef.column.in_(valueList))
                
            data = query.all()
            
            
            # match data with file input
            
            pkDataMap = {}
            for row in data:
                
                pk = row._primary_key
                values = []
        
                for colDef in self.colMap:
                    values.append(getattr(row,colDef.name))

                 # create the unique key for this row
                key = None
                cols = []
                for colDef in primaryCols:
                    
                    # check if this is an auto-gen column
                    if colDef.isRelative and \
                        colDef.name not in self.relativeKeyMap \
                        and colDef.isPrimaryKey():
                        continue
                    
                    val = getattr(row, colDef.name)
                    if colDef.isDbType(db.String):
                        val = val.lower()
                    cols.append(val)
                    
                key = tuple(cols)
                
                pkDataMap[key] = values

            #print "\nprinting MAPS\n"
            #print pkLineMap
            #print pkDataMap
            for key, lineItems in pkLineMap.items():
                if key in pkDataMap:
                    data = pkDataMap[key]
                    inputRow = lineItems[1]
                    
                    for colDef in self.colMap:
                        if colDef.isRelative:
                            # map file key to database key
                            dataVal = 0
                            for i in range(len(self.colMap)):
                                if self.colMap[i].name == colDef.name:
                                    dataVal = data[i]
                                    
                            fileVal = colDef.val(inputRow)
                            
                            self.setRelativeValues(colDef, fileVal, dataVal)
                        
                        
                    if not self.dataEquals(dataRow=data, inputRow=inputRow):
                        self.ops.append([self.UPDATE, lineItems[0]])
                
                else:
                    self.ops.append([self.INSERT, lineItems[0]])
            
        self.ops.sort()
            
        # reset the file pointer
        self.filePointer.seek(0)
        next(self.filePointer)
        next(self.filePointer)
        next(self.filePointer)
        
        self.unified = True
            
            
    def load(self):
        """
        Load the preprocessed data file
        """
        if not self.unified:
            self.unify()
            
        if not self.ops:
            return
            
            
        opDict = {}
        for op in self.ops:
            opDict[op[1]] = op[0]
            
        batchSize = 100
        
        primaryCols = self.getUniqueKeys()
        
        # set maxKey if need to auto-generate primary keys
        if self.needGenPrimaryKey():
            self.maxKey = self.getMaxKey()
        else:
            self.maxKey = 0
        
        for startIdx in range(0, self.fileLength, batchSize):
            endIdx = min(startIdx + batchSize, self.fileLength)
        
            pkLineMap = {}
            
            for i in range(startIdx, endIdx):
                
                # no new data to insert/update for this line
                if i not in opDict:
                    continue
                    print "skipping line %d" % i
                    
                op = opDict[i]
                    
                row = next(self.filePointer).split(self.columnDelim)
                row = [c.strip() for c in row]
                
                row = self.assignRelativeKeys(row)
                
                if op == self.INSERT:
                    self.insertData(row)
                    
                elif op == self.UPDATE:
                    self.updateData(row)
                    
                elif op == self.DELETE:
                    self.deleteData(row)
        
        
    def insertData(self, dataRow):
        """
        Insert data for this dataRow
        """
        
        insertValues = {}
        for colDef in self.colMap:
            value = colDef.val(dataRow)

            # only insert actual table columns (not column_properties)
            if type(colDef.column.property.columns[0]) == db.Column:
                
                if colDef.isRelative and colDef.name not in self.relativeKeyMap:
                        # map file key to next gen key
                        dataVal = self.maxKey + 1
                        fileVal = value
                        self.setRelativeValues(colDef, fileVal, dataVal)
                        value = dataVal
                
                insertValues[colDef.name] = value
                
                
                
            elif colDef.foreignColumn:
                # use foreign key settings
                subQuery = db.select([colDef.foreignInsert])
                if colDef.isDbType(db.String):
                    subQuery = subQuery.where(db.func.lower(colDef.foreignMapping)==value.lower())
                else:
                    subQuery = subQuery.where(colDef.foreignMapping==value)
                    
                insertValues[colDef.foreignColumn.key] = subQuery.as_scalar()
                
        # Insert new maxKey if there is a single primary key column
        primaryKeys = self.MODEL.__mapper__.primary_key
        if len(primaryKeys) == 1:
            primaryKey = primaryKeys[0].key
            if primaryKey not in insertValues:
                insertValues[primaryKey] = self.maxKey + 1
                
        
        if insertValues:
            #print "insertValues = %s" % insertValues
            ins = self.MODEL.__table__.insert(values=insertValues)
            db.session.connection().execute(ins)
            self.maxKey += 1
        
        
    def updateData(self, dataRow):
        """
        Update data for this dataRow
        """
        query = db.session.query(self.MODEL)
        
        primaryCols = self.getUniqueKeys()
        

        valueLists = []
        for colDef in primaryCols:
            
            value = colDef.val(dataRow)
                
            if colDef.isDbType(db.String):
                query = query.filter(db.func.lower(colDef.column)==value.lower())
            else:
                query = query.filter(colDef.column==value)
        
        updateValues = {}
        for colDef in self.colMap:
            if colDef.updatable:
                value = colDef.val(dataRow)
                
                updateValues[colDef.name] =  value
                
        if updateValues:
            #print "updateValues = %s" % updateValues
            query.update(values=updateValues,synchronize_session=False)
        else:
            raise Exception("cannot update row with no updatable fields %s" % dataRow)
        
        
    def deleteData(self, dataRow):
        """
        delete data rows by primaryKey
        """
        
        query = db.session.query(self.MODEL)
        
        primaryCols = self.getUniqueKeys()
        
        valueLists = []
        for colDef in primaryCols:
            
            if colDef.isRelative:
                # TODO(kstone): better exception class
                raise FileInputException("Cannot delete data with relative column %s, for %s handler" % \
                                         (colDef.name, self.DATA_TYPE))
            
            value = colDef.val(dataRow)
                
            if colDef.isDbType(db.String):
                query = query.filter(db.func.lower(colDef.column)==value.lower())
            else:
                query = query.filter(colDef.column==value)
        
        query.delete(synchronize_session=False)
    
    
    def getMaxKey(self):
        """
        get maxKey from DB
        """
        primaryKeys = self.MODEL.__mapper__.primary_key
        if primaryKeys and len(primaryKeys) == 1:
            maxKey = db.session.query(db.func.max(primaryKeys[0])).scalar()
            if not maxKey:
                maxKey = 0
            if not isinstance(maxKey, (int, long, float, complex)):
                maxKey = 0
            return maxKey
        else:
            # TODO(kstone): better error class
            raise FileInputException("Max key not supported for this handler")
        
    def needGenPrimaryKey(self):
        """
        If we need to auto-generate any primary keys
        """
        primaryColumns = [c.key for c in self.MODEL.__table__.primary_key.columns]

        hasAllPrimaries = True
        for primaryColumn in primaryColumns:
            hasPrimary = False
            for column in self.columnOrder:
                if '(R)' in column:
                    column = column.replace('(R)','')
                    if column not in self.relativeKeyMap:
                        continue
                    
                if column == primaryColumn:
                    hasPrimary = True
            hasAllPrimaries = hasAllPrimaries and hasPrimary
            
        return not hasAllPrimaries
        
        
        
    def dataEquals(self,dataRow, inputRow):
        """
        Compare data row with input file row
            All updatable columns must match
        """
                    
        updatableColNums = []
        for i in range(len(self.colMap)):
            colDef = self.colMap[i]
            if colDef.updatable:
                inputVal = colDef.val(inputRow)
                if colDef.isDbType(db.Integer):
                    inputVal = int(inputVal)
                if dataRow[i] != inputVal:
                    return False
        
        return True
    
    def getRelativeValue(self, columnDef, value):
        """
        Check if row has a relative value mapped to it
        """
        if columnDef.name in self.relativeKeyMap:
            return self.relativeKeyMap[columnDef.name][value]
        else:
            if not columnDef.isPrimaryKey():
                # TODO(kstone): better exception class
                raise FileInputException("There are no generated keys to map for foreign key column %s" % \
                                         columnDef.name)
            return None
        
        
    def setRelativeValues(self, columnDef, fileVal, dataVal):
        """
        Set the mapping for this relative key
        """
        
        if columnDef.name not in self.relativeKeyMap:
            self.relativeKeyMap[columnDef.name] = {}
            
        self.relativeKeyMap[columnDef.name][fileVal] = dataVal
        
        
    def assignRelativeKeys(self, inputRow):
        """
        Assign any mapped relative keys to the inputRow
        """
        
        for i in range(len(self.colMap)):
            colDef = self.colMap[i]
            if colDef.isRelative and colDef.name in self.relativeKeyMap:
                val = self.getRelativeValue(colDef, colDef.val(inputRow))
                inputRow[i] = val
   
        return inputRow
    
class ColumnDef():
    """
    Defines a database column for the Handler
    
        column -- An SQLAlchemy Column object (E.g. VocTerm.term)
    
        default -- A default value for any input on this column.
            If this column is not provided, default is also used.
            NOTE: this overrides any sqlalchemy defaults
    
        updatable -- means this column is allowed 
            to be used to insert/update data
            
        foreignColumn -- An foreign key column to be used on inserts,
            This is appropriate for using column_properties as ColumnDefs. (E.g. VocTerm.vocabname)
            Used in conjunction with foreignMapping
            Example:
                column=VocTerm.vocabname
                foreignColumn=VocTerm._vocab_key
                foreignInsert=Vocab._vocab_key
                foreignSelect=Vocab.name
                
                Yields _vocab_key=(select _vocab_key from voc_vocab where name='<vocabname>')
                
        foreignInsert -- For foreign key subqueries, this value is inserted into MODEL table
            See foreignColumn documentation above for example
        
        foreignMapping -- For foreign key subqueries, this maps value of column to foreignColumn.
            See foreignColumn documentation above for example
            
        
    """
    
    def __init__(self, column, 
                 default=None,
                 updatable=True,
                 foreignColumn=None,
                 foreignInsert=None,
                 foreignMapping=None):
        self.column = column
        self.name = column.key
        self.default = default
        self.foreignColumn = foreignColumn
        self.lineNum = -1
        self.updatable = updatable
        self.foreignInsert = foreignInsert
        self.foreignMapping = foreignMapping
        self.isRelative = False
        
        
    def val(self, row):
        """
        Return the value of this column in the input row
        if no lineNum set or column is empty,
            use self.default as the value
        """
        val = ''
        if self.lineNum >= 0:
            val = row[self.lineNum]
            if not val and self.default!=None:
                val = self.default
                
        elif self.default:
            val = self.default
            
            
        if self.isDbType(db.Integer):
            val = int(val)
            
        return val
    
    def validate(self, row):
        """
        Validate a value based on this columndef
        """    
        value = self.val(row)
        # validate integer
        if self.isDbType(db.Integer):
            temp = int(value)
            
    def isDbType(self, sqaType):
        """
        Check column type against sqlalchemy generic types
        """
        return type(self.column.property.columns[0].type) == sqaType
    
    def isPrimaryKey(self):
        """
        Is this column a primary key of the table
        """
        
        try:
            return self.column.property.columns[0].primary_key
        except:
            return false
        return false
        