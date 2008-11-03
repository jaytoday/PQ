import logging
# Log a message each time this module get loaded.
logging.info('Loading %s', __name__)
import cgi
import wsgiref.handlers
import datetime, time
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from utils.utils import ROOT_PATH, tpl_path
import simplejson
from utils.gql_encoder import GqlEncoder, encode


# Template paths
QUIZTAKER_PATH = 'quiztaker/'
QUIZBUILDER_PATH = 'quizbuilder/'
DEV_PATH = 'dev/'



class Admin(webapp.RequestHandler):
  #Load admin page

  def get(self):

    template_values = {}
    path = tpl_path(DEV_PATH +'admin.html')
    self.response.out.write(template.render(path, template_values))
    



class LoadTopics(webapp.RequestHandler):


  def get(self):
	print ""
	json_file = open(ROOT_PATH + "/data/topics.json")
	json_str = json_file.read()
	newdata = simplejson.loads(json_str) # Load JSON file as object
	topics = []
	types = []
	for t in newdata:
	   topics.append(t)
	   print t['name']


	

	return
	template_values = {}
	path = tpl_path(DEV_PATH +'admin.html')
	self.response.out.write(template.render(path, template_values))
    
