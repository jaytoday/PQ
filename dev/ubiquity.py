import logging
import wsgiref.handlers
from utils import webapp
from utils.webapp import template
from google.appengine.ext import db
from utils.utils import tpl_path, memoize


# Template paths
DEV_PATH = 'dev/'



class QuizBuilder(webapp.RequestHandler):

  def get(self):
      if self.request.get('get') == "html": return self.get_html()
      if self.request.get('get') == 'js': return self.get_js()
      
  @memoize('ubiquity_html')
  def get_html(self):      
    template_values = {'text': self.request.get('text')}
    path = tpl_path(DEV_PATH +'ubiquity_builder.html')
    self.response.out.write(template.render(path, template_values))
    

  @memoize('ubiquity_js')
  def get_js(self):      
      template_values = {}
      path = tpl_path(DEV_PATH +'ubiquity_builder.js')
      self.response.out.write(template.render(path, template_values))
