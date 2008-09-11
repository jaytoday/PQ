import logging
import random
from utils import *
from model import *


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

  def Add(self, *args):


    logging.debug('Posting Answer')    
    score = Score()
    score.picked_answer = str(args[0])
    
    item_slug = str(args[1])
    #Lookup quiz item with slug, clean it, and match it. 
    this_item = QuizItem.gql("WHERE slug = :slug",
                                  slug=item_slug)
                                
   
    logging.debug(this_item)  
    score.correct_answer = this_item[0].index
    
    picked_clean = score.picked_answer.strip()
    picked_clean = picked_clean.lower()
    correct_clean = score.correct_answer.strip()
    correct_clean = correct_clean.lower()


    if picked_clean == correct_clean:
        score.score = "correct"
    else:
        score.score = "incorrect"
        logging.debug('Incorrect answer') 

    score.author = "author" # TODO Use Accounts
          
    try:
        score.put()
        logging.info('Score entered by user %s with score %s, correct: %s, picked: %s'
                     % (score.author, score.score, score.picked_answer, score.correct_answer))
    except:
        raise_error('Error saving score for user %s with score %s, correct: %s, picked: %s'
                    % (score.author, score.score, score.picked_answer, score.correct_answer))

    return score.score


  def Init(self, *args):


    logging.debug('Deleting Datastore!')   
    q = db.GqlQuery("SELECT * FROM Score")
    results = q.fetch(1000)
    for result in results:
        result.delete()
        


  def List(self, *args):
  
    logging.debug('Posting List Entry')    
    list_entry = List()    
    list_entry.email = str(args[0])
    list_entry.put()



class PQHome(webapp.RequestHandler):
  #Load Plopquiz Homepage 

  def get(self):

    template_values = {


                                                    
      }
     
      
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
    


class ViewAd(webapp.RequestHandler):
  #Put something here  

  def get(self):
      # Create random list of three quiz items.
       

    quiz_items = []
    all_quiz_items = []
    query = db.GqlQuery("SELECT * FROM QuizItem") # Query all quiz items
    fetch_items = query.fetch(1000)
    for item in fetch_items:
        item_dict = {"slug" : item.slug, "index" : item.index, "answer1" : item.answers[0], "answer2" : item.answers[1], "answer3": item.answers[2]}
        all_quiz_items.append(item_dict)
        
  
    
    quiz_item_count = 5

    quiz_items = random.sample(all_quiz_items,
                              quiz_item_count)


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
        latest_scores = Score.gql("WHERE author = :author ORDER BY date DESC",
                                  author="author")   
        logging.info('Loading all score items') 
      except:
        raise_error('Error Retrieving Data From Score Model')
      
      try:
        correct_item = Score.gql("WHERE author = :author AND score = :score ORDER BY date DESC",
                               author="author", score="correct" )
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
    
    
    
    
    
    
    
class LoadData(webapp.RequestHandler):
  #Put something here  

  def get(self):

    # Delete Old Data 
    query = db.GqlQuery("SELECT * FROM QuizItem") # Query all quiz items
    items = query.fetch(1000)
    for item in items:
        print "deleted " + str(item.slug)
        item.delete()
    template_values = {}

    # Load External JSON fixture
        
    json_file = open("static/data/quiz_items.json")
    json_str = json_file.read()
    newdata = simplejson.loads(json_str)
    
    for item in newdata["quiz_items"]:
    
    # Store Item in Datastore
    
        quiz_item = QuizItem()
        quiz_item.slug = item['slug']
        #Add List of Answers
        quiz_item.answers = item['answers']
        print "added " + str(quiz_item.slug)
        quiz_item.index = item['index']
        quiz_item.put()           

