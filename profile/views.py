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
PROFILE_PATH = 'profile/'



class ViewProfile(webapp.RequestHandler):
  #Load admin page

  def get(self):

    template_values = {}
    path = tpl_path(PROFILE_PATH +'prototype.html')
    self.response.out.write(template.render(path, template_values))
    

class ViewEmployerProfile(webapp.RequestHandler):
  #Load admin page

  def get(self):

    template_values = {}
    path = tpl_path(PROFILE_PATH +'employer_prototype.html')
    self.response.out.write(template.render(path, template_values))
    


class BrowseProfiles(webapp.RequestHandler):
  #Load admin page

  def get(self):
    template_values = {}
    path = tpl_path(PROFILE_PATH +'browse_profiles.html')
    self.response.out.write(template.render(path, template_values))
    


class LoadUserProfile(webapp.RequestHandler):
  #Load admin page

  def get(self):
    user = self.request.get('user')
    template_values = {}
    path = tpl_path(PROFILE_PATH + user + '.html')
    self.response.out.write(template.render(path, template_values))
    


