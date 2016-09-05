from mgipython.error import NotFoundError
from mgipython.service_schema.search import SearchResults
from mgipython.util.urlreader import UrlReader, UrlResponse
from mgipython.service.helpers.json_helper import JsonHelper
import logging
import exceptions

logger = logging.getLogger('GxdHTRawSampleService')

class GxdHTRawSampleService():
    '''
    Is: the service for retrieving raw samples directly from ArrayExpress; only does 'search' operation.
    Note: We could factor the interaction with ArrayExpress out into a DAO, but that would be distinct
        from the current DAO classes that all deal with SQLAlchemy models (and it would only be read-only),
        so it seems like overkill at this point.
    '''
    
    def search(self, search_query):
        if not search_query.has_valid_param("experimentID"):
                raise Exception("%s.search requires an experimentID parameter" % self.__class__.__name__)

        url = 'http://www.ebi.ac.uk/arrayexpress/json/v3/experiments/%s/samples' % search_query.get_value("experimentID")
        urlreader = UrlReader()
        logger.debug("Preparing to read: %s" % url)

        response = urlreader.get(url)
        logger.debug("Read URL, status code (%s), content length(%d bytes)" % (response.statusCode, len(response.content)))
        if response.statusCode != 200:
            raise Exception("Bad status code (%d) received when retrieving samples" % response.statusCode)
        
        search_result = SearchResults()
        search_result.items = JsonHelper().fromJson(response.content)['experiment']['sample']
        search_result.total_count = len(search_result.items)
        
        return search_result

    def create(self, args):
        raise NotImplementedError("%s does not implement the create() method" % self.__class__.__name__)

    # Read
    def get(self, key):
        raise NotImplementedError("%s does not implement the get() method" % self.__class__.__name__)
 
    # Update
    def save(self, key, args):
        raise NotImplementedError("%s does not implement the save() method" % self.__class__.__name__)

    def delete(self, key):
        raise NotImplementedError("%s does not implement the delete() method" % self.__class__.__name__)
