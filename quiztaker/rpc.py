import logging
# Log a message each time this module get loaded.
logging.info('Loading %s', __name__)
from google.appengine.ext import webapp
from google.appengine.ext import db
import simplejson
from .model.quiz import Proficiency, ProficiencyTopic, QuizTaker, QuizItem, ItemScore
from .model.user import InviteList
from methods import refresh_data, dump_data

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

  def get_quiz(self, *args):
    template_values = {}
    quiz_slug = [args[0], args[1]]
    this_quiz_item = QuizItem.gql("WHERE slug = :slug",
                                  slug=quiz_slug).get()
    quiz_item = {}
    quiz_item['category'] = this_quiz_item.category
    quiz_item['content'] = this_quiz_item.content
    quiz_item['answers'] = this_quiz_item.answers
    json_response = simplejson.dumps(quiz_item) 
    return json_response
    
        
  def refresh_data(self, *args):
  	if len(args) == 0: return "specify data type"
  	if args[0] == "quiz_items":
  	    return refresh_data(QuizItem.all(), "loud")
            

  def dump_data(self, *args):
  	if args[0] == "quiz_items":
  	    print dump_data(QuizItem.all())
  	    print ""
  	    print "---do not copy this line or below---"
  
  def AddScore(self, *args):

    logging.debug('Posting Answer')    
    picked_answer = str(args[0])
    item_slug = eval(args[1])
    #Lookup quiz item with slug, clean it, and match it. 
    this_item = QuizItem.gql("WHERE slug = :slug",
                                  slug=item_slug)
    logging.debug(this_item)  

    picked_clean = picked_answer.strip()
    picked_clean = picked_clean.lower()
    correct_clean = this_item[0].index.strip()
    correct_clean = correct_clean.lower()


    if picked_clean == correct_clean:
        this_score = 1 # TODO add Timer Data 
    else:
        this_score = 0
        logging.debug('Incorrect answer') 


          
    try:
        score = ItemScore(type='temp', 
                          slug = item_slug,
                          quiz_item = this_item[0].key(),
                          score = this_score,
                          correct_answer = this_item[0].index,
                          picked_answer = picked_answer,
                          )
        score.put()
        logging.info('Score entered by user %s with score %s, correct: %s, picked: %s'
                     % (score.quiz_taker, score.score, score.picked_answer, score.correct_answer))
    except:
        raise_error('Error saving score for user %s with score %s, correct: %s, picked: %s'
                    % (score.quiz_taker, score.score, score.picked_answer, score.correct_answer))

    return score.score


## QUIZTAKER SESSION ##

  def Init(self, *args):
    q = db.GqlQuery("SELECT * FROM ItemScore WHERE type='temp'")
    results = q.fetch(1000)
    d = 0
    for result in results:
        result.delete()
        d += 1
    return "deleted: " + str(d) + " entries"

        


  def NewUser(self, *args):
  
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
                            type = 'demo')
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
