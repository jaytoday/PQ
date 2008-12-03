import logging
# Log a message each time this module get loaded.
logging.info('Loading %s', __name__)
import random
from utils import webapp
from utils.webapp import util
from .utils.utils import tpl_path, ROOT_PATH, raise_error
from .model.quiz import QuizItem, ItemScore
from .model.user import QuizTaker
from .model.proficiency import Proficiency, ProficiencyTopic 
from methods import refresh_data
# Template paths
QUIZTAKER_PATH = 'quiztaker/'
DEMO_PATH = 'demo/'

    
    
    
class LoadQuiz(): 
  #View Quiz
  quiz_array = []
  all_quiz_items = []
  proficiencies = {}
  QUIZ_ITEM_PER_PROFICIENCY = 5
    
  def get(self, proficiencies):
	self.proficiencies = {}
	# Create random list of three quiz items.
	quiz_items = []
	#try: proficiencies = eval(proficiencies)  # when passed in via url
	#except: pass
	logging.debug('getting proficiencies...')
	for p in proficiencies:  # TODO make these keys for easy lookup   -- these are proficiencies, not topics.
		this_p = Proficiency.gql("WHERE name = :1", p)
		q = QuizItem.gql("WHERE proficiency = :1", this_p.get())   # use topic for key
		quiz_items.extend(q.fetch(1000))
	logging.debug('loading items...')		
	for item in quiz_items:
		try: self.load_item(item)
		except: logging.debug('unable to load item')
	self.load_array()
	return self.quiz_array 


    

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
        if len(self.proficiencies) == 1: self.QUIZ_ITEM_PER_PROFICIENCY = 10  # in case there is only one proficiency
        for prof_type in self.proficiencies:
            try: proficiency = random.sample(self.proficiencies[prof_type],
                                  self.QUIZ_ITEM_PER_PROFICIENCY)
            except ValueError: continue     #sample size larger than population
            self.quiz_array += proficiency
        random.shuffle(self.quiz_array)
        return self.quiz_array
        
  						




class QuizSession(): 

	def __init__(self, session):
		self.session = session
		
	def load_quiz_items(self, profNames):
		self.load_quiz = LoadQuiz();
		# proficiencies should be resolved from employer/user at earlier point.
		proficiencies = self.get_proficiencies(profNames)
		quiz_items = self.get_quiz_items(proficiencies)
		return self.next_quiz_item()

	def get_proficiencies(self, profNames):
		proficiencies = []
		for p in profNames:
		   this_p = Proficiency.get_by_key_name(p)
		   proficiencies.append(this_p.name)
		self.session['proficiencies'] = proficiencies
		return proficiencies


	def get_quiz_items(self, proficiencies):
		quiz_items = self.load_quiz.get(proficiencies)
		self.session['quiz_items'] = quiz_items
		return quiz_items



	def next_quiz_item(self):
		next_item = self.session['quiz_items'].pop()
		return next_item
		
