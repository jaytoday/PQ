import logging
# Log a message each time this module get loaded.
logging.info('Loading %s', __name__)
import cgi
import wsgiref.handlers
import datetime, time
from utils.webapp import template
from google.appengine.ext import db
from google.appengine.api import users
from utils import webapp, simplejson
from utils.utils import ROOT_PATH, tpl_path 
from google.appengine.api import urlfetch
import urllib
from utils.appengine_utilities.sessions import Session

from methods import registered

# Template paths
ACCOUNTS_PATH = 'accounts/'



class Login(webapp.RequestHandler):
  def get(self):
    login_response = str('http://' + self.request._environ['HTTP_HOST'] + '/login/response')
    template_values = {'token_url': login_response, 'no_load': True }
    if self.request.get('error') == "true":
        template_values['error'] = "True"
    self.session = Session()
    if self.request.get('continue'): self.session['continue'] = self.request.get('continue')
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
		if json['stat'] != 'ok':
		  self.redirect('/login?error=true')
		else:    
		  try: unique_identifier = json['profile']['identifier']
		  except:
		      logging.debug(json)
		      self.redirect('/login?error=true')
		  try: nickname = json['profile']['preferredUsername']
		  except: nickname = ''
		  try: email = json['profile']['email']
		  except: email = ''
		  self.session = Session()
		  self.session['user'] = unique_identifier
		  self.session['nickname'] = nickname
		  self.session['email'] = email
		  if registered(self.session['user']) is False: self.redirect('/register')
		  else: 
		        self.session['continue'] = '/preview/homepage'
		        self.redirect(self.session['continue'])
		  
		  

    
class Logout(webapp.RequestHandler):
  def get(self):
    self.session = Session()
    self.session['user'] = False
    if self.request.get('continue'):
      self.redirect(self.request.get('continue'))
    else:
        self.redirect('/preview/homepage')
        



