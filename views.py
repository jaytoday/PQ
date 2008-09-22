import logging
import random
from utils import *
from model import *
from stubs import *


# Log a message each time this module get loaded.
logging.info('Loading %s', __name__)

    
    
   


class RPCHandler(webapp.RequestHandler):
  #Arg1 is language. Arg2 is correct_language
  """ Allows the functions defined in the RPCMethods class to be RPCed."""
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
  """ Defines the methods that can be RPCed.
  NOTE: Do not allow remote callers access to private/protected "_*" methods.
  """

  def AddScore(self, *args):


    logging.debug('Posting Answer')    
    score = TempItemScore()
    score.picked_answer = str(args[0])
    
    item_slug = str(args[1])
    #Lookup quiz item with slug, clean it, and match it. 
    this_item = QuizItem.gql("WHERE slug = :slug",
                                  slug=item_slug)
                                
   
    logging.debug(this_item)  
    score.correct_answer = this_item[0].index
    score.quiz_item = str(args[1]) # slug
    
    picked_clean = score.picked_answer.strip()
    picked_clean = picked_clean.lower()
    correct_clean = score.correct_answer.strip()
    correct_clean = correct_clean.lower()


    if picked_clean == correct_clean:
        score.score = 1 # TODO add Timer Data 
    else:
        score.score = 0
        logging.debug('Incorrect answer') 

    score.quiz_taker = "quiz_taker" # TODO Use Accounts
          
    try:
        score.put()
        logging.info('Score entered by user %s with score %s, correct: %s, picked: %s'
                     % (score.quiz_taker, score.score, score.picked_answer, score.correct_answer))
    except:
        raise_error('Error saving score for user %s with score %s, correct: %s, picked: %s'
                    % (score.quiz_taker, score.score, score.picked_answer, score.correct_answer))

    return score.score


  def Init(self, *args):


    logging.debug('Deleting Datastore!')  # For Demo Only 
    q = db.GqlQuery("SELECT * FROM TempItemScore")
    results = q.fetch(1000)
    for result in results:
        result.delete()
        


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
    logging.debug('New User - Saving Score')    
    q = db.GqlQuery("SELECT * FROM TempItemScore")
    results = q.fetch(1000)
    for result in results:
        result = ItemScore()
        result.quiz_taker = str(args[0])
        result.put()
        logging.debug('Moved A Score Item')
        
    
  def RedirectHome(self, *args):
  
      pass#self.redirect("/")

    
    

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
  #Put something here  

  def get(self):

    template_values = {}
    
    quiz_template = self.request.get('quiz_item') + ".html"
    path = item_path(quiz_template)
    self.response.out.write(template.render(path, template_values))





class PQDemo(webapp.RequestHandler):
  #Put something here  

  def get(self):

    template_values = {


                                                    
      }
     
      
    path = tpl_path('trixy_blog.html')
    self.response.out.write(template.render(path, template_values))
    


class ViewQuiz(webapp.RequestHandler):
  #Put something here  

  def get(self):
      # Create random list of three quiz items.
       

    quiz_items = []
    all_quiz_items = []
    proficiencies = {}
    quiz_item_count = 3
    
    # Query all quiz items
    query = db.GqlQuery("SELECT * FROM QuizItem") 
    fetch_items = query.fetch(1000)
    
    # Load Fixture Data if Necessary
    if len(fetch_items) == 0: 
        refresh_data("quiz_items")
        newquery = db.GqlQuery("SELECT * FROM QuizItem") 
        fetch_items = newquery.fetch(1000)
        
        
    for item in fetch_items:
        item_dict = {"slug" : item.slug, "index" : item.index, "answer1" : item.answers[0], "answer2" : item.answers[1], "answer3": item.answers[2],
        "proficiency": item.proficiency}
        if item.proficiency in proficiencies:
            pass
        else:
            proficiencies[item.proficiency] = []
        proficiencies[item.proficiency].append(item_dict)
    for prof_type in proficiencies:
        proficiency = random.sample(proficiencies[prof_type],
                              quiz_item_count)
        quiz_items += proficiency
    random.shuffle(quiz_items)
    print quiz_items
    template_values = {"quiz_items": quiz_items }

      
    path = tpl_path('ad.html')
    self.response.out.write(template.render(path, template_values))
    






class ViewScore(webapp.RequestHandler):
  # View Taught Or Not Grade.
   def get(self):
    logging.debug('Loading Score')
    template_values = {}

    if self:
    
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

    for item in newdata["quiz_items"]:

    # Store Item in Datastore

        quiz_item = QuizItem()
        quiz_item.slug = item['slug']
        quiz_item.proficiency = item['proficiency']
        #Add List of Answers
        quiz_item.answers = item['answers']
        if verbose:
            print "added quiz item: " + str(quiz_item.slug) + " + " + str(quiz_item.proficiency)
        
        quiz_item.index = item['index']
        quiz_item.put()
     

    # Store Proficiencies

        proficiencies.append(quiz_item.proficiency)
        
    proficiencies = set(proficiencies)
    for this_proficiency in proficiencies:
        proficiency = Proficiency()
        proficiency.proficiency = this_proficiency
        proficiency.put()
        if verbose:
            print "added proficiency: " + str(proficiency.proficiency)
        
