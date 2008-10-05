import logging
import random
from google.appengine.api import urlfetch
import cgi
import wsgiref.handlers
import datetime, time
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
#RPC - add to utils
from google.appengine.ext.webapp import util
import simplejson

from utils import utils
from model import *
from stubs import *
from quizbuilder.views import *


# Log a message each time this module get loaded.
logging.info('Loading %s', __name__)

    



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

          

class PQHome(webapp.RequestHandler):
  #Load Plopquiz Homepage 

  def get(self):

    template_values = {}
    path = tpl_path('homepage.html')
    self.response.out.write(template.render(path, template_values))
    
    
class PQIntro(webapp.RequestHandler):
  #Put something here  

  def get(self):

    template_values = {}
    intro_template = self.request.get('page') + ".html"
    path = tpl_path(intro_template)
    self.response.out.write(template.render(path, template_values))




class QuizItemTemplate(webapp.RequestHandler):

  def get(self):

    template_values = {}
    quiz_slug = [self.request.get('slug'), self.request.get('source')]
    this_quiz_item = QuizItem.gql("WHERE slug = :slug",
                                  slug=quiz_slug)
    template_values['quiz_item'] = this_quiz_item
    path = tpl_path('quiz_item.html') # Pass Quiz Item to Template
    self.response.out.write(template.render(path, template_values))





class PQDemo(webapp.RequestHandler):
  #Load Ad Embed Preview Page

  def get(self):

    template_values = {}
    path = tpl_path('example_blog.html')
    self.response.out.write(template.render(path, template_values))
    


class ViewQuiz(webapp.RequestHandler):
  #View Quiz

  quiz_array = []
  all_quiz_items = []
  proficiencies = {}
  quiz_item_count = 5
    
  def get(self):
      # Create random list of three quiz items.
    
    # Query all quiz items
    q = db.GqlQuery("SELECT * FROM QuizItem")
    quiz_items = q.fetch(1000) 
    
    # Load Fixture Data if Necessary
    if len(quiz_items) == 0: 
        refresh_data("quiz_items")
        q = db.GqlQuery("SELECT * FROM QuizItem")
        quiz_items = q.fetch(1000)         
        
    for item in quiz_items:
        self.load_item(item)

    self.load_array()
    template_values = {"quiz_items": self.quiz_array }
    logging.debug(template_values)
    path = tpl_path('ad.html')
    self.response.out.write(template.render(path, template_values))
    

  def load_item(self, item):
        random.shuffle(item.answers)
        item_dict = {"slug" : item.slug, "answer1" : item.answers[0], "answer2" : item.answers[1], "answer3": item.answers[2],
        "proficiency": item.proficiency.name}
        if item.proficiency.name not in self.proficiencies: self.proficiencies[item.proficiency.name] = []
        self.proficiencies[item.proficiency.name].append(item_dict)
        return self.proficiencies

  def load_array(self):
        for prof_type in self.proficiencies:
            proficiency = random.sample(self.proficiencies[prof_type],
                                  self.quiz_item_count)
            self.quiz_array += proficiency
        random.shuffle(self.quiz_array)
        return self.quiz_array
        

class QuizComplete(webapp.RequestHandler):
  # Quiz Completed Screen
   def get(self):
    logging.debug('Loading Score')
    template_values = {}
    path = tpl_path('quiz_complete.html')
    self.response.out.write(template.render(path, template_values))
    
            

class ViewScore(webapp.RequestHandler):
  # View Score Report.
   def get(self):
    logging.debug('Loading Score')
    template_values = {}
    try:
      latest_scores = TempItemScore.gql("WHERE quiz_taker = :quiz_taker ORDER BY date DESC",
                                quiz_taker="quiz_taker")   
      logging.info('Loading all score items') 
    except:
      raise_error('Error Retrieving Data From Score Model')
  
    try:
      correct_item = TempItemScore.gql("WHERE score > :score AND quiz_taker = :quiz_taker ORDER BY score DESC, date DESC",
                             quiz_taker="quiz_taker", score=0 )
      logging.info('Loading correct Score items from user')
    except:
      raise_error('Error Retrieving Data From Score Model')    
        
    logging.info(latest_scores.count())
    totalscore = correct_item.count()
    totalitems = latest_scores.count()
    logging.info("totalitems:" + str(totalitems))
    logging.info("totalscore:" + str(totalscore))
  
    percentage = 0
    if totalitems > 0:
      percentage = float(totalscore) / float(totalitems) * 100
      percentage = int(percentage)

    if percentage > 99:
       passed = True
    else:
       passed = False
    
    template_values["scores"] = latest_scores
    template_values["totalscore"] = totalscore
    template_values["totalitems"] = totalitems
    template_values["percentage"] = percentage
    template_values["passed"] = passed


    path = tpl_path('score.html')
    self.response.out.write(template.render(path, template_values))
    

    
class RefreshData(webapp.RequestHandler):
  #Refreshes Data

  def get(self):
      destroy_data("quiz_items", "verbose")
      destroy_data("proficiencies", "verbose")
      refresh_data("verbose")




class DumpData(webapp.RequestHandler):
  #Dumps Data

  def get(self):
      dump_data("quiz_items", "verbose")
      
        
 

def dump_data(data_type, *verbose):
    items = []
    models = {"quiz_items" : "QuizItem"}
    query_string = "SELECT * FROM " + models[data_type] 
    query = db.GqlQuery(query_string) # Query all quiz items
    items = query.fetch(1000)
    encoder = GqlEncoder()
    json_items = encoder.encode(items)
    print json_items




def destroy_data(data_type, *verbose):
# use "verbose" to print logging info

    models = {"quiz_items" : "QuizItem", "proficiencies" : "Proficiency"}
    item_names= {"quiz_items" : "slug", "proficiencies" : "proficiency"}
    query_string = "SELECT * FROM " + models[data_type]
    
    query = db.GqlQuery(query_string) # Query all quiz items
    data_type = query.fetch(1000)
    for item in data_type:
        if verbose:
            print ""   
            print "deleted: " + str(item.__dict__) 
        item.delete()
        
def refresh_data(*verbose):
    # use "verbose" to print logging info
    proficiencies = []
    # Load External JSON fixture
    json_file = open(ROOT_PATH + "/data/quiz_items.json")
    json_str = json_file.read()
    newdata = simplejson.loads(json_str) # Load JSON file as object
    
    # Retrieve Proficiency. If new, then save it. 
    for item in newdata["quiz_items"]:
        this_proficiency = Proficiency.gql("WHERE name = :proficiency",
                                       proficiency=item['proficiency']).get()
        if not this_proficiency:
            this_proficiency = Proficiency(name=item['proficiency'])
            this_proficiency.put()
            if verbose:
                print "added proficiency: " + str(this_proficiency.name)
    # Store Item in Datastore
        
        quiz_item = QuizItem(slug = item['slug'],
                             category = item['content'][0],
                             content = item['content'][1],
                             proficiency = this_proficiency.key(),
                             answers = item['answers'],
                             index = item['index'] )
       
                              #Add List of Answers
        quiz_item.put()
        if verbose:
            print "added quiz item: " + str(quiz_item.slug) + " + " + str(quiz_item.proficiency.name)

        







class ViewNone(webapp.RequestHandler):

   def get(self):
       pass
