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
    
