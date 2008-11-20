import logging
# Log a message each time this module get loaded.
logging.info('Loading %s', __name__)
import cgi
import wsgiref.handlers
import datetime, time
from utils.webapp import template
from google.appengine.ext import db
from google.appengine.api import users
from utils import webapp
from utils.utils import ROOT_PATH, tpl_path
import simplejson
from google.appengine.api import urlfetch
import urllib

# Template paths
ACCOUNTS_PATH = 'accounts/'



class Login(webapp.RequestHandler):
  def get(self):
    login_response = str('http://' + self.request._environ['HTTP_HOST'] + '/login/response')
    template_values = {'token_url': login_response }
    if self.request.get('error') == "true":
        template_values['error'] = "True"
    path = tpl_path(ACCOUNTS_PATH +'login.html')
    self.response.out.write(template.render(path, template_values))
    
     
    

class LoginResponse(webapp.RequestHandler):
		#RPX Response Handler
	def get(self):
		token = self.request.get('token')
		url = 'https://rpxnow.com/api/v2/auth_info'
		args = {
		  'format': 'json',
		  'apiKey': 'a36dbaa685c9356086c69b9923a637ecf33369bc',
		  'token': token
		  }
		r = urlfetch.fetch(url=url,
						   payload=urllib.urlencode(args),
						   method=urlfetch.POST,
						   headers={'Content-Type':'application/x-www-form-urlencoded'}
						   )
		json = simplejson.loads(r.content)
		if json['stat'] == 'ok':    
		  unique_identifier = json['profile']['identifier']
		  nickname = json['profile']['preferredUsername']
		  email = json['profile']['email']
		  # log the user in using the unique_identifier
		  # this should your cookies or session you already have implemented
		  
		  #self.log_user_in(unique_identifier)    
		  self.redirect('/preview/homepage')
		else:
		  self.redirect('/login?error=true')
		  

    
class Logout(webapp.RequestHandler):
  #Login
  def get(self):
    template_values = {'token_url': self.request.env}
    path = tpl_path(ACCOUNTS_PATH +'login.html')
    self.response.out.write(template.render(path, template_values))
    

