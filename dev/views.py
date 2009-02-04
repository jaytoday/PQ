import logging
import cgi
import wsgiref.handlers
from utils import webapp
from utils.webapp import template
from google.appengine.ext import db
from utils.utils import ROOT_PATH, tpl_path, admin_only
from utils.gql_encoder import encode

# Template paths
QUIZTAKER_PATH = 'quiztaker/'
QUIZBUILDER_PATH = 'quizbuilder/'
DEV_PATH = 'dev/'



class Admin(webapp.RequestHandler):
  #Load admin page
  @admin_only
  def get(self):
    if self.request.get('shortcut') == 'login':
        return self.dev_login()
    template_values = {}
    path = tpl_path(DEV_PATH +'admin.html')
    self.response.out.write(template.render(path, template_values))
    


  def dev_login(self):
	if not self.request.get('uid'):
		self.response.out.write('please enter a uid')
		return
	self.session['unique_identifier'] = self.request.get('uid')
	self.redirect('/register')



class LoadTopics(webapp.RequestHandler):
  def get(self):
	print ""
	json_file = open(ROOT_PATH + "/data/topics.json")
	json_str = json_file.read()
	from utils import simplejson
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
      if self.request.get('error') == '500': return dict['this'] # test 500 errors
  def quiz_item(self, item_key):
		from model.quiz import QuizItem
		item = QuizItem.get(item_key)
		item_answers = []
		[item_answers.append(str(a)) for a in item.answers]  		
		quiz_item = {"answers": item_answers, "answer1" : item.answers[0], "answer2" : item.answers[1], "answer3": item.answers[2],  #answer1,2,3 is deprecated
		"proficiency": item.proficiency.name, "topic": item.topic.name, "key": item.key()}      
		template_values = {"quiz_items": [quiz_item]}
		logging.debug('loaded quiz...')
		path = tpl_path(QUIZTAKER_PATH + 'debug_quiz.html')
		self.response.out.write(template.render(path, template_values))



class EditSubjects(webapp.RequestHandler):
  def get(self):
		#from model.proficiency import SubjectProfile
		#subjects = SubjectProfile.all().fetch(1000)
		#template_values = {"subjects": subjects}
		from model.proficiency import Proficiency
		proficiencies = Proficiency.all().fetch(1000)
		template_values = {'proficiencies': proficiencies}
		path = tpl_path(DEV_PATH + 'edit_subjects.html')
		self.response.out.write(template.render(path, template_values))		





class Error(webapp.RequestHandler):
  def get(self):
	error_type = self.request.path.split('/error/')[1]   
	if error_type == "browser": return self.browser_error()
	template_values = {"error_type": error_type}
	logging.debug('loaded error page for error type %s',  error_type)
	path = tpl_path('utils/error.html')
	self.response.out.write(template.render(path, template_values))

  def browser_error(self):
	template_values = {"browser_type": self.request.environ['HTTP_USER_AGENT']}
	logging.debug('loaded browser error page for browser type %s',  self.request.environ['HTTP_USER_AGENT'])
	path = tpl_path('utils/browser_error.html')
	self.response.out.write(template.render(path, template_values))
