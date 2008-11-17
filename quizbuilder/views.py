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
from utils.webapp import template
from google.appengine.ext import db
from google.appengine.api import users
from utils import webapp
from utils.webapp import util
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


class RawItemTemplate(webapp.RequestHandler):

    def get(self):
        template_values = {}
        self.request.get
        path = tpl_path(QUIZBUILDER_PATH + 'raw_item_template.html')
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
        
            
