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
from .utils.utils import tpl_path, ROOT_PATH, raise_error
from model.quiz import Proficiency, ProficiencyTopic, QuizTaker, QuizItem, ItemScore
from methods import refresh_data
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
                                  slug=quiz_slug)
    template_values['quiz_item'] = this_quiz_item
    path = tpl_path(QUIZTAKER_PATH + 'quiz_item.html') # Pass Quiz Item to Template
    self.response.out.write(template.render(path, template_values))





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
    self.proficiencies = {}
      # Create random list of three quiz items.
    
    # Query all quiz items
    q = db.GqlQuery("SELECT * FROM QuizItem")
    quiz_items = q.fetch(1000) 
    
    # Load Fixture Data if Necessary
    if len(quiz_items) == 0: 
        refresh_data("quiz_items", "quiet") 
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
        self.quiz_array = []
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
    

 



class ViewNone(webapp.RequestHandler):

   def get(self):
       pass
