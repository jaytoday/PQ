import logging
from utils import webapp
import wsgiref.handlers
from utils import utils
from utils import stubs as stubs
from dev import *
import quiztaker.views
import quiztaker.rpc
import quizbuilder.views
import quizbuilder.rpc
import dev.views
import homepage.views
import quizbuilder
import profiles.views
import employer.views
from google.appengine.ext import admin
import employer.rpc
import ranking.views


class Quizbuilder(webapp.RequestHandler):
  def get(self, *args):
	  logging.getLogger().setLevel(logging.DEBUG)
	  application = webapp.WSGIApplication(
										   [
											('/quizbuilder/?',
											 quizbuilder.views.QuizBuilder),
											('/quizbuilder/induction/?',
											 quizbuilder.views.InductionInterface),
											('/quizbuilder/rpc/?',
											 quizbuilder.rpc.RPCHandler),
											('/quizbuilder/rpc/post/?',
											 quizbuilder.rpc.RPCPostHandler),                                         
											('/quizbuilder/item/?',
											 quizbuilder.views.RawItemTemplate),
											],
										   debug=True)
	  
	  wsgiref.handlers.CGIHandler().run(application)



class Dev(webapp.RequestHandler):
  def get(self):
	  logging.getLogger().setLevel(logging.DEBUG)
	  application = webapp.WSGIApplication(
										   [
											 ('/dev/admin/?', 
											 dev.views.Admin),
											 ('/admin/?', 
											 admin),                                         
											('/drilldown/?',
											 quizbuilder.views.Drilldown),
											('/dev/load_topics/?',
											 dev.views.LoadTopics),  
											('/debug/?',
											 dev.views.Debug),                                                                                   
											],
										   debug=True)
	  
	  wsgiref.handlers.CGIHandler().run(application)


class Preview(webapp.RequestHandler):

  	
  def get(self):
  	  logging.debug('b')
	  logging.getLogger().setLevel(logging.DEBUG)
	  application = webapp.WSGIApplication(
										   [
											('/preview/?',
											 homepage.views.ExitPage),                                                                                  
											('/preview/homepage/?',
											 homepage.views.ViewHomepage),  
											('/preview/proficiency/?',
											 homepage.views.ChooseProficiency), 
											('/preview/profile/?',
											 profiles.views.ViewProfile),
											('/preview/employer/profile/?',
											 profiles.views.ViewEmployerProfile),  
											('/preview/employer/profile/browse/?',
											 profiles.views.BrowseProfiles), 
											('/preview/employer/profile/browse/stats/?',
											 employer.views.Stats),                                                                                    
											('/preview/employer/load_profile/?',
											 profiles.views.LoadUserProfile), 
											],
										   debug=True)
	  
	  wsgiref.handlers.CGIHandler().run(application)
  
                                                                                  
                                         
