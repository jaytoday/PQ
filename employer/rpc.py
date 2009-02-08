import logging
# Log a message each time this module get loaded.
logging.info('Loading %s', __name__)
from utils import webapp, simplejson
from google.appengine.ext import db
from .model.quiz import QuizItem, ItemScore
from .model.user import QuizTaker, InviteList
from .model.employer import Employer
from .utils.utils import tpl_path, ROOT_PATH, raise_error


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


  def get_scores(self, *args):
	employer = Employer.get(args[0])
	scores = employer.scores.fetch(1000)
	for score in scores:
		print score.type
		print score.score
		
	# add up all scores for a given quiztaker, and then rank them.
	return 



  	
  	


class SponsorPost(webapp.RequestHandler): 
  def post(self):
  	if self.request.get('action') == 'settings': self.response.out.write(simplejson.dumps(  self.sponsor_settings()  )) 
  	if self.request.get('action') == 'apply': self.response.out.write(simplejson.dumps(  self.sponsor_apply()  ))   
  	


  def sponsor_settings(self): 	
	PLEDGE_NUM = 500 
	# get employer
	this_employer = Employer.get_by_key_name(self.request.get('sponsor'))
	# save message
	this_employer.sponsorship_message = self.request.get('sponsorship_message')
	#save quiz subjects
	this_employer.quiz_subjects = [ self.request.get('quiz_subject') ]
	# also save it in the profile_image
	from model.user import Profile
	this_user = Profile.get_by_key_name(this_employer.unique_identifier)
	from model.proficiency import Proficiency
	this_proficiency = Proficiency.get_by_key_name(self.request.get('quiz_subject'))
	
	#this_user.sponsored_subjects.append( Proficiency.get_by_key_name(self.request.get('quiz_subject')) )  -- Multiple Entries
	if self.request.get('quiz_subject') != "undefined": this_user.sponsored_subjects = [ this_proficiency.key() ]
	# create auto_pledge
	from model.employer import AutoPledge
	# save sponsor account
  	new_pledge = AutoPledge(employer = this_employer,
  	                        proficiency = this_proficiency,
  	                        count = PLEDGE_NUM)

	db.put([this_employer, this_user])
	return "OK"
  	

  def sponsor_apply(self): 	
	from model.employer import Sponsor_Application
	sponsor_app = Sponsor_Application(name = self.request.get('name'),
	                                      email = self.request.get('email') )
	sponsor_app.put()
	return "OK"

