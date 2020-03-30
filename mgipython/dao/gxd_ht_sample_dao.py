from mgipython.service.helpers.date_helper import DateHelper
from mgipython.model import GxdHTSample
from mgipython.model import Accession
from mgipython.model import db
from .base_dao import BaseDAO

class GxdHTSampleDAO(BaseDAO):

    model_class = GxdHTSample


