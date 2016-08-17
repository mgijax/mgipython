from mgipython.model import GxdHTExperiment
from mgipython.model import db
from base_dao import BaseDAO


class GxdHTExperimentDAO(BaseDAO):
    
    model_class = GxdHTExperiment
    
    def _build_search_query(self, search_query):

        query = GxdHTExperiment.query

        if search_query.has_valid_param("name"):
            name = search_query.get_value("name")
            name = name.lower()
            query = query.filter(db.func.lower(GxdHTExperiment.name).like(name))

        if search_query.has_valid_param("description"):
            description = search_query.get_value("description")
            description = description.lower()
            query = query.filter(db.func.lower(GxdHTExperiment.description).like(description))
            
        query = query.order_by(GxdHTExperiment._experiment_key)
        
        return query
