import logging
from utils.webapp import template
from google.appengine.ext import db
#from google.appengine.api import users
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
		from model.quiz import QuizItem
		from model.user import Profile
		from model.proficiency import ProficiencyTopic
		try: self.get_subject()
		except: print "SUBJECT NOT FOUND" #self.redirect('/error/subject_not_found')
		from quizbuilder.methods import get_membership, get_user_items
		try:self.subject_membership = get_membership(self.session['user'], self.this_subject)
		except: print "NOT A MEMBER"
		template_values = {'subject': self.this_subject, 
		                   'user_items': get_user_items(self.session['user'], self.this_subject), 
		                   'subject_membership': self.subject_membership }
		template_values['ANSWERCOUNT'] = range(1,3)
		path = tpl_path(QUIZBUILDER_PATH + 'quiz_editor.html')
		self.response.out.write(template.render(path, template_values))
		
	def get_subject(self):
		# Get subject from path
			import string #string.capwords() 
			subject_name = self.request.path.split('/edit/')[1].replace("%20"," ")  #TODO - instead of capwords, make all subject names lowercase
			self.this_subject = Proficiency.get_by_key_name(subject_name)
			assert self.this_subject is not None
     

     


			
				 


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
        
            
