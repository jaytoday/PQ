import logging
# Log a message each time this module get loaded.
logging.info('Loading %s', __name__)
from google.appengine.ext import webapp
from google.appengine.ext import db
import simplejson
from .model.quiz import QuizItem, ItemScore
from .model.user import QuizTaker, InviteList
from .model.employer import Employer
from methods import refresh_data, dump_data, load_data
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


        
  def refresh_data(self, *args):
  	if len(args) == 0: return "specify data type"
  	return refresh_data(args[0], "loud")

  def load_data(self, *args):
  	if len(args) == 0: return "specify data type"
  	return load_data(args[0], "loud")
  	            
  def dump_data(self, *args):
  	if len(args) == 0: return "specify data type"
  	if args[0] == "employers":
  	    print dump_data(Employer.all())  
  	    print ""
  	    print "---do not copy this line or below---"  #TODO: Don't print HTTP headers
  




  def get_scores(self, *args):
	employer = Employer.get(args[0])
	scores = employer.scores.fetch(1000)
	for score in scores:
		print score.type
		print score.score
		
	# add up all scores for a given quiztaker, and then rank them.
	return 


  	
  	
