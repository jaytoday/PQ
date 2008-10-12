import unittest
from google.appengine.api import urlfetch
from google.appengine.api import apiproxy_stub_map
from google.appengine.api import urlfetch_stub
class AppEngineTestCase(unittest.TestCase):
    
    def setUp(self):
    	apiproxy_stub_map.apiproxy = apiproxy_stub_map.APIProxyStubMap()
    	apiproxy_stub_map.apiproxy.RegisterStub('urlfetch', urlfetch_stub.URLFetchServiceStub())
    def test_url_fetch(self):
        response = urlfetch.fetch('http://www.google.com')
        self.assertEquals(0, response.content.find(''))
