import logging
from google.appengine.api import urlfetch
import cgi
import wsgiref.handlers
import datetime, time
import string
from utils.webapp import template
from google.appengine.ext import db
from google.appengine.api import users
from utils import webapp, simplejson
from utils.random import jsonp
from utils.gql_encoder import GqlEncoder, encode
from utils.webapp import util
from .utils.utils import tpl_path, ROOT_PATH, raise_error
from .model.quiz import QuizItem, ItemScore
from .model.user import QuizTaker
from .model.employer import Employer 
from .model.proficiency import Proficiency, ProficiencyTopic 
from load_quiz import LoadQuiz


# Template paths
QUIZTAKER_PATH = 'quiztaker/'
QUIZDEMO_PATH = 'quiztaker/demo/'
DEMO_PATH = 'demo/'







class PQDemo(webapp.RequestHandler):   # This is just for the demo
  #Load Ad Embed Preview Page
  def get(self):
    template_values = {}
    path = tpl_path(DEMO_PATH +'example_blog.html')
    self.response.out.write(template.render(path, template_values))
    


class QuizItemTemplate(webapp.RequestHandler):
  # TODO: Error Handling, so client can display error messages, logs, etc.
  def get(self):
    logging.info('loading quiz item')
    template_values = {}
    if self.request.get('item_key'): this_quiz_item = QuizItem.get(self.request.get('item_key'))
    if self.request.get('token'): 
        from google.appengine.api import memcache
        self.session = memcache.get(self.request.get('token'))
        this_item = self.session.get('current_item', False)
        if this_item: this_quiz_item = QuizItem.get(this_item['key'])
        else: 
            logging.warning('token used past expiration', self.request.get('token'))
            return False
    quiz_item = {}
    try: quiz_item['topic_name'] = this_quiz_item.topic.name
    except: print this_quiz_item
    if this_quiz_item.content.endswith('.'): this_quiz_item.content = this_quiz_item.content[:-1] + "<br/>" # this should be done in advance,and it should replace </span>. with </span><br/>
    quiz_item['content'] = this_quiz_item.content
    quiz_item['answers'] = this_quiz_item.answers
    quiz_item['theme'] = this_quiz_item.theme
    template_values = quiz_item
    if self.request.get('demo') == 'true': path = tpl_path(QUIZDEMO_PATH + 'quiz_item.html')
    else: path = tpl_path(QUIZTAKER_PATH + 'quiz_item.html')
    if self.request.get("callback"):
            self.response.out.write(jsonp(self.request.get("callback"), template.render(path, template_values)))
    else:
            self.response.out.write(template.render(path, template_values))



class TakeQuiz(webapp.RequestHandler):
  #Load Quiz Based on Path Argument
  def get(self):
    load_proficiencies = self.get_proficiencies()
    proficiencies = load_proficiencies[0]
    vendor = load_proficiencies[1] 
    if proficiencies[0] == None:
        logging.info('quiz not found for argument %s', load_proficiencies[0])
        return self.redirect('/quiz_not_found/') 
    load_quiz = LoadQuiz()
    if vendor == "": vendor = self.get_default_vendor()
    template_values = {"proficiencies": proficiencies, "quiz_subject": str(proficiencies[0].name), "vendor_name": vendor.name.capitalize(), "vendor": vendor.key() }
    path = tpl_path(QUIZTAKER_PATH + 'takequiz.html')
    self.response.out.write(template.render(path, template_values))

  def get_proficiencies(self):
  # Get proficiencies from path
    DEFAULT_QUIZ_SUBJECT = "Recovery.Gov"
    if len(self.request.path.split('/quiz/')[1]) > 0:
		import string
		this_proficiency = self.request.path.split('/quiz/')[1].replace("%20"," ") #TODO - instead of capwords, make all subject names lowercase
		return [[Proficiency.get_by_key_name(this_proficiency)], ""]  # This only allows one proficiency, and no vendor. 
		"""
    if self.request.get('proficiencies'):
        proficiencies = self.request.get('proficiencies')
        return [eval(proficiencies,{"__builtins__":None},{}), self.get_default_vendor()] 
        """ 
    # if no quiz argument, return newest Quiz Subject
    return [[Proficiency.get_by_key_name(DEFAULT_QUIZ_SUBJECT)], ""]	   
         
  def get_default_vendor(self):
	plopquiz = Employer.gql("WHERE name = :1", "Plopquiz")
	return plopquiz.get()



    
