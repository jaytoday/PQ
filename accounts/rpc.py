import logging
from utils import webapp, simplejson
from google.appengine.ext import db
from .utils.utils import tpl_path, ROOT_PATH
from utils.gql_encoder import GqlEncoder, encode
from utils.appengine_utilities.sessions import Session


class RPCHandler(webapp.RequestHandler):
  # AJAX Handler
  def __init__(self):
    webapp.RequestHandler.__init__(self)
    self.methods = RPCMethods()

 
  def get(self):
    func = None
   
    action = self.request.get('action')
    if action:
      if action[0] == '_':
        self.error(403) # access denied
        return
      else:
        func = getattr(self.methods, action, None)
   
    if not func:
      self.error(404) # file not found
      return
     
    args = ()
    while True:
      key = 'arg%d' % len(args)
      val = self.request.get(key)
      if val:
        args += (simplejson.loads(val),)
      else:
        break
    result = func(*args)
    self.response.out.write(simplejson.dumps(result))
    


class RPCMethods(webapp.RequestHandler):
  """ Defines AJAX methods.
  NOTE: Do not allow remote callers access to private/protected "_*" methods.
  """




  def SubmitProfileEdits(self, *args):
  	session = Session()
  	user = session['user']    
  	user.has_edited = True
  	user.fullname = args[0]
  	if len(args[1]) > 5:  user.email = args[1]
  	user.location = args[2]
  	if len(args[3]) > 8: 
		webpage = args[3]
		if 'http://' not in webpage: webpage = 'http://' + webpage
		try: user.webpage = webpage
		except: 
		      return "Webpage error"
  	user.work_status = args[4]
  	user.aboutme = args[5]
  	if len(args[6]) > 3:
  		from .model.user import ProfilePicture
  		user.photo = ProfilePicture.get(args[6])
  	user.put()
  	session['user'] = user # update profile info cached for session

		
	# add up all scores for a given quiztaker, and then rank them.
	return "OK"




  def SubmitSponsorPledge(self, *args):
  	 # check args 
  	 if len(args) < 4: return "error"
  	 # TODO: better checking!
  	 else:
  	 	session = Session()
  	 	session['pledge'] = args
  	 	return True



  	
  	
  def intro_mail_message(self, *args):
  	from model.user import Profile
  	from accounts.mail import mail_intro_message
  	profiles = Profile.all().fetch(10)
  	for p in profiles:
  		mail_intro_message(p)
  		


  def new_years_message(self, *args):
  	from accounts.mail import new_years_message
  	return new_years_message()
  		

  	
  	
  	
  	  	

  def nickname_check(self, *args):
	profile_path = args[0].lower()
	profile_path = profile_path.replace(' ','_')
	from model.user import Profile
	same_path = Profile.gql("WHERE profile_path = :1", profile_path).fetch(1)
	if same_path: return "not_available"
	else: return "available"


class Post(webapp.RequestHandler): 
  def post(self):
  	try:
		from utils.appengine_utilities.sessions import Session
		self.session = Session()
		if self.request.get('action') == 'reset': self.response.out.write(simplejson.dumps(  self.reset_account()  ))
		if self.request.get('action') == 'update_user_stats': self.response.out.write(simplejson.dumps(  self.update_user_stats()  ))  
		if self.request.get('action') == 'update_user_awards': self.response.out.write(simplejson.dumps(  self.update_user_awards()  ))
		if self.request.get('action') == 'update_user_sponsorships': self.response.out.write(simplejson.dumps(  self.update_user_sponsorships()  ))   
  	except:
  		print "Error"
  		return False 



  def reset_account(self):
  	from model.user import Profile
  	this_profile = Profile.gql("WHERE email = :1", self.request.get('email')).get()
  	if this_profile:
  		from accounts.mail import reset_account_access
  		reset_account_access(this_profile)
  		return "OK"	
	return "Profile Not Found"




  def update_user_stats(self):
      from quiztaker.methods import ProficiencyLevels
      pl = ProficiencyLevels()
      from model.quiz import QuizTaker
      qt = QuizTaker.get_by_key_name(self.session['user'].unique_identifier)
      logging.info('Updating Level Stats for User %s', self.session['user'].unique_identifier)
      db.put( pl.set_for_user(qt) )
      print "OK"
      return "OK"
      
  def update_user_awards(self):      
      from accounts.methods import Awards
      awards = Awards()
      # check for new awards
      logging.info('Updating Awards for User %s', self.session['user'].unique_identifier)
      from model.quiz import QuizTaker
      qt = QuizTaker.get_by_key_name(self.session['user'].unique_identifier)
      new_awards = awards.check_all(qt)
      if new_awards > 0: self.session['flash_msg'] = 'new_award'
      print "OK"
      return "OK"
      
      
  def update_user_sponsorships(self):          
      from accounts.methods import Sponsorships
      sponsorships = Sponsorships()
      # check for new sponsorships, both personal and business
      logging.info('Updating Sponsorships for User %s', self.session['user'].unique_identifier)
      new_sponsorships = sponsorships.check_user(self.session['user'])
      if new_sponsorships > 0: self.session['flash_msg'] = 'new_sponsorship'
      print "OK"
      return "OK"
