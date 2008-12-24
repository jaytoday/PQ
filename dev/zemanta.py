import logging
import utils.simplejson as simplejson
from google.appengine.api import urlfetch
import urllib


GATEWAY = 'http://api.zemanta.com/services/rest/0.0/'
API_KEY = 'n5wfc2kjavepgz32qpmjp35d'


def request():
	args = {'method': 'zemanta.suggest',
			'api_key': API_KEY,
			'text': '''The Phoenix Mars Lander has successfully deployed its robotic arm and tested other instruments including a laser designed to detect dust, clouds, and fog. The arm will be used to dig up samples of the Martian surface which will be analyzed as a possible habitat for life.''',
			'return_categories': 'dmoz',
			'format': 'json'}            
			
			
	print ""
	print "Request text is:", args['text']
	args_enc = urllib.urlencode(args)
	fetch_page = urlfetch.fetch(GATEWAY, payload=args_enc, method="POST")
	output = simplejson.loads(fetch_page.content)
	print ""
	print ""
	
	for cat in output['categories']: print "this text is classified in the category: ", cat['name'], "with confidence: ", cat['confidence']
	print ""
	print ""
	for key in output['keywords']: print "this text has keywords category: ", key['name'], "with confidence: ", key['confidence']
	
	print ""
	print output
