from utils import webapp
from .model.proficiency import Proficiency, ProficiencyTopic
from .utils.utils import ROOT_PATH, memoize, Debug, tpl_path
import datetime, time
from utils.webapp import template
from utils.gql_encoder import GqlEncoder, encode

FILE_CACHE_CONTROL = 'private, max-age=86400'
FILE_CACHE_TIME = datetime.timedelta(days=20)


def widget_path(template_file_name):
    import os
    return os.path.join(ROOT_PATH,
                        './widget', template_file_name)    
                        
    
class QuizJS(webapp.RequestHandler):
  @memoize('quiz_js')
  def get(self):
    DEFAULT_QUIZ_SUBJECT = "Misconceptions"
    if not Debug(): self.set_expire_header()
    try : 
        proficiency_arg = self.request.path.split('/quiz/')[1].replace('%20',' ')
        self.these_proficiencies = [Proficiency.get_by_key_name(proficiency_arg)]
    except: self.these_proficiencies = [Proficiency.get_by_key_name(DEFAULT_QUIZ_SUBJECT)]
    proficiency_names = [str(p.name) for p in self.these_proficiencies] 
    session_token = self.get_session_token()
    
    template_values = {
    'proficiencies': encode(proficiency_names).replace("\n", ""), 
    'user_token': session_token, 
    'css': self.get_widget_css().replace('\n','').replace("'",'"'),
    'widget_html': self.get_widget_html(), 
    'widget_subject': self.these_proficiencies[0].key(),
    'auto_start': self.get_auto_start() 
    }
     
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


  def get_widget_html(self):
  	QUIZTAKER_PATH = 'quiztaker/'
  	path = tpl_path(QUIZTAKER_PATH + '/widget/widget.html')
  	template_values = {'proficiencies': self.these_proficiencies}
  	return template.render(path, template_values)
  	
  @memoize('widget_css')
  def get_widget_css(self):
    template_values = {} 
    path = widget_path('pqwidget.css')
    return template.render(path, template_values)
    
  def get_auto_start(self):
  	if self.request.get('autostart') == "True":
  		return "true"
  	return "false"
	


# this might be deprecated since we're loading the css inline with the JS 
class QuizCSS(webapp.RequestHandler):
  @memoize('quiz_css')
  def get(self):
    self.response.headers['Content-Type'] = 'text/css'
    if not Debug(): self.set_expire_header()
    template_values = { } 
    path = widget_path('pqwidget.css')
    self.response.out.write(template.render(path, template_values))
    
  def set_expire_header(self):
      expires = datetime.datetime.now() + FILE_CACHE_TIME 
      self.response.headers['Cache-Control'] = FILE_CACHE_CONTROL
      self.response.headers['Expires'] = expires.strftime('%a, %d %b %Y %H:%M:%S GMT') # TODO: is this working? 
      
