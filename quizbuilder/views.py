import logging
from utils.webapp import template
from google.appengine.ext import db
from google.appengine.api import users
from utils import webapp
from utils.webapp.util import login_required
from .utils.utils import tpl_path, admin_only
from model.proficiency import Proficiency
from model.quiz import QuizItem

QUIZBUILDER_PATH = 'quizbuilder/'           
              
class QuizBuilder(webapp.RequestHandler):

    @admin_only
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



class QuizEditor(webapp.RequestHandler):
	"""

	Contribute to quiz material for a subject. 

	"""

	@login_required
	def get(self):
		try: this_subject = self.get_subject()
		except: return #self.redirect('/error/subject_not_found')
		template_values = {'subject': this_subject, 'new_item': self.new_item_template() }
		template_values['ANSWERCOUNT'] = range(1,3)
		path = tpl_path(QUIZBUILDER_PATH + 'quiz_editor.html')
		self.response.out.write(template.render(path, template_values))
		
	def get_subject(self):
		# Get subject from path
			import string #string.capwords() 
			subject_name = self.request.path.split('/edit/')[1].replace("%20"," ")  #TODO - instead of capwords, make all subject names lowercase
			this_subject = Proficiency.get_by_key_name(subject_name)
			assert this_subject is not None
			return this_subject       
				
	def new_item_template(self):
			new_item = {}
			return list(new_item)
			 


class InductionInterface(webapp.RequestHandler):

    @admin_only
    def get(self):
        template_values = {}
        path = tpl_path(QUIZBUILDER_PATH + 'induction.html')
        self.response.out.write(template.render(path, template_values))
        




           
class Drilldown(webapp.RequestHandler):

    def get(self):
        template_values = {}
        path = tpl_path('drilldown.html')
        self.response.out.write(template.render(path, template_values))
        
            
