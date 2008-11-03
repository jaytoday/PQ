import logging
# Log a message each time this module get loaded.
logging.info('Loading %s', __name__)
import random
from google.appengine.api import urlfetch
import cgi
import wsgiref.handlers
import datetime, time
import string
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from utils.gql_encoder import GqlEncoder, encode
from google.appengine.ext.webapp import util
import simplejson
from .utils.utils import tpl_path, ROOT_PATH, raise_error
from .model.quiz import QuizItem, ItemScore
from .model.user import QuizTaker
from .model.employer import Employer 
from .model.proficiency import Proficiency, ProficiencyTopic 
from methods import refresh_data
from load_quiz import LoadQuiz
# Template paths
QUIZTAKER_PATH = 'quiztaker/'
QUIZDEMO_PATH = 'quiztaker/demo/'
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
    if self.request.get('demo') == "true": intro_template = QUIZDEMO_PATH + self.request.get('page') + ".html"
#    if  self.request.get('page') == "begin_quiz": template_values['proficiencies'] = eval(self.request.get('proficiencies'))

    path = tpl_path(intro_template)
    self.response.out.write(template.render(path, template_values))






class PQDemo(webapp.RequestHandler):
  #Load Ad Embed Preview Page

  def get(self):
    template_values = {}
    path = tpl_path(DEMO_PATH +'example_blog.html')
    self.response.out.write(template.render(path, template_values))
    


# this is only used for the demo. 
class QuizItemTemplate(webapp.RequestHandler):

  def get(self):
    logging.debug('quiz_item')
    template_values = {}
    #quiz_slug = [self.request.get('slug'), self.request.get('source')] -- deprecated
    this_quiz_item = QuizItem.get(self.request.get('item_key'))
    quiz_item = {}
    try: quiz_item['topic_name'] = this_quiz_item.topic.name
    except: print this_quiz_item
    quiz_item['content'] = this_quiz_item.content
    quiz_item['answers'] = this_quiz_item.answers
    quiz_item['theme'] = this_quiz_item.theme
    template_values = quiz_item
    path = tpl_path(QUIZDEMO_PATH + 'quiz_item.html') # Pass Quiz Item to Template
    self.response.out.write(template.render(path, template_values))




class TakeQuiz(webapp.RequestHandler):
  #Load Plopquiz Homepage 
  def get(self):
    proficiencies = self.get_proficiencies()
    if proficiencies == None:
        all_proficiencies = Proficiency.all()
        proficiencies = [proficiency.name for proficiency in all_proficiencies.fetch(4)] 
    logging.debug(proficiencies)
    logging.debug('loading quiz...')    
    load_quiz = LoadQuiz()
    template_values = {"quiz_items": load_quiz.get(proficiencies), "proficiencies": proficiencies }
    logging.debug('loaded quiz...')    
    path = tpl_path(QUIZTAKER_PATH + 'takequiz.html')
    self.response.out.write(template.render(path, template_values))

  def get_proficiencies(self):
    all_proficiencies = Proficiency.all()
    if len(self.request.path.split('/quiz/')[1]) > 0:
		employer = Employer.gql('WHERE name = :1', self.request.path.split('/quiz/')[1].lower())
		try: these_proficiencies = employer.get().proficiencies
		except: return None
		proficiencies = []
		for p in these_proficiencies:
		   this_p = Proficiency.get_by_key_name(p)
		   proficiencies.append(this_p.name)
		return proficiencies        
		#except: return [proficiency.name for proficiency in all_proficiencies.fetch(4)]
    if self.request.get('proficiencies'):
        proficiencies = self.request.get('proficiencies')
        return proficiencies   
	return None
         


class QuizFrame(webapp.RequestHandler):
        def get(self):
                template_values = {}
                path = tpl_path(QUIZTAKER_PATH + 'quizframe.html')
                self.response.out.write(template.render(path, template_values))






class QuizComplete(webapp.RequestHandler):
  # Quiz Completed Screen
   def get(self):
    logging.debug('Loading Score')
    template_values = {}
    path = tpl_path(QUIZDEMO_PATH + 'quiz_complete.html')
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
    

 

# this is only used for the demo. 
class ViewSnaptalentQuiz(webapp.RequestHandler): # most work should go into its own file?
  #View Quiz
  quiz_array = []
  all_quiz_items = []
  proficiencies = {}
  QUIZ_ITEM_PER_PROFICIENCY = 5
    
  def get(self):
    self.proficiencies = {}
      # Create random list of three quiz items.
    if self.request.get('proficiencies'):
        quiz_items = []
        for p in eval(self.request.get('proficiencies')):  # TODO make these keys for easy lookup   -- these are proficiencies, not topics.
			this_p = Proficiency.gql("WHERE name = :1", p)
			q = QuizItem.gql("WHERE proficiency = :1", this_p.get())   # use topic for key
			quiz_items.extend(q.fetch(1000))
    # Query all quiz items
    else:
        q = db.GqlQuery("SELECT * FROM QuizItem")
        quiz_items = q.fetch(1000) 
    # Load Fixture Data if Necessary
        refresh_data("quiz_items", "quiet") 
        q = db.GqlQuery("SELECT * FROM QuizItem")
        quiz_items = q.fetch(1000)
    for item in quiz_items:
        self.load_item(item)
    self.load_array()
    template_values = {"quiz_items": self.quiz_array  }
    logging.debug(template_values)
    path = tpl_path(DEMO_PATH + 'ad.html')
    self.response.out.write(template.render(path, template_values))
    

  def load_item(self, item):
        random.shuffle(item.answers)
        item_answers = []
        [item_answers.append(str(a)) for a in item.answers]
        item_dict = {"answers": item_answers, "answer1" : item.answers[0], "answer2" : item.answers[1], "answer3": item.answers[2],  #answer1,2,3 is deprecated
        "proficiency": item.proficiency.name, "topic": item.topic.name, "key": item.key()}
        if item.proficiency.name not in self.proficiencies: self.proficiencies[item.proficiency.name] = []
        self.proficiencies[item.proficiency.name].append(item_dict)
        return self.proficiencies

  def load_array(self):
        self.quiz_array = []
        for prof_type in self.proficiencies:
            try: proficiency = random.sample(self.proficiencies[prof_type],
                                  self.QUIZ_ITEM_PER_PROFICIENCY)
            except ValueError: continue     #sample size larger than population
            self.quiz_array += proficiency
        random.shuffle(self.quiz_array)
        return self.quiz_array
        
        


class ViewNone(webapp.RequestHandler):

   def get(self):
       pass
