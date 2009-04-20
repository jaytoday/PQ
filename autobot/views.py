import logging
from utils.webapp import template
from google.appengine.ext import db
from utils import webapp

from model.proficiency import Proficiency
from model.quiz import QuizItem

EDITOR_PATH = 'editor/'           
              
class Autobot(webapp.RequestHandler):

    def get(self):
    	all_quizzes = QuizItem.all().fetch(1000)
    	for quiz in all_quizzes:
    		print quiz.answers
    	print "i am the autobot!"
