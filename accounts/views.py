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
from utils.webapp.util import login_required

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
    if self.request.get('continue'): self.session['continue'] = self.request.get('continue')
    if self.request.get('test'):
        template_values['pre_test'] = "True"
        self.session['continue'] = '/test/' + self.request.get('test')    
    if self.session['user']: 
        if self.session['continue']: 
            self.redirect(self.session['continue'])
            del self.session['continue']
        else: self.redirect('/')
    if self.session['continue']: template_values['login_context'] = self.session['continue'].split('/')
    self.session['post_quiz'] = False
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
		  except: nickname = json['profile'].get('displayName', unique_identifier[-7:-1]) # TODO: whoops, your name is gibberish. 
		  try: email = json['profile']['email']
		  except: email = ''
		  logging.debug(json['profile'])
		  try: fullname = json['profile']['displayName']
		  except: fullname = nickname	  
		  self.session['unique_identifier'] = unique_identifier
		  self.session['nickname'] = nickname
		  self.session['email'] = email
		  self.session['fullname'] = fullname
		  self.session['user'] = registered(self.session['unique_identifier'])
		  if self.session['user'] is False: self.register_user()  # TODO: This should all be in transaction-esque block using db.put() 
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
    self.session['user'] = False
    if self.request.get('continue'):
      self.redirect(self.request.get('continue'))
    else:
        self.redirect('/preview/homepage')
        






class Redirect(webapp.RequestHandler):
  def get(self):
    redirect_path = self.request.path.split('/redirect/')[1]
    if redirect_path.split('/')[0] == 'from_quiz': return self.token_redirect()
    return False
        
        
        
  @login_required
  def token_redirect(self):
      token = self.request.path.split('/from_quiz/')[1]
      from utils.utils import set_flash
      self.set_flash = set_flash
      self.set_flash('post_quiz')
      from quiztaker.load_quiz import QuizSession
      quiz_session = QuizSession()
      quiz_session.update_scores(token, self.session['user'].unique_identifier) 
      #do other jobs to make sure profile is ready. proficiency level, (awards?)
      self.update_user_stats()
      self.redirect('/profile/' + self.session['user'].profile_path)

  def update_user_stats(self):
      from quiztaker.methods import ProficiencyLevels
      pl = ProficiencyLevels()
      from model.quiz import QuizTaker
      qt = QuizTaker.get_by_key_name(self.session['user'].unique_identifier)
      pl.set_for_user(qt)
      from accounts.methods import Awards
      awards = Awards()
      new_awards = awards.check_all(qt)
      if new_awards > 0: self.set_flash('new_award')
      from accounts.methods import Sponsorships
      sponsorships = Sponsorships()
      if new_sponsorships > 0: self.set_flash('new_sponsorship')
      new_sponsorships = sponsorships.check_all(qt)
