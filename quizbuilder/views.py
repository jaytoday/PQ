import logging
# Log a message each time this module get loaded.
logging.info('Loading %s', __name__)
import random
import string
import re
import cgi
import wsgiref.handlers
import os
import datetime, time
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
import simplejson

from .model.quiz import ContentPage, RawQuizItem, QuizItem
from .model.proficiency import  Proficiency, ProficiencyTopic
from .utils.utils import tpl_path

QUIZBUILDER_PATH = 'quizbuilder/'           
              
class QuizBuilder(webapp.RequestHandler):

    def get(self):
        template_values = {}
        path = tpl_path(QUIZBUILDER_PATH + 'quizbuilder.html')
        self.response.out.write(template.render(path, template_values))






class InductionInterface(webapp.RequestHandler):

    def get(self):
        template_values = {}
        path = tpl_path(QUIZBUILDER_PATH + 'induction.html')
        self.response.out.write(template.render(path, template_values))
        




           
class Drilldown(webapp.RequestHandler):

    def get(self):
        template_values = {}
        path = tpl_path('drilldown.html')
        self.response.out.write(template.render(path, template_values))
        
            
