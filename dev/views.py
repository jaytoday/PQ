import logging
# Log a message each time this module get loaded.
logging.info('Loading %s', __name__)
import cgi
import wsgiref.handlers
import datetime, time
from utils.webapp import template
from google.appengine.ext import db
from google.appengine.api import users
from utils import webapp, simplejson
from .model.quiz import QuizItem, ItemScore
from .model.user import QuizTaker
from utils.utils import ROOT_PATH, tpl_path
from utils.gql_encoder import GqlEncoder, encode
from ranking.methods import TopicLevelData, ProficiencyLevelData

# Template paths
QUIZTAKER_PATH = 'quiztaker/'
QUIZBUILDER_PATH = 'quizbuilder/'
DEV_PATH = 'dev/'



class Admin(webapp.RequestHandler):
  #Load admin page

  def get(self):

    template_values = {}
    path = tpl_path(DEV_PATH +'admin.html')
    self.response.out.write(template.render(path, template_values))
    



class LoadTopics(webapp.RequestHandler):
  def get(self):
	print ""
	json_file = open(ROOT_PATH + "/data/topics.json")
	json_str = json_file.read()
	newdata = simplejson.loads(json_str) # Load JSON file as object
	topics = []
	types = []
	for t in newdata:
	   topics.append(t)
	   print t['name']

	return
	template_values = {}
	path = tpl_path(DEV_PATH +'admin.html')
	self.response.out.write(template.render(path, template_values))
    


class Debug(webapp.RequestHandler):
  def get(self):
      if self.request.get('quiz_item'): return self.quiz_item(self.request.get('quiz_item'))
  def quiz_item(self, item_key):
		item = QuizItem.get(item_key)
		item_answers = []
		[item_answers.append(str(a)) for a in item.answers]  		
		quiz_item = {"answers": item_answers, "answer1" : item.answers[0], "answer2" : item.answers[1], "answer3": item.answers[2],  #answer1,2,3 is deprecated
		"proficiency": item.proficiency.name, "topic": item.topic.name, "key": item.key()}      
		template_values = {"quiz_items": [quiz_item]}
		logging.debug('loaded quiz...')
		path = tpl_path(QUIZTAKER_PATH + 'debug_quiz.html')
		self.response.out.write(template.render(path, template_values))



class SetProficiencyLevels(webapp.RequestHandler):
  def get(self):
      quiz_takers = QuizTaker.all().fetch(20)
      ptl = TopicLevelData()
      for qt in quiz_takers:
          ptl.set(qt)
      pl = ProficiencyLevelData()
      for qt in quiz_takers:
          pl.set(qt)      
      
          
      



