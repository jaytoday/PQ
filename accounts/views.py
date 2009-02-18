import logging
import cgi
import wsgiref.handlers
import datetime, time
from utils.webapp import template
from google.appengine.ext import db
from google.appengine.api import users
from utils import webapp, simplejson
from utils.utils import memoize, ROOT_PATH, tpl_path, Debug 
from google.appengine.api import urlfetch
import urllib
from utils.webapp.util import login_required, quiztaker_required

from accounts.methods import registered, register_user, register_qt, register_account

# Template paths
ACCOUNTS_PATH = 'accounts/'
if Debug(): RPX_API_KEY = '081f35f427b90c6ed3415256e8d934ed8d01b11e'
else: RPX_API_KEY = 'a36dbaa685c9356086c69b9923a637ecf33369bc'
RPX_API_KEY = 'a36dbaa685c9356086c69b9923a637ecf33369bc'  #### TODO: dev key doesn't work. ('data not found' error)
DEFAULT_LANDING_PAGE = '/'



class Login(webapp.RequestHandler):
  def get(self):
    logging.info('continue: %s', self.request.get('continue')) 
    login_response = str('http://' + self.request._environ['HTTP_HOST'] + '/login/response')
    template_values = {'token_url': login_response, 'no_quizlink': True}
    if self.request.get('continue'): self.session['continue'] = self.request.get('continue')
    if self.request.get('reset'): 
        self.session['user'] = False # log current user out, if logged in
        template_values = self.reset_account_access(template_values)
    
    """ TODO: test taking functionality -- not yet implemented. 
    if self.request.get('test'):
        template_values['pre_test'] = "True"
        self.session['continue'] = '/test/' + self.request.get('test')    
    """
    if self.session['user']: 
		if not self.session['continue']: self.session['continue'] = '/profile/' + self.session['user'].profile_path 
		self.redirect(self.session['continue'])
		self.session['continue'] = False
    #self.session['reset_account'] = False -- Why was this here? 
    if self.session['continue']: template_values['login_context'] = self.session['continue'].split('/')
    if self.request.get('sponsor'):
        template_values['login_context'] = "sponsor"
    self.session['post_quiz'] = False
    if self.request.get('error') == "true":
        template_values['error'] = "True"
    template_values['login_js'] = login_js(template_values)
    path = tpl_path(ACCOUNTS_PATH +'login.html')
    self.response.out.write(template.render(path, template_values))

         
  def reset_account_access(self, template_values):
    from model.user import Profile
    try: 
        self.session['reset_account'] = Profile.get(self.request.get('reset'))
        assert self.session['reset_account'] is not False
        logging.info('Presenting Reset Account Options for User %s', (self.session['reset_account'].email))
        template_values['login_context'] = "reset"
    except: 
        logging.warning('unable to use key %s for login shortcut', self.request.get('secret'))
        template_values['error'] = "True" # TODO change text of error?
    return template_values        

class LoginResponse(webapp.RequestHandler):
	#RPX Response Handler
	def get(self):
		logging.info('Loading Login Response')
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
		if self.validate_response(json):
		  if self.session['reset_account']:
		      from accounts.methods import reset_account
		      self.session['user'] = reset_account(self.session['reset_account'], json['profile']['identifier'])
		      self.session['reset_account'] = False
		  else: self.session['user'] = registered(json['profile']['identifier']) # check to see if this_user is registered
		  if self.session['user'] is False: return self.register_user(json) 
		  else: 
		        if not self.session['continue']: self.session['continue'] = '/profile/' + self.session['user'].profile_path 
		        self.redirect(self.session['continue'])
		        self.session['continue'] = False
		return




	def validate_response(self, json):	
		if json['stat'] != 'ok':
		  logging.error('unable login user with json response: %s',json) 
		  self.redirect('/login?error=true')
		  return False
		else:    
		  try: unique_identifier = json['profile']['identifier']
		  except:
			  logging.error('unable login user with json response: %s',json) 
			  self.redirect('/login?error=true')
			  return False
		return True
		      
		      		  
	def register_user(self, json):	
		try: nickname = json['profile']['preferredUsername']
		except: 
			  try:  nickname = json['profile'].get('displayName', json['profile']['email'].split('@')[0]) # try to get a nickname, somehow! 
			  except: nickname = ''
		email = json['profile'].get('email', '')
		fullname = json['profile'].get('displayName', nickname)
		self.session['unique_identifier'] = json['profile']['identifier']
		self.session['nickname'] = nickname
		self.session['email'] = email
		self.session['fullname'] = fullname
		from utils.utils import set_flash
		set_flash('fresh_register')  # didn't take quiz first
		self.redirect('/register')
		return
		


    
    
