import logging
# Log a message each time this module get loaded.
logging.info('Loading %s', __name__)
import cgi
import wsgiref.handlers
import datetime, time
from utils.webapp import template
from google.appengine.ext import db
from utils import webapp
from utils.utils import ROOT_PATH, tpl_path

from .model.user import QuizTaker
from accounts.methods import register_user
from utils.appengine_utilities.sessions import Session


# Template paths
PROFILE_PATH = 'profile/'


class ViewProfile(webapp.RequestHandler):
  #View a profile
  def get(self):
    self.get_profile()
    template_values = {}
    path = tpl_path(PROFILE_PATH +'prototype.html')
    self.response.out.write(template.render(path, template_values))


  def get_profile(self):
      if len(self.request.path.split('/profile/')[1]) > 0:
         profile_path = self.request.path.split('/profile/')[1].lower()
         profile_path = profile_path.replace(' ','_')
         user = QuizTaker.gql('WHERE profile_path = :1', self.request.path.split('/profile/')[1].lower())
      if not user.get(): self.redirect('/profile_not_found/')
      return user
      



class EditProfile(webapp.RequestHandler):
  def get(self):
    self.session = Session()
    if not self.session['user']: self.redirect('/login/')
    
    user = QuizTaker.get_by_key_name(self.session['user'])
    edit_type = 'Edit'
    if not user: 
        user = register_user(self.session['user'], self.session['nickname'], self.session['email'])
        edit_type = 'Create'
    template_values = {'user': user, 'edit_type': edit_type}
    path = tpl_path(PROFILE_PATH +'edit.html')
    self.response.out.write(template.render(path, template_values))




  
      

class ViewEmployerProfile(webapp.RequestHandler):
  def get(self):
    template_values = {}
    path = tpl_path(PROFILE_PATH +'employer_prototype.html')
    self.response.out.write(template.render(path, template_values))
    


class BrowseProfiles(webapp.RequestHandler):
  def get(self):
    template_values = {}
    path = tpl_path(PROFILE_PATH +'browse_profiles.html')
    self.response.out.write(template.render(path, template_values))
    


class LoadUserProfile(webapp.RequestHandler):
  def get(self):
    if not self.request.get('user'): return False
    template_values = {}
    path = tpl_path(PROFILE_PATH + self.request.get('user') + '.html')
    self.response.out.write(template.render(path, template_values))
    







class PreviewViewProfile(webapp.RequestHandler):
  def get(self):

    template_values = {}
    path = tpl_path(PROFILE_PATH +'prototype.html')
    self.response.out.write(template.render(path, template_values))



