import logging
# Log a message each time this module get loaded.
logging.info('Loading %s', __name__)
from utils import webapp
from google.appengine.ext import db
import simplejson
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
  	user = registered(session['user'])
  	user.fullname = args[0]
  	user.email = args[1]
  	user.location = args[2]
  	if len(args[3]) > 8: 
		try: user.webpage = args[3]
		except: return "Webpage error"
  	user.work_status = args[4]
  	user.aboutme = args[5]
  	user.put()

		
	# add up all scores for a given quiztaker, and then rank them.
	return encode(user)


  	
  	
