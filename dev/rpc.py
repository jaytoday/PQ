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

  
  def restore_backup(self, *args):
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
  	if len(args) == 0: return "enter in a proficiency name, or an empty arg0 string to refresh all subjects"
  	from methods import Build
  	build = Build()
	from model.proficiency import Proficiency
	import string 
	if len(args[0]) > 0: 
	    subject = Proficiency.get_by_key_name(string.capwords(args[0]))
	    return build.refresh_subject_images(subject)
  	return build.refresh_subject_images()

  # refresh default profile images
  def refresh_profile_images(self, *args):
  	from methods import Build
  	build = Build()
  	build.refresh_profile_images()		

  def working(self, *args):
  	return
  	from model.user import Profile, ProfilePicture
  	i = ProfilePicture.all().get()
  	ps = Profile.all().fetch(1000)
  	for p in ps:
  		p.photo = i
  		p.put()
  	



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