class Register(webapp.RequestHandler):
  def get(self):
		
		logging.info('Loading Registration Page')
		self.session['user'] = registered(self.session['unique_identifier']) 
		if self.session['user']: 
		                       logging.warning('user %s attempting to register while signed in', self.session['user'].unique_identifier) 
		                       if not self.session['continue']: self.session['continue'] = '/profile/' + self.session['user'].profile_path 
		                       self.redirect(self.session['continue'])
		                       self.session['continue'] = False
		if not self.session['unique_identifier']: # you should only be visiting this page after a redirect from login page
		     self.redirect('/login')
		     return False
		if self.request.get('nickname'): return self.create_user()
		nickname, email = None, None
		if self.session['nickname']: nickname = self.session['nickname']
		if self.session['email']: email = self.session['email']
		template_values = {'nickname': nickname, 'email': email, 'no_quizlink': True}
		template_values['register_js'] = register_js(template_values)
		path = tpl_path(ACCOUNTS_PATH +'signup.html')
		self.response.out.write(template.render(path, template_values))
		return

  def create_user(self):
        save = []
        if not self.request.get('nickname') and self.request.get('email'):
            self.response.out.write('nickname and email required')
            return 
        logging.info('Creating New User With Nickname %s', self.request.get('nickname'))
        try:
            int(self.session['unique_identifier'][0]) #check to see if it starts with an integer. key_names cant start with number.
            self.session['unique_identifier'] = "pq" + self.session['unique_identifier']
        except ValueError: pass #doesnt start with integer
        self.session['nickname'] = self.request.get('nickname')
        if not self.session['fullname']: self.session['fullname'] = self.session['nickname']
        self.session['email'] = self.request.get('email')
        self.session['account'] = register_account(self.session['unique_identifier'], self.session['nickname'], save=False)
        self.session['user'] = register_user(self.session['unique_identifier'], self.session['nickname'], self.session['fullname'], self.session['email'], save=False)
        self.session['quiz_taker'] = register_qt(self.session['unique_identifier'], self.session['nickname'], save=False)
        save.extend( (self.session['account'], self.session['user'], self.session['quiz_taker']) ) 
        db.put(save)
        from accounts.mail import mail_intro_message
        mail_intro_message(self.session['user'])
        self.redirect('/login')

	  
    
    
    
    
class Logout(webapp.RequestHandler):
  def get(self):
    logging.info('Logging Out User %s', self.session['nickname'])
    self.session.flush()
    if self.request.get('continue'):
      self.redirect(self.request.get('continue'))
    else:
        self.redirect(DEFAULT_LANDING_PAGE)
        






class Redirect(webapp.RequestHandler):
  def get(self):
    redirect_path = self.request.path.split('/redirect/')[1]
    if redirect_path.split('/')[0] == 'from_quiz': return self.from_quiz_redirect()
    if redirect_path.split('/')[0] == 'from_pledge': return self.from_pledge_redirect()
    return False
        
        
        
  @login_required
  @quiztaker_required
  def from_quiz_redirect(self):      # These occasionally time out. Try/Except solution for re-trying update. 
	# redirect after quiz
	logging.info('Redirecting From Quiz')
	token = self.request.path.split('/from_quiz/')[1]
	from utils.utils import set_flash
	self.set_flash = set_flash
	self.set_flash('post_quiz')
	from quiztaker.load_quiz import QuizSession
	quiz_session = QuizSession()
	quiz_session.update_scores(token, self.session['user'].unique_identifier) # re-assigns token scores to this user
	template_values = {'redirect_path': '/profile/' + self.session['user'].profile_path}
	path = tpl_path(ACCOUNTS_PATH +'post_quiz.html')
	self.response.out.write(template.render(path, template_values))      



      


  @login_required
  def from_pledge_redirect(self):
	logging.info('Redirecting from Sponsorship Pledge From User %s', self.session['user'].unique_identifier)
	if not self.session['pledge']: 
	    logging.error('Expired sponsor pledge call made by user %s', self.session['user'])
	    return False
	from accounts.methods import SponsorPledge
	sp = SponsorPledge()
	if sp.submit(self.session['pledge']): print "redirect me somewhere, please"
	else: print "there was a problem"
	#self.redirect('/profile/' + self.session['user'].profile_path) # I don't know...where else? 
  	



@memoize('login_js')
def login_js(template_values):
        path = tpl_path(ACCOUNTS_PATH   + 'scripts/login.js')
        from utils.random import minify 
        return minify( template.render(path, template_values) )



@memoize('register_js')
def register_js(template_values):
        path = tpl_path(ACCOUNTS_PATH  + 'scripts/register.js')
        from utils.random import minify 
        return minify( template.render(path, template_values) )

