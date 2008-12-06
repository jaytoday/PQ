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
from utils.utils import ROOT_PATH, tpl_path, Debug 
from google.appengine.api import urlfetch
import urllib
from utils.appengine_utilities.sessions import Session

from methods import registered, register_user, register_qt, register_account

# Template paths
ACCOUNTS_PATH = 'accounts/'
if Debug(): RPX_API_KEY = '081f35f427b90c6ed3415256e8d934ed8d01b11e'
else: RPX_API_KEY = 'a36dbaa685c9356086c69b9923a637ecf33369bc'
RPX_API_KEY = 'a36dbaa685c9356086c69b9923a637ecf33369bc'  #### TODO: dev key should work.
DEFAULT_LANDING_PAGE = '/preview/homepage'



class Login(webapp.RequestHandler):
  def get(self):
    login_response = str('http://' + self.request._environ['HTTP_HOST'] + '/login/response')
    template_values = {'token_url': login_response, 'no_load': True }
    self.session = Session()
    if self.request.get('continue'): self.session['continue'] = self.request.get('continue')
    if self.request.get('test'):
        template_values['test'] = "True"
        self.session['continue'] = '/test/' + self.request.get('test')    
    if self.session['user']: 
        if self.session['continue']: 
            self.redirect(self.session['continue'])
            del self.session['continue']
            
        else: self.redirect('/')
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
		  'apiKey': RPX_API_KEY,
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
		  logging.debug(json['profile'])
		  try: fullname = json['profile']['displayName']
		  except: fullname = nickname	  
		  self.session = Session()
		  self.session['unique_identifier'] = unique_identifier
		  self.session['nickname'] = nickname
		  self.session['email'] = email
		  self.session['fullname'] = fullname
		  if registered(self.session['unique_identifier']) is False: self.register_user()  # This should all be in transaction. 
		  else: 
		        if not self.session['continue']: self.session['continue'] = DEFAULT_LANDING_PAGE
		        self.redirect(self.session['continue'])
		  
	def register_user(self):		  
		self.session['account'] = register_account(self.session['unique_identifier'], self.session['nickname'])
		self.session['user'] = register_user(self.session['unique_identifier'], self.session['nickname'], self.session['fullname'], self.session['email'])
		self.session['quiz_taker'] = register_qt(self.session['unique_identifier'], self.session['nickname'])
		self.session['create_profile'] == True
		if self.session['continue']:
			self.redirect(self.session['continue'])
		else: self.redirect('/register')		  

    
class Logout(webapp.RequestHandler):
  def get(self):
    self.session = Session()
    self.session['user'] = False
    if self.request.get('continue'):
      self.redirect(self.request.get('continue'))
    else:
        self.redirect('/preview/homepage')
        



