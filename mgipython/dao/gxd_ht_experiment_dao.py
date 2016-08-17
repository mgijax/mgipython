from mgipython.model import GxdHTExperiment
from mgipython.model import db
from base_dao import BaseDAO


class GxdHTExperimentDAO(BaseDAO):
    
    model_class = GxdHTExperiment
    
    def search(self, searchObject=None):

        query = GxdHTExperiment.query

        if searchObject.params.has_key("name"):
            name = searchObject.params["name"].lower()
            query = query.filter(db.func.lower(GxdHTExperiment.name).like(name))
            
        if searchObject.params.has_key("description"):
            description = searchObject.params["description"].lower()
            query = query.filter(db.func.lower(GxdHTExperiment.description).like(description))
            
        if searchObject.params.has_key("_createdby_key"):
            query = query.filter(GxdHTExperiment._createdby_key==searchObject.params["_createdby_key"])
        if searchObject.params.has_key("_modifiedby_key"):
            query = query.filter(GxdHTExperiment._modifiedby_key==searchObject.params["_modifiedby_key"])
        
        query = query.order_by(GxdHTExperiment._experiment_key)
        
        return query.all()
