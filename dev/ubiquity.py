import logging
import cgi
import wsgiref.handlers
from utils import webapp
from utils.webapp import template
from google.appengine.ext import db
from utils.utils import tpl_path


# Template paths
DEV_PATH = 'dev/'



class QuizBuilder(webapp.RequestHandler):

  def get(self):
    template_values = {}
    path = tpl_path(DEV_PATH +'ubiquity_builder.html')
    self.response.out.write(template.render(path, template_values))
    


