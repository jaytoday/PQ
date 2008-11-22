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



# Template paths
PROFILE_PATH = 'profile/'


class ViewProfile(webapp.RequestHandler):
  #View a profile
  def get(self):
    template_values = self.get_profile()
    if not template_values: return
    path = tpl_path(PROFILE_PATH +'profile_template.html')
    self.response.out.write(template.render(path, template_values))


  def get_profile(self):
		profile_path = self.request.path.split('/profile/')[1].lower()
		profile_path = profile_path.replace(' ','_')
		user = QuizTaker.gql('WHERE profile_path = :1', self.request.path.split('/profile/')[1].lower())
		try:
			user = user.get()
		except: self.redirect('/profile_not_found/') # if no user is found
		
		if self.session.logged_in(): 
		    if user.unique_identifier == self.session['user']: profile_owner = True
		else: profile_owner = False
		top_proficiencies = self.get_top_proficiencies(user) 
		return {'user': user, 'profile_owner': profile_owner, 'top_proficiencies': top_proficiencies}


      
  def get_top_proficiencies(self, user):
      print ""
      print user.levels
      
      


class EditProfile(webapp.RequestHandler):
  def get(self):
    if not self.session['user']: self.redirect('/login/') # login_required decorator
    user = QuizTaker.get_by_key_name(self.session['user'])
    edit_type = 'Edit'
    if not user: 
        user = register_user(self.session['user'], self.session['nickname'], self.session['email'])
        edit_type = 'Create'
        user = QuizTaker.get_by_key_name(self.session['user'])
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



