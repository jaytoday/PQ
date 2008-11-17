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

HOMEPAGE_PATH = 'homepage/'           
              
class ChooseProficiency(webapp.RequestHandler):

    def get(self):
        template_values = {}
        path = tpl_path(HOMEPAGE_PATH + 'proficiency.html')
        self.response.out.write(template.render(path, template_values))


class ViewHomepage(webapp.RequestHandler):

    def get(self):
        template_values = {}
        path = tpl_path(HOMEPAGE_PATH + 'homepage.html')
        self.response.out.write(template.render(path, template_values))


class ExitPage(webapp.RequestHandler):

    def get(self):
        template_values = {}
        path = tpl_path(HOMEPAGE_PATH + 'exit.html')
        if self.request.get('o'): path = tpl_path(HOMEPAGE_PATH + 'old_exit.html')  #for demo, and old time's sake.
        self.response.out.write(template.render(path, template_values))

