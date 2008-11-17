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




    

class PQHandler(webapp.RequestHandler):
  logging.getLogger().setLevel(logging.DEBUG)
  
  application = webapp.WSGIApplication(
                                       [

										#Homepage
										('/?',
										 quiztaker.views.PQHome), 
										('/preview/?',
										 homepage.views.ExitPage),                                                                                  
										('/preview/homepage/?',
										 homepage.views.ViewHomepage),  
										('/preview/proficiency/?',
										 homepage.views.ChooseProficiency), 
										
										# Profiles
										('/preview/profile/?',
										 profiles.views.ViewProfile),
										('/preview/employer/profile/?',
										 profiles.views.ViewEmployerProfile),  
										('/preview/employer/profile/browse/?',
										 profiles.views.BrowseProfiles), 
										
										# Employers
										('/preview/employer/profile/browse/stats/?',
										 employer.views.Stats),                                                                                    
										('/preview/employer/load_profile/?',
										 profiles.views.LoadUserProfile),  
										
										
										# Snaptalent Demo
										('/demo/?',
										 quiztaker.views.PQDemo),
										('/preview/ad_embed/?',
										 quiztaker.views.PQDemo),
										('/st_quiz/?',
										quiztaker.views.ViewSnaptalentQuiz),
										
										# Taking Quizzes										  
										('/intro/?',
										 quiztaker.views.PQIntro),                                                                                                                 
										('/viewscore/?',
										 quiztaker.views.ViewScore),
										('/quiz_complete/?',
										 quiztaker.views.QuizComplete),                                         

										('/quiz_frame/?',
										 quiztaker.views.QuizFrame),                                        
										('/st_quiz/close/?',
										 quiztaker.views.ViewNone),     
										('/quiz/.*?',
										 quiztaker.views.TakeQuiz), 
										('/quiz_item/?',
										 quiztaker.views.QuizItemTemplate),                                         
										
										
										# Induction & Building Quizzes
										('/quizbuilder/?',
										 quizbuilder.views.QuizBuilder),
										('/quizbuilder/induction/?',
										 quizbuilder.views.InductionInterface),
										('/quizbuilder/item/?',
										 quizbuilder.views.RawItemTemplate), 


										# RPC Handlers
										('/quiztaker/rpc/?',
										 quiztaker.rpc.RPCHandler),    
										('/quizbuilder/rpc/?',
										 quizbuilder.rpc.RPCHandler),
										('/quizbuilder/rpc/post/?',
										 quizbuilder.rpc.RPCPostHandler),
										('/employer/rpc/?',
										 employer.rpc.RPCHandler),										   										 										
										
										 # Developer Pages
										 ('/dev/admin/?', 
										 dev.views.Admin),
										 ('/admin/?', 
										 admin),
										('/dev/load_topics/?',
										 dev.views.LoadTopics),  
										('/debug/?',
										 dev.views.Debug),  
										('/ranking/graph/?',
										 ranking.views.Graph),                                                                                       
										
										
										('/create_scores/?',
										 stubs.CreateScoreStubs),
										('/view_scores/?',
										 stubs.ViewScoreStubs),
										('/set_proficiencies/?',
										 stubs.Set_Proficiencies),
										('/set_difficulties/?',
										 stubs.Set_Difficulties),
										('/drilldown/?',
										 quizbuilder.views.Drilldown),
										 ('/.*', utils.NotFoundPageHandler)                                                                            
                                        ],
                                       debug=True)
  wsgiref.handlers.CGIHandler().run(application)                                  
  




if __name__ == "__main__":
  PQHandler()




