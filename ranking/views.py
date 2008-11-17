import logging
# Log a message each time this module get loaded.
logging.info('Loading %s', __name__)
import random
import cgi
import wsgiref.handlers
import datetime, time
import string
from utils.webapp import template
from google.appengine.ext import db
from google.appengine.api import users
from utils import webapp
from .utils.utils import tpl_path, ROOT_PATH, raise_error
from .model.quiz import QuizItem, ItemScore
from .model.user import QuizTaker
from .model.proficiency import Proficiency, ProficiencyTopic 

# Template paths
RANKING_PATH = 'ranking/'



class Graph(webapp.RequestHandler):
  def get(self):
    template_values = {}
    path = tpl_path(RANKING_PATH + 'graph.html')
    self.response.out.write(template.render(path, template_values))
    

