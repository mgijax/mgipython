from mgipython.service.helpers.json_helper import JsonHelper
from mgipython.service_schema.search import SearchResults
from mgipython.util.urlreader import UrlReader, UrlResponse
import logging

logger = logging.getLogger('GxdHTRawSampleDAO')

class GxdHTRawSampleDAO():

    def download_raw_samples(self, experiment_primaryid):

        url = 'http://www.ebi.ac.uk/arrayexpress/json/v3/experiments/%s/samples' % experiment_primaryid
        urlreader = UrlReader()
        logger.debug("Preparing to read: %s" % url)

        response = urlreader.get(url)
        logger.debug("Read URL, status code (%s), content length(%d bytes)" % (response.statusCode, len(response.content)))
        if response.statusCode != 200:
            raise Exception("Bad status code (%d) received when retrieving samples" % response.statusCode)
        
        search_result = SearchResults()
        search_result.items = JsonHelper().fromJson(response.content)['experiment']['sample']
        search_result.items = self.consolidate_samples(search_result.items)
        search_result.total_count = len(search_result.items)
        
        return search_result

    def consolidate_samples(self, samples):
        return samples

