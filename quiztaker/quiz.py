import logging
import md5
import random
import time


from .model.employer import Employer 
from .model.proficiency import Proficiency, ProficiencyTopic 
from .model.quiz import QuizItem, ItemScore
 
from utils import webapp
from quiztaker.load_quiz import LoadQuiz

 
class Main(webapp.RequestHandler):
	def get(self):
		if not self.session["start"]:
				self.session["start"] = time.clock();
		if self.request.get("prof"): return self.load_quiz_items()

	def load_quiz_items(self):
		self.load_quiz = LoadQuiz();
		profString = self.request.get("prof").replace("%20", " ");
		profNames = profString.split(",");
		# proficiencies can be loaded at initialization
		proficiencies = self.get_proficiencies(profNames)
		quiz_items = self.get_quiz_items(proficiencies)
		return self.next_quiz_item()

		self.response.out.write(self.request.get("callback") + "('" + self.next_quiz_item + "');");



	def get_proficiencies(self, profNames):
		proficiencies = []
		for p in profNames:
		   this_p = Proficiency.get_by_key_name(p)
		   proficiencies.append(this_p.name)
		self.session['proficiencies'] = proficiencies
		return proficiencies


	def get_quiz_items(self, proficiencies):
		quiz_items = self.load_quiz.get(proficiencies)
		session['quiz_items'] = quiz_items
		return quiz_items



	def next_quiz_item(self):
		return self.session['quiz_items'].pop()


