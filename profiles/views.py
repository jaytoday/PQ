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
from utils.random import sort_by_attr
from .model.user import Profile, QuizTaker
from accounts.methods import register_user, register_qt



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
		user = Profile.gql('WHERE profile_path = :1', self.request.path.split('/profile/')[1].lower())
		try:
			user = user.get()
		except: self.redirect('/profile_not_found/') # if no user is found
		
		profile_owner = False
		if self.session.logged_in(): 
		    if user.unique_identifier == self.session['user']: profile_owner = True
		qt = QuizTaker.get_by_key_name(user.unique_identifier)
		topic_levels = self.get_topic_levels(qt)
		level_cloud = self.make_cloud(topic_levels[0:9])
		range = 50
		depth = 50
		user = clean(user)
		return {'user': user, 'profile_owner': profile_owner, 
		        'top_levels': topic_levels[0:3], 'level_cloud': level_cloud,
		        'range': range, 'depth': depth }


      
  def get_topic_levels(self, qt):
      topic_levels = qt.topic_levels.fetch(100)
      return sort_by_attr(topic_levels, 'topic_level') # sort from greatest to least

      
  def make_cloud(self, topic_levels):
	level_cloud = []
	num = len(topic_levels)
	for tl in topic_levels:
		for n in range(num):
		   level_cloud.append(tl)
		num -= 1
	return level_cloud            


class EditProfile(webapp.RequestHandler):
  def get(self):
    if not self.session['user']: self.redirect('/login/') # login_required decorator
    user = Profile.get_by_key_name(self.session['user'])
    edit_type = 'Edit'
    if not user: 
        user = register_user(self.session['user'], self.session['nickname'], self.session['email'])
        qt = register_qt(self.session['user'])
        edit_type = 'Create'
        user = Profile.get_by_key_name(self.session['user'])
    user = clean(user)
    template_values = {'user': user, 'edit_type': edit_type, 'no_load': True}
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








def clean(user):
    return user
