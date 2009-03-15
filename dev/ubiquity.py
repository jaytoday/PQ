import logging
import wsgiref.handlers
from utils import webapp
from utils.webapp import template
from google.appengine.ext import db
from utils.utils import tpl_path, memoize


# Template paths
DEV_PATH = 'dev/'



class QuizEditor(webapp.RequestHandler):

  def post(self):
      if self.request.get('get') == "html": return self.get_html()
      if self.request.get('get') == 'js': return self.get_js()
      

  def get_html(self):
    
    import urllib
    template_values = {'text': urllib.unquote( self.request.get('text') ) }
    from model.proficiency import Proficiency 
    if self.request.get('subject_key'): template_values['subject_key'] = self.request.get('subject_key')
    else: 
      subjects = Proficiency.gql("WHERE status = 'public'").fetch(1000) 
      template_values['subjects'] = subjects
    if self.request.get('topic_key'): template_values['topic_key'] = self.request.get('topic_key')
    path = tpl_path(DEV_PATH +'ubiquity_builder.html')
    self.response.out.write(template.render(path, template_values))
    

  @memoize('ubiquity_js')
  def get_js(self):      
      template_values = {}
      path = tpl_path(DEV_PATH +'ubiquity_builder.js')
      self.response.out.write(template.render(path, template_values))
