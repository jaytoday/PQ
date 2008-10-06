from google.appengine.ext import webapp
from google.appengine.ext import db
import simplejson

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

  def ds(self, *args):
    qt = QuizTaker(email = "a@a.com")
    qt.put()
    quiztakers = QuizTaker.all()
    for t in quiztakers:
        if t.filter.get():  # Check if filter exists for this quiz taker
           try:
               print t.filters   #fake
           except AttributeError:
               pass
           f = t.filter.get()
           f.mean = 0
           f.put()
           self.runOperation(t, f)

        else:
            f = QuizTakerFilter(quiz_taker = t)
            f.put() # Create new filter
            f = self.runOperation(t, f)
        #f.put()
    
        
    
  def runOperation(self, t, f):
    print t.filter.get().mean
    print f.quiz_taker.filter.get().mean
    print f.quiz_taker.scores
    print f.quiz_taker.itemscores.get()

            
  
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


  def Init(self, *args):
    q = db.GqlQuery("SELECT * FROM ItemScore WHERE type='temp'")
    results = q.fetch(1000)
    d = 0
    for result in results:
        result.delete()
        d += 1
    return "deleted: " + str(d) + " entries"

        


  def List(self, *args):
  
    logging.debug('Posting E-mail List Entry')    
    list_entry = InviteList()    
    list_entry.email = str(args[0])
    list_entry.put()



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

     
        
  def SubmitContentUrl(self, *args): 
      return "ruh roh!"   
    
  def SubmitQuizItem(self, *args):

      new_quiz_item = QuizItem()
      new_quiz_item.slug = [str(args[0]), str(args[1])]
      new_quiz_item.index = str(args[2])
      new_quiz_item.answers = args[3] # And args[2] 
      new_quiz_item.category = str(args[4])       # different datastore? Not currently in model 
      new_quiz_item.proficiency = str(args[5])  # Should be Proficiency
      new_quiz_item.content = str(args[6])
      new_quiz_item.difficulty = 0 # Default?
      #new_quiz_item.put()
      return "saved quiz item" 

