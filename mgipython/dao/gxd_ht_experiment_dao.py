from mgipython.model import GxdHTExperiment
from mgipython.model import db
from base_dao import BaseDAO


class GxdHTExperimentDAO(BaseDAO):
    
    model_class = GxdHTExperiment
    
    def search(self, searchObject=None):

        query = GxdHTExperiment.query

        if searchObject.has_key("name"):
            name = searchObject["name"].lower()
            query = query.filter(db.func.lower(GxdHTExperiment.name).like(name))
            
        if searchObject.has_key("description"):
            description = searchObject["description"].lower()
            query = query.filter(db.func.lower(GxdHTExperiment.description).like(description))
            
        if searchObject.has_key("_createdby_key"):
            query = query.filter(GxdHTExperiment._createdby_key==searchObject["_createdby_key"])
        if searchObject.has_key("_modifiedby_key"):
            query = query.filter(GxdHTExperiment._modifiedby_key==searchObject["_modifiedby_key"])
        
        query = query.order_by(GxdHTExperiment._experiment_key)
        
        return query.all()
