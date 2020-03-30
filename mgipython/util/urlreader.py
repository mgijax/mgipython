'''
Name: urlreader.py
Purpose: to provide a convenient way to download data via a URL
'''

import urllib.request, urllib.error, urllib.parse
import base64

# globals
DEFAULT_TIMEOUT = 120       # 2 minutes

class UrlResponse:
    '''
    results of reading data from a URL; exposes public instance variables:
        statusCode - HTTP status code
        content - the text returned
        headers - the HTTP headers, as a dictionary-like object
        finalUrl - the eventual URL that returned a response (in case of redirection)
    '''
    def __init__ (self):
        self.statusCode = None
        self.content = None
        self.headers = None
        self.finalUrl = None
        return 

class UrlReader:
    '''
    reads data from URLs, constructs and returns a UrlResponse object for each call
    '''

    def __init__(self, params = {}):
        '''
        params - dictionary of name:value pairs, recognizing names:
            timeout : integer number of seconds
        '''
        self.timeout = DEFAULT_TIMEOUT
        if 'timeout' in params:
            self.timeout = int(params['timeout'])

        return
    
    def get(self, url, username = None, password = None, headers = None):
        '''
        read data from the given 'url', using the given 'username' and 'password' (optionally) to log in.
        'headers' can by a python dictionary of HTTP header name : value pairs to submit to the server.
        '''
        request = urllib.request.Request(url)

        if headers:
            for (name, value) in list(headers.items()):
                request.add_header(name, value)

        if username and password:
            request.add_header('Authorization', 'Basic ' + base64.b64encode('%s:%s' % (username, password)))

        rawResponse = urllib.request.urlopen(request, None, self.timeout)
        
        response = UrlResponse()
        response.statusCode = rawResponse.getcode()
        response.finalUrl = rawResponse.geturl()
        response.headers = rawResponse.headers
        response.content = rawResponse.read()
        
        return response
        