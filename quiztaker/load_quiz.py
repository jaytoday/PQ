import logging
import random
from utils import webapp
from utils.webapp import util
from .utils.utils import tpl_path, ROOT_PATH, raise_error, hash_pipe, Debug
from .model.quiz import QuizItem, ItemScore
from .model.user import QuizTaker
from .model.employer import Employer 
from .model.proficiency import Proficiency, ProficiencyTopic 
from google.appengine.api import memcache
# Template paths
QUIZTAKER_PATH = 'quiztaker/'
DEMO_PATH = 'demo/'


# TODO: Better logging
    
    
    
class LoadQuiz(): 
  #View Quiz
  quiz_array = []
  all_quiz_items = []
  proficiencies = {}
  QUIZ_ITEM_PER_PROFICIENCY = 1
    
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
	if Debug():
		from utils.appengine_utilities.sessions import Session
		self.session = Session()
  	for item in quiz_items:
		try: self.load_item(item)
		except: logging.debug('unable to load item')
	self.load_array()
	return self.quiz_array 



    

  def load_item(self, item):
        random.shuffle(item.answers)
        item_answers = []
        [item_answers.append(str(a)) for a in item.answers] # is this necessary?
        if Debug():
        	item_answers = self.god_mode(item, item_answers)
        item_dict = {"answers": item_answers, "key": item.key(), "proficiency": item.proficiency.name, "topic": item.topic.name}
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
        
  						

  def god_mode(self, item, item_answers): # check if god mode is enabled
  	if self.session['god_mode']: 
		try: item_answers[item_answers.index(item.index)] = str(item.index) + "!"
		except: logging.debug('unable to run god mode process')
	return item_answers


class QuizSession(): 
     ##### TODO: Better logging

	def initiate(self):
		token = self.make_quiz_session()
		import time
		self.session["start"] = time.clock()
		self.session["token"] = token
		return token 

	def make_quiz_session(self):
		self.session = {'start': None, 'token': None, 'user': None,}
		token = hash_pipe("mytoken")
		memcache.set(token, self.session, 60000)
		return token

	def get_last_quiz_item(self, token):
	 return memcache.get(token)
	 

	def get_quiz_session(self, token):
	 return memcache.get(token)
	  
		
	def load_quiz_items(self, profNames, token):
		self.session = self.get_quiz_session(token)
		print self.session
		self.load_quiz = LoadQuiz();
		proficiencies = self.get_proficiencies(profNames)
		quiz_items = self.get_quiz_items(proficiencies)
		if len(self.session['quiz_items']) < 1: return False
		else: self.session['current_item'] = self.session['quiz_items'][0]
		memcache.replace(token, self.session, 60000)
		return proficiencies
		

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


	def next_quiz_item(self, token):
		self.session = self.get_quiz_session(token)
		try: 
		    next_item = self.session['quiz_items'].pop()
		    self.session['current_item'] = next_item
		    #del next_item['key'] - is this necessary?  
		except IndexError: return False #no items left
		memcache.replace(token, self.session, 60000)
		return next_item
		


	def add_score(self, picked_answer, timer_status, token, vendor):
		logging.info('Posting the Score')  
		self.session = self.get_quiz_session(token)
		this_item = QuizItem.get(self.session['current_item']['key']) 
		#Lookup quiz item with slug, clean it, and match it. 
		picked_clean = picked_answer.strip()
		picked_clean = picked_clean.lower()
		correct_clean = this_item.index.strip()
		correct_clean = correct_clean.lower()

		if picked_clean == correct_clean:
			timer_status = float(timer_status)
			this_score = int(round(timer_status * 100))
		else:
			this_score = 0

		# Need Better Temp Storing 
							 
		score = ItemScore(quiz_item = this_item.key(),
						  score = this_score,
						  correct_answer = this_item.index,
						  picked_answer = picked_answer,
						  type = token # temp storage
						  )

		"""
		user = self.session['user']
		if user:
			this_user = QuizTaker.get_by_key_name(user)
			score.quiz_taker = this_user.key()
			score.type = "site"     # type could be site, practice widget
		else:
			score.type = "temp"
		"""
		if len(vendor) > 0: score.vendor = Employer.get(vendor)
		score.put()
		logging.info('Score entered by user %s with score %s, picked: %s, correct: %s'
					% (score.quiz_taker, score.score, score.picked_answer, score.correct_answer))
		


	# save temporary scores
	def update_scores(self, token, unique_identifier):
		logging.info('Transferring Score')  
		this_user = QuizTaker.get_by_key_name(unique_identifier)
		save_items = []
		these_items = ItemScore.gql("WHERE type = :1", token).fetch(1000)
		for i in these_items:
			i.quiz_taker = this_user
			save_items.append(i)
		from google.appengine.ext import db
		db.put(save_items)
		return True
