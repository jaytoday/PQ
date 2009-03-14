import logging
import wsgiref.handlers
from utils import webapp
from utils.webapp import template
from google.appengine.ext import db
from utils.utils import tpl_path, memoize


# Template paths
EDITOR_PATH = 'editor/'



class QuizEditor(webapp.RequestHandler):

  def get(self):
      if self.request.get('get') == "html": return self.get_html()
      if self.request.get('get') == 'js': return self.get_js()
      
  @memoize('portable_html') # TODO: The markup can be cached, except for the places where the text template tag is used. (and short cache on subjects)
  def get_html(self):
    from model.proficiency import Proficiency 
    subjects = Proficiency.gql("WHERE status = 'public'").fetch(1000) 
    template_values = {'text': self.request.get('text'), 'subjects': subjects}
    path = tpl_path(EDITOR_PATH +'portable.html')
    self.response.out.write(template.render(path, template_values))
    

  @memoize('portable_js')
  def get_js(self):      
      template_values = {}
      path = tpl_path(EDITOR_PATH +'portable.js')
      self.response.out.write(template.render(path, template_values))
