"""
	Contains core functions and classes for working with SQL Alchemy
"""
from mgipython.modelconfig import db
from sqlalchemy.inspection import inspect
from datetime import datetime

class Serializer(object):

    def serialize(self):
        dict = {}
        for c in inspect(self).attrs.keys():
            if c not in inspect(self).unloaded:
                if isinstance(getattr(self, c), list):
                    dict[c] = self.serialize_list(getattr(self, c))
                elif isinstance(getattr(self, c), unicode):
                    dict[c] = str(getattr(self, c))
                elif isinstance(getattr(self, c), datetime):
                    dict[c] = str(getattr(self, c))
                elif isinstance(getattr(self, c), float):
                    dict[c] = float(getattr(self, c))
                elif isinstance(getattr(self, c), int):
                    dict[c] = int(getattr(self, c))
                elif isinstance(getattr(self, c), str):
                    dict[c] = str(getattr(self, c))
                elif getattr(self, c) is None:
                    continue
                else:
                    dict[c] = getattr(self, c).serialize()
        return dict

    @staticmethod
    def serialize_list(l):
        return [m.serialize() for m in l]

class MGIModel(Serializer):
        __table_args__ = {"useexisting": True}
        __table_args__["schema"] = "mgd"
        # define a method to retrieve the current table subclass
        @classmethod
        def getSubClass(cls):
                return cls 
        # make this class iterable, and return the values of each column
        def __iter__(self):
                for col in getColumnNames(self.getSubClass()):
                        yield self.__getattribute__(col)
     
        @property
        def _primary_key(self):
                return getPrimaryKey(self)

def getPrimaryKey(object):
        return object.__mapper__.primary_key_from_instance(object)[0]

def mgi_table(tableName,*others):
        tableName = "mgd."+tableName
        table = db.Table(tableName,*others,quote=False)
        return table
def mgi_fk(fkString):
	fkString = "mgd."+fkString
	fk = db.ForeignKey(fkString)
	return fk

def getColumnNames(dbModel):
        colnames = []
        for colname,col in dbModel.__mapper__.columns.items():
                if not isColumnHidden(col):
                        colnames.append(colname)
        return colnames
# takes in a SQA column object
def isColumnHidden(col):
        return "hidden" in dir(col) and col.hidden

# for debugging
def printquery(statement, bind=None):
    """ 
    print a query, with values filled in
    for debugging purposes *only*
    for security, you should always separate queries from their values
    please also note that this function is quite slow
    """
    import sqlalchemy.orm
    if isinstance(statement, sqlalchemy.orm.Query):
        if bind is None:
            bind = statement.session.get_bind(
                    statement._mapper_zero_or_none()
            )   
        statement = statement.statement
    elif bind is None:
        bind = statement.bind 

    dialect = bind.dialect
    compiler = statement._compiler(dialect)
    class LiteralCompiler(compiler.__class__):
        def visit_bindparam(
                self, bindparam, within_columns_clause=False, 
                literal_binds=False, **kwargs
        ):  
            return super(LiteralCompiler, self).render_literal_bindparam(
                    bindparam, within_columns_clause=within_columns_clause,
                    literal_binds=literal_binds, **kwargs
            )   

    compiler = LiteralCompiler(dialect, statement)
    print compiler.process(statement)
    
