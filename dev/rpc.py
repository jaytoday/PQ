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


  def refresh_subject_images(self, *args):
  	from methods import Build
  	build = Build()
  	build.refresh_subject_images()

  def refresh_profile_images(self, *args):
  	from methods import Build
  	build = Build()
  	build.refresh_profile_images()		

  def working(self, *args):
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
  
