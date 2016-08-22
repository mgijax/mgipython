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

        if search_query.has_valid_param("release_date"):
            release_date = search_query.get_value("release_date")

            # This following code needs to be pulled out into a parser in order to be use
            # on all date fields for searching
            if " " in release_date:
                [operator, date] = release_date.split(" ")
                if operator == ">":
                    query = query.filter(GxdHTExperiment.release_date > date)
                elif operator == "<":
                    query = query.filter(GxdHTExperiment.release_date < date)
                elif operator == ">=":
                    query = query.filter(GxdHTExperiment.release_date >= date)
                elif operator == "<=":
                    query = query.filter(GxdHTExperiment.release_date <= date)
            elif ".." in release_date:
                [date1, date2] = release_date.split("..")
                query = query.filter(GxdHTExperiment.release_date.between(date1, date2))
            else:
                query = query.filter(GxdHTExperiment.release_date == release_date)
            
        query = query.order_by(GxdHTExperiment._experiment_key)
        
        return query
