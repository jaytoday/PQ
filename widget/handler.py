from utils import webapp
from .model.proficiency import Proficiency, ProficiencyTopic
from .utils.utils import ROOT_PATH, memoize, Debug, tpl_path, GetUserAgent
import datetime, time
from utils.webapp import template
from utils.gql_encoder import GqlEncoder, encode

FILE_CACHE_CONTROL = 'private, max-age=86400'
FILE_CACHE_TIME = datetime.timedelta(days=5)


def widget_path(template_file_name):
    import os
    return os.path.join(ROOT_PATH,
                        './widget', template_file_name)    
                        
    
class QuizJS(webapp.RequestHandler):

  def get(self):
    if not Debug(): self.set_expire_header()
    if "Mozilla/4.0" in GetUserAgent(): return self.browser_error()
    return self.load_quiz_js()
    
    	
  @memoize('quiz_js') # will this cache incorrectly? 
  def load_quiz_js(self):
    JQUERY_VERSION = '1.3.1'
    DEFAULT_QUIZ_SUBJECT = "Recovery.Gov"
    try : 
        proficiency_arg = self.request.path.split('/quiz/')[1].replace('%20',' ')
        this_proficiency = Proficiency.get_by_key_name(proficiency_arg)
        assert this_proficiency != None
        self.these_proficiencies = [this_proficiency]
    except: self.these_proficiencies = [Proficiency.get_by_key_name(DEFAULT_QUIZ_SUBJECT)]
    proficiency_names = [str(p.name) for p in self.these_proficiencies] 
    session_token = self.get_session_token()
    
    template_values = {
    'proficiencies': encode(proficiency_names).replace("\n", ""), 
    'user_token': session_token, 
    'css': self.get_widget_css().replace('\n','').replace("'",'"'),
    'widget_html': self.get_widget_html(), 
    'widget_subject': self.these_proficiencies[0].key(),
    'jquery_version' : JQUERY_VERSION,
    'jquery_location': JQUERY_VERSION,
    'auto_start': self.get_auto_start() 
    }
     
    path = widget_path('pqwidget.js')
    from utils.random import minify
    self.response.out.write(  minify(template.render(path, template_values))  )

        
            
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
    from utils.random import css_minify
    return css_minify( template.render(path, template_values) )
    
  def get_auto_start(self):
  	if self.request.get('autostart') == "True":
  		return "true"
  	return "false"
	


  def browser_error(self):
    DEFAULT_QUIZ_SUBJECT = "Recovery.Gov"
    if not Debug(): self.set_expire_header()
    try : 
        proficiency_arg = self.request.path.split('/quiz/')[1].replace('%20',' ')
        this_proficiency = Proficiency.get_by_key_name(proficiency_arg)
        assert this_proficiency != None
        self.these_proficiencies = [this_proficiency]
    except: self.these_proficiencies = [Proficiency.get_by_key_name(DEFAULT_QUIZ_SUBJECT)]
    proficiency_names = [str(p.name) for p in self.these_proficiencies] 
    session_token = self.get_session_token()
    
    template_values = {
    'quiz_subject': encode(proficiency_names[0]).replace("\n", "")
    }
     
    path = widget_path('error.js')
    from utils.random import minify
    self.response.out.write(  minify(template.render(path, template_values))  )
    