class PQIntro(webapp.RequestHandler): 
  def get(self):
	logging.info('loading quiz intro')
	template_values = {}
	if self.request.get('subject'): template_values['proficiencies'] = self.get_quiz_subjects()
	    
	intro_template = QUIZTAKER_PATH + self.request.get('page') + ".html"
	if self.request.get('demo') == "true": intro_template = QUIZDEMO_PATH + self.request.get('page') + ".html" # only for demo
	path = tpl_path(intro_template)
	if self.request.get("callback"):
			response = jsonp(self.request.get("callback"), template.render(path, template_values))
			self.response.out.write(response);
	else:
			self.response.out.write(template.render(path, template_values))

  def get_quiz_subjects(self):
		from model.proficiency import Proficiency
		quiz_subjects = Proficiency.gql("WHERE status = 'public' ORDER BY name DESC" ).fetch(6)
		for p in quiz_subjects:
		    if p.name == eval(self.request.get('subject'))[0]: 
		        quiz_subjects.remove(p)
		        quiz_subjects.insert(0, p)
		        continue
		return quiz_subjects[0:5]
		    
		    
		    
		        
class Widget(webapp.RequestHandler):
        # Load Quiz Widget
        def get(self):
                path = tpl_path(QUIZTAKER_PATH + '/widget/widget.html')
                proficiencies = [Proficiency.get(self.request.get('proficiency'))]
                template_values = {'proficiencies': proficiencies}
                self.response.out.write(template.render(path, template_values))
                 
                 
                 
                        
                        
class QuizFrame(webapp.RequestHandler):
        # Load HTML layout for Quiz
        def get(self):
                template_values = {}
                path = tpl_path(QUIZTAKER_PATH + 'quizframe.html')
                if self.request.get("callback"):
                        response = jsonp(self.request.get("callback"), template.render(path, template_values))
                        self.response.headers['Content-Type'] = 'application/x-javascript'
                        self.response.out.write(response);
                else:
                        self.response.out.write(template.render(path, template_values))





class QuizComplete(webapp.RequestHandler):
  # Quiz Completed Screen
   def get(self):
	logging.info('Loading Quiz Completed Frame')
	template_values = {}
	path = tpl_path(QUIZDEMO_PATH + 'quiz_complete.html')
	if self.request.get("callback"):
			response = jsonp(self.request.get("callback"), template.render(path, template_values))
			self.response.out.write(response);
	else:
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
        q = db.GqlQuery("SELECT * FROM QuizItem")
        quiz_items = q.fetch(1000)
    import random
    for item in quiz_items:
        self.load_item(item, random)
    self.load_array(random)
    template_values = {"quiz_items": self.quiz_array  }
    logging.debug(template_values)
    path = tpl_path(DEMO_PATH + 'ad.html')
    self.response.out.write(template.render(path, template_values))
    

  def load_item(self, item, random):
        random.shuffle(item.answers)
        item_answers = []
        [item_answers.append(str(a)) for a in item.answers]
        item_dict = {"answers": item_answers, "answer1" : item.answers[0], "answer2" : item.answers[1], "answer3": item.answers[2],  #answer1,2,3 is deprecated
        "proficiency": item.proficiency.name, "topic": item.topic.name, "key": item.key()}
        if item.proficiency.name not in self.proficiencies: self.proficiencies[item.proficiency.name] = []
        self.proficiencies[item.proficiency.name].append(item_dict)
        return self.proficiencies

  def load_array(self, random):
        self.quiz_array = []
        for prof_type in self.proficiencies:
            try: proficiency = random.sample(self.proficiencies[prof_type],
                                  self.QUIZ_ITEM_PER_PROFICIENCY)
            except ValueError: continue     #sample size larger than population
            self.quiz_array += proficiency
        random.shuffle(self.quiz_array)
        return self.quiz_array
        
        


class ViewNone(webapp.RequestHandler): # Deprecated

   def get(self):
       pass







            
"""
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
	if self.request.get("callback"):
			response = jsonp(self.request.get("callback"), template.render(path, template_values))
			self.response.out.write(response);
	else:
			self.response.out.write(template.render(path, template_values))

"""
