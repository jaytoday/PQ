from utils import webapp
from .model.proficiency import Proficiency, ProficiencyTopic
from .utils.utils import ROOT_PATH, memoize, Debug
import datetime, time
from utils.webapp import template
from utils.gql_encoder import GqlEncoder, encode

FILE_CACHE_CONTROL = 'private, max-age=86400'
FILE_CACHE_TIME = datetime.timedelta(days=20)


def widget_path(template_file_name):
    import os
    return os.path.join(ROOT_PATH,
                        './static/widget', template_file_name)    
                        
    
class QuizJS(webapp.RequestHandler):
  @memoize('quiz_js')
  def get(self):
    if not Debug(): self.set_expire_header()
    proficiency_arg = self.request.path.split('/quiz/')[1].replace('%20',' ')
    these_proficiencies = Proficiency.gql("WHERE name = :1", proficiency_arg).fetch(1) #TODO: should use .get_by_key_name() method
    proficiency_names = [str(p.name) for p in these_proficiencies] 
    session_token = self.get_session_token()
    template_values = {'proficiencies': encode(proficiency_names).replace("\n", ""), 'user_token': session_token, 'widget_subject': these_proficiencies[0].key() } #encode(proficiency_names).replace("\n", "")
    path = widget_path('pqwidget.js')
    self.response.out.write(template.render(path, template_values))
    
  def set_expire_header(self):
      expires = datetime.datetime.now() + FILE_CACHE_TIME 
      self.response.headers['Cache-Control'] = FILE_CACHE_CONTROL
      self.response.headers['Expires'] = expires.strftime('%a, %d %b %Y %H:%M:%S GMT')

  def get_session_token(self):
  	from google.appengine.api import memcache
	from utils.utils import hash_pipe
	token = hash_pipe(datetime.datetime.now())
	
	#token = hash_pipe(self.session['user'].unique_identifier) # TODO: in most cases, there won't be a session. 
	#memcache.set(token, self.session['user'].unique_identifier, 60000)
	return token

    
class QuizCSS(webapp.RequestHandler):
  @memoize('quiz_css')
  def get(self):
    if not Debug(): self.set_expire_header()
    template_values = { } 
    path = widget_path('pqwidget.css')
    print ""
    print template.render(path, template_values)
    #self.response.out.write(template.render(path, template_values))
    
  def set_expire_header(self):
      expires = datetime.datetime.now() + FILE_CACHE_TIME 
      self.response.headers['Cache-Control'] = FILE_CACHE_CONTROL
      self.response.headers['Expires'] = expires.strftime('%a, %d %b %Y %H:%M:%S GMT')
      
