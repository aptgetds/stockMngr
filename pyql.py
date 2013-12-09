import urllib2
import json

'''
The module provides Python API to retreive stock information from Yahoo! Finance
using Yahoo Query Language.

The module uses Yahoo Query API, and sends REST to retrieve JSON, then converts
the result in a list of dictionary objects, and returns it.


Basic Usage:
   >>> import pyql
   >>> list = ['FFIV', 'MSFT', 'GOOG']
   >>> print pyql.lookup(list)
   >>> list = ['AAPL']
   >>> print pyql.lookup(list)
   
   
   
'''

class Pyql:
    pass

def lookup(symbols):
    yql = "select * from yahoo.finance.quotes where symbol in (" \
                    + '\'' \
                    + '\',\''.join( symbols ) \
                    + '\'' \
                    + ")"
                    
    url = "http://query.yahooapis.com/v1/public/yql?q=" \
            + urllib2.quote( yql ) \
            + "&format=json&env=http%3A%2F%2Fdatatables.org%2Falltables.env&callback="
    
    try: 
        result = urllib2.urlopen(url)
    except urllib2.HTTPError, e:        
        print ("HTTP error: ", e.code)        
    except urllib2.URLError, e:
        print ("Network error: ", e.reason)
       
    data = json.loads( result.read() )
    jsonQuotes = data['query']['results']['quote']
    
    # To make sure the function returns a list
    pythonQuotes = []
    if type( jsonQuotes ) == type ( dict() ):
        pythonQuotes.append( jsonQuotes )
    else:
        pythonQuotes = jsonQuotes
    
    return pythonQuotes
