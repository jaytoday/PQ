import logging
# Log a message each time this module get loaded.
logging.info('Loading %s', __name__)
from utils import webapp, simplejson
from google.appengine.ext import db
from .utils.utils import tpl_path, ROOT_PATH, raise_error
from methods import registered
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

		
	# add up all scores for a given quiztaker, and then rank them.
	return str(user.key())




  def SubmitSponsorPledge(self, *args):
  	session = Session()
  	from .model.account import Account
  	from .model.user import Profile
  	sponsor_type = "personal" # or corporate
  	package = args[0]
  	award_type = args[1]
  	raw_target = [args[2]] # for more than one user
  	target = []
  	activated = []
  	single_target = False
  	for u in raw_target: 
  	    t = Profile.get(u)
  	    if len(raw_target) > 1: single_target = t
  	    target.append(t.key())
  	    activated.append(False)
  	from model.account import SponsorPledge
  	new_pledge = SponsorPledge(#key_name?
  	                           sponsor = session['user'],
  	                           sponsor_type = sponsor_type,
  	                           package = package,
  	                           award_type = award_type,
  	                           target = target,
  	                           type = type,
  	                           activated = activated)
  	
  	# if only a single person is receiving the pledge
  	if single_target:
  		new_pledge.single_target = single_target
  	# if any subject was chosen
  	if args[3] != "any_subject":
  		from model.proficiency import Proficiency
  		new_pledge.proficiency = Proficiency.get(args[3])
  		
  	db.put(new_pledge)
  	return "True"


  	
  	
  def intro_mail_message(self, *args):
  	from model.user import Profile
  	from accounts.mail import mail_intro_message
  	profiles = Profile.all().fetch(10)
  	for p in profiles:
  		mail_intro_message(p)
  		

  	
  	  	
