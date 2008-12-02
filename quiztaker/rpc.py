import logging
# Log a message each time this module get loaded.
logging.info('Loading %s', __name__)
from utils import webapp, simplejson
from google.appengine.ext import db
from .model.quiz import QuizItem, ItemScore
from .model.user import QuizTaker, InviteList
from .model.employer import Employer 
from methods import refresh_data, dump_data, load_data
from .utils.utils import tpl_path, ROOT_PATH, raise_error
from utils.gql_encoder import GqlEncoder, encode
from utils.appengine_utilities.sessions import Session
from load_quiz import QuizSession

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
    if self.request.get('callback'): self.response.out.write(self.request.get("callback") + "('" + str(simplejson.dumps(result)) + "');")
    else: self.response.out.write(simplejson.dumps(result))
    


class RPCMethods(webapp.RequestHandler):
  """ Defines AJAX methods.
  NOTE: Do not allow remote callers access to private/protected "_*" methods.
  """


  def get_quiz_items(self, *args):
  	if not self.session["start"]:
		import time
		self.session["start"] = time.clock()
	quiz_session = QuizSession(self.session)
	return quiz_session.load_quiz_items(args[0])


  def get_quiz(self, *args):
    template_values = {}
    item_key = args[0]
    this_quiz_item = db.get(item_key)
    quiz_item = {}
    quiz_item['topic_name'] = this_quiz_item.topic.name
    quiz_item['content'] = this_quiz_item.content
    quiz_item['answers'] = this_quiz_item.answers
    quiz_item['theme'] = this_quiz_item.theme
    json_response = simplejson.dumps(quiz_item) 
    return json_response
    

  def next_quiz_item(self):
		next_item = self.session['quiz_items'].pop()
		return next_item
		        
  def refresh_data(self, *args):
  	if len(args) == 0: return "specify data type"
  	return refresh_data(args[0], "loud")

  def load_data(self, *args):
  	if len(args) == 0: return "specify data type"
  	return load_data(args[0], "loud")
  	            

  def dump_data(self, *args):
  	if args[0] == "quiz_items":
  	    print dump_data(QuizItem.all()) 
  	if args[0] == "item_scores":
  	    print dump_data(ItemScore.all()) 
  	print ""
  	print "---do not copy this line or below---"  #TODO: Don't print HTTP headers
  
  
  
  
  def AddScore(self, *args):
	logging.debug('Posting Answer')    
	picked_answer = str(args[0])
	#Lookup quiz item with slug, clean it, and match it. 
	
	this_item = QuizItem.get(args[2])
	logging.debug(this_item)  

	picked_clean = picked_answer.strip()
	picked_clean = picked_clean.lower()
	correct_clean = this_item.index.strip()
	correct_clean = correct_clean.lower()

	if picked_clean == correct_clean:
		timer_status = float(args[1])
		this_score = int(round(timer_status * 100))
	else:
		this_score = 0
		logging.debug('Incorrect answer')

	# Need Better Temp Storing 
                         
	score = ItemScore(quiz_item = this_item.key(),
					  score = this_score,
					  correct_answer = this_item.index,
					  picked_answer = picked_answer,
					  )
					  	
	self.session = Session()
	user = self.session.logged_in()
	
	if user:
		this_user = QuizTaker.get_by_key_name(user)
		score.quiz_taker = this_user.key()
		score.type = "site"     # type could be site, practice widget
	else:
		score.type = "temp"
	if len(args[3]) > 0: score.vendor = Employer.get(args[3])
	score.put()
	if user: 
	  this_user.scores.append(score.key())
	  this_user.put()
	logging.info('Score entered by user %s with score %s, correct: %s, picked: %s'
				% (score.quiz_taker, score.score, score.picked_answer, score.correct_answer))
	
	# send jsonp response 
	


## QUIZTAKER SESSION ##

  def Init(self, *args):
	q = db.GqlQuery("SELECT * FROM ItemScore WHERE type='temp'")
	results = q.fetch(1000)
	d = 0
	for result in results:
		result.delete()
		d += 1
	return "deleted: " + str(d) + " entries"

        


  def Register(self, *args):
	logging.debug('Registering New User')
	try:     
		new_quiz_taker = QuizTaker(name = args[0],
								   email = str(args[1]),
								   key_name = str(args[1]),
								   occupation = args[2],
								   work_status = args[3],
								   location = args[5]
								   )
		if len(args[4]) > 7: new_quiz_taker.webpage = args[4]  
		new_quiz_taker.put()
	except: return "invalid webpage or e-mail address"
	logging.debug('New User - Saving Score')    
	q = db.GqlQuery("SELECT * FROM ItemScore WHERE type = 'temp'")
	results = q.fetch(1000)
	print results
	movescores = []
	for result in results:
		try:
			print result.type
			movescore = ItemScore(quiz_taker = new_quiz_taker.key(),
								score = result.score,
								quiz_item = result.quiz_item,
								picked_answer = result.picked_answer,
								correct_answer = result.correct_answer,
								vendor = result.vendor,
								type = new_quiz_taker.email
								)
			movescores.append(movescore)
			logging.debug('Moved A Score Item')
			result.type = 'trash'
			result.put()
			
		except:                # if not all parts of the item score are accessible
		    result.type = 'incomplete'
		    result.put()	
	
	db.put(movescores) # save new scores
	for ms in movescores: new_quiz_taker.scores.append(ms.key())   # These perform a duplicate reference to the quiz_taker property in ItemScore. 
	new_quiz_taker.put()
	list_entry = InviteList()    
	list_entry.email = str(args[1])
	list_entry.put()
	print new_quiz_taker.scores
	print new_quiz_taker.__dict__
	for s in new_quiz_taker.scores:
		try: print s
		except: print "unable to print scores"
   




  def DemoNewUser(self, *args):  #deprecated
    # f.name.value, f.email.value, f.occupation.value, f.work_status.value, f.webpage.value, f.location.value
    logging.debug('New User - Adding to E-mail List')    
    list_entry = InviteList()    
    list_entry.email = str(args[0])
    list_entry.put()
    new_quiz_taker = QuizTaker(email = str(args[0]),key_name = str(args[0]))
    new_quiz_taker.put()
    print new_quiz_taker.key()
    logging.debug('New User - Saving Score')    
    q = db.GqlQuery("SELECT * FROM ItemScore WHERE type = 'temp'")
    results = q.fetch(1000)
    for result in results:
        movescore = ItemScore(quiz_taker = new_quiz_taker.key(),
                            score = result.score,
                            quiz_item = result.quiz_item,
                            picked_answer = result.picked_answer,
                            correct_answer = result.correct_answer,
                            vendor = result.vendor)
        movescore.put()
        logging.debug('Moved A Score Item')
        result.type = 'trash'
        result.put()
        new_quiz_taker.scores.append(movescore.key())   # These perform a duplicate reference to the quiz_taker property in ItemScore. 
    new_quiz_taker.put()
    

        
        
  def AllScores (self, *args):        
    q = db.GqlQuery("SELECT * FROM ItemScore")
    results = q.fetch(1000)
    return [result.score for result in results]




  def List(self, *args):
  
    logging.debug('Posting E-mail List Entry')    
    list_entry = InviteList()    
    list_entry.email = str(args[0])
    list_entry.put()

