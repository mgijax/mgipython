from flask_login import current_user
from mgipython.model.query import batchLoadAttribute
from mgipython.service_schema import *
from mgipython.service.helpers import *
from mgipython.model import *
from mgipython.dao import *
from mgipython.domain import *
from mgipython.error import *
from dateutil import parser
from datetime import datetime
import re

class GxdGenotypeService():

    genotype_dao = GenotypeDAO()

    def search(self, search_query):
        search_result = self.genotype_dao.search(search_query)
        search_result.items = convert_models(search_result.items, GenotypeDomain)
        return search_result
