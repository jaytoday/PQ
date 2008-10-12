import logging
# Log a message each time this module get loaded.
logging.info('Loading %s', __name__)
import random
from google.appengine.api import urlfetch
import cgi
import wsgiref.handlers
import datetime, time
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp

from google.appengine.ext.webapp import util
import simplejson
from .utils.utils import tpl_path, ROOT_PATH
import model.quiz 

# Template paths
QUIZTAKER_PATH = 'quiztaker/'
DEMO_PATH = 'demo/'



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
    intro_template = QUIZTAKER_PATH + self.request.get('page') + ".html"
    path = tpl_path(intro_template)
    self.response.out.write(template.render(path, template_values))






class PQDemo(webapp.RequestHandler):
  #Load Ad Embed Preview Page

  def get(self):

    template_values = {}
    path = tpl_path(DEMO_PATH +'example_blog.html')
    self.response.out.write(template.render(path, template_values))
    


class QuizItemTemplate(webapp.RequestHandler):

  def get(self):
    template_values = {}
    quiz_slug = [self.request.get('slug'), self.request.get('source')]
    this_quiz_item = QuizItem.gql("WHERE slug = :slug",
                                  slug=quiz_slug).get()
    
    
    quiz_item = {}
    quiz_item['content'] = this_quiz_item.content
    quiz_item['category'] = this_quiz_item.category
    quiz_item['answers'] = this_quiz_item.answers
    json_response = simplejson.dumps(quiz_item)
    print "a" 
    print json_response
    
    json_loads = simplejson.loads(json_response)
    print json_loads['content']
    """                      
    template_values['quiz_item'] = this_quiz_item
    path = tpl_path(QUIZTAKER_PATH + 'quiz_item.html') # Pass Quiz Item to Template
    self.response.out.write(template.render(path, template_values))
    """


class QuizFrame(webapp.RequestHandler):
        def get(self):
                template_values = {}
                path = tpl_path(QUIZTAKER_PATH + 'quizframe.html')
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
    path = tpl_path(DEMO_PATH + 'ad.html')
    self.response.out.write(template.render(path, template_values))
    

  def load_item(self, item):
        random.shuffle(item.answers)
        item_answers = []
        [item_answers.append(str(a)) for a in item.answers]
        item_dict = {"slug" : item.slug, "answers": item_answers, "answer1" : item.answers[0], "answer2" : item.answers[1], "answer3": item.answers[2],
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
    path = tpl_path(QUIZTAKER_PATH + 'quiz_complete.html')
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


    path = tpl_path(QUIZTAKER_PATH + 'score.html')
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












          
