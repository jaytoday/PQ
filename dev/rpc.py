import logging
# Log a message each time this module get loaded.
logging.info('Loading %s', __name__)
from utils import webapp
from google.appengine.ext import db
import string, re
from google.appengine.api import urlfetch
from utils import jsonparser as parser, simplejson
from utils.utils import ROOT_PATH
from utils.gql_encoder import GqlEncoder, encode
from methods import restore_backup
from google.appengine.api import memcache
      	
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
  NOTE: Do not allow reload(sys); sys.setdefaultencoding('utf-8')
remote callers access to private/protected "_*" methods.
  """
  
 

  	        
  def refresh_data(self, *args):
  	from dev.methods import refresh_data
  	if len(args) == 0: return "specify data type"
  	return refresh_data(args[0])


  def delete_data(self, *args):
  	from dev.methods import delete_data
  	if len(args) == 0: return "specify data type"
  	print delete_data(args[0])
  	return
  	

  def load_data(self, *args):
   	if args[0] == "refresh_subject_images": 
   	    args = ()
   	    return self.refresh_subject_images(args) 
   	from dev.methods import load_data
  	if len(args) == 0: return "specify data type"
  	return load_data(args[0])
  	
  	
  	            
  def dump_data(self, *args):
  	from dev.methods import dump_data
  	print dump_data(args[0]) 
 
  
  def restore_backup(self, *args):
  	from dev.methods import restore_backup
  	return restore_backup()  	






  def flush_memcache(self, *args):
  	print ""
  	print "before flush:", memcache.get_stats()
  	memcache.flush_all()
  	print "after flush:", memcache.get_stats()
  		

############# Quiz Material Updates ################


  def add_proficiency(self, *args):
  	if len(args) < 3: return "Please give a name, status, and blurb"
  	from model.proficiency import Proficiency
  	save_entity = Proficiency.get_or_insert(key_name=args[0], name = args[0], status = args[1], blurb = args[2])
  	save_entity.put()
  	return encode(save_entity)


  def refresh_subject_images(self, *args):
  	this_subject = False
  	if len(args) > 0: this_subject = args[0]
  	from methods import refresh_subject_images
  	refresh_subject_images(this_subject)
  	


  def refresh_profile_images(self, *args):
  	from methods import Build
  	build = Build()
  	build.refresh_profile_images()		


  def working(self, *args):
  	pass

  	
  	    

  	
  # this should probably go in its own file
  def make_scores(self, *args):
  	SCORE_NUM = 10
  	self.correct_scores = 0
  	if len(args) < 2: return "Specify A Proficiency, and Correct Ratio"
  	from utils.appengine_utilities.sessions import Session
  	self.session = Session()
  	self.correct_prob = args[1]
  	
  	if not self.session['user']: return "Not Logged In"
  	import random
  	from model.quiz import QuizItem
  	from model.proficiency import Proficiency
  	this_proficiency = Proficiency.get_by_key_name(args[0])
  	items = QuizItem.gql("WHERE proficiency = :1", this_proficiency).fetch(1000)
  	items = random.sample(items, SCORE_NUM)
  	self.save = []
  	for i in items: 
  	    self.make_score(i) 
  	print "saved ", len(self.save), " scores. ", self.correct_scores, " were correct." 
  	db.put(self.save)
  	

  def make_score(self, i): 
	from model.quiz import QuizTaker
	from model.quiz import ItemScore
	import random
	this_user = QuizTaker.get_by_key_name(self.session['user'].unique_identifier)
	picked_answer = ''
	if random.randint(1,100) > self.correct_prob: #wrong answer -- could also just use normal distribution of correct probability
		while picked_answer == i.index: picked_answer = i.answers.pop()
	else:  picked_answer = i.index
	score = ItemScore(quiz_item = i,
						  quiz_taker = this_user,
						  correct_answer = i.index,
						  picked_answer = picked_answer,
						  type = "stub")	
	if score.picked_answer == score.correct_answer: 
		this_score = int(random.normalvariate(self.correct_prob, 15))
		if this_score > 100: this_score == 100
		score.score = this_score
		self.correct_scores += 1
	else: score.score = 0
	self.save.append(score)
  	

  	



  def god_mode(self, *args): # for debugging quizzes
  	from google.appengine.api import users
  	if not users.is_current_user_admin(): return "You can login through the console."
  	from utils.appengine_utilities.sessions import Session
  	self.session = Session()
  	if self.session['god_mode']: self.session['god_mode'] = False
  	else: self.session['god_mode'] = True
  	return self.session['god_mode']

############ Account Updates #######################
  	
  def set_levels(self, *args):
  	from quiztaker.methods import ProficiencyLevels
  	pl = ProficiencyLevels()
  	pl.set()

  def set_awards(self, *args):
  	from accounts.methods import Awards
  	awards = Awards()
  	return awards.check_all()  
  	
  def set_sponsorships(self, *args):
  	from accounts.methods import Sponsorships
  	sponsorships = Sponsorships()
  	return sponsorships.check_all()  
  
  def refresh_mailing_list(self, *args):
    from model.account import MailingList
    entries = MailingList.all().fetch(1000)
    for e in entries: e.delete()
    from methods import DataMethods
    data = DataMethods()
    data.load_data("mailing_list", "")
    return self.dump_mailing_list()
    
    
  def dump_mailing_list(self, *args):
    from model.account import MailingList
    print encode(MailingList.all().fetch(1000))



###### BUSINESSES ###############

  def add_business(self, *args):
	if not args: return "Specify A Business Name"
	if len(args) < 1: return "Specify A Business Name"
	business_name = args[0]
	from employer.methods import DataMethods
	dm = DataMethods()
	return dm.create_business_account(business_name)


  def add_auto_pledge(self, *args):
  	if not args: return "Specify A Business Identifier, Proficiency Name, and Number of Pledges."
  	if len(args) > 3: return "Specify A Business Identifier, Proficiency Name, and Number of Pledges."
  	business_name = args[0]
  	from model.employer import Employer
  	this_employer = Employer.get_by_key_name(business_name)
  	if not this_employer: return "employer does not exist"
  	proficiency_name = args[1]
  	from model.proficiency import Proficiency
  	import string
  	this_proficiency = Proficiency.get_by_key_name(string.capwords(proficiency_name))
  	pledge_num = int(args[2])
  	from model.employer import AutoPledge
  	new_pledge = AutoPledge(employer = this_employer,
  	                        proficiency = this_proficiency,
  	                        count = pledge_num)
  	new_pledge.put()
  	return encode(new_pledge)                       

  def refresh_employer_images(self, *args):
  	 from employer.methods import DataMethods
  	 d = DataMethods()
  	 return d.refresh_employer_images()






#### EXPERIMENTAL #####


  def zemanta(self, *args):
  	 from dev.zemanta import request
  	 return request()



  def destroy_everything(self, *args):
  	from dev.methods import Build
  	build = Build()
  	build.destroy_everything()
  	 
  	 
  	 

  	 
  	 


