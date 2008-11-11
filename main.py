import logging
from google.appengine.ext import webapp
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


    
    
def url_handler():
  logging.getLogger().setLevel(logging.DEBUG)
  
  application = webapp.WSGIApplication(
                                       [
                                        ('/demo/?',
                                         quiztaker.views.PQDemo),
                                        ('/preview/ad_embed/?',
                                         quiztaker.views.PQDemo),  
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
                                        ('/intro/?',
                                         quiztaker.views.PQIntro),
                                        ('/quiztaker/rpc/?',
                                         quiztaker.rpc.RPCHandler),                                                                                                                     
                                        ('/viewscore/?',
                                         quiztaker.views.ViewScore),
                                        ('/quiz_complete/?',
                                         quiztaker.views.QuizComplete),                                         
                                        ('/st_quiz/?',
                                         quiztaker.views.ViewSnaptalentQuiz), 
                                        ('/st_quiz/close/?',
                                         quiztaker.views.ViewNone),     
                                         
                                                                             
                                        ('/quiz/.*?',
                                         quiztaker.views.TakeQuiz), 
                                        ('/quiz_item/?',
                                         quiztaker.views.QuizItemTemplate),                                         
                                        ('/?',
                                         quiztaker.views.PQHome),                                        
                                        ('/create_scores/?',
                                         stubs.CreateScoreStubs),
                                        ('/view_scores/?',
                                         stubs.ViewScoreStubs),
                                        ('/set_proficiencies/?',
                                         stubs.Set_Proficiencies),
                                        ('/set_difficulties/?',
                                         stubs.Set_Difficulties),
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
                                         ('/dev/admin/?', 
                                         dev.views.Admin),
                                         ('/admin/?', 
                                         admin),                                         
                                        ('/quiz_frame/?',
                                         quiztaker.views.QuizFrame),
                                        ('/drilldown/?',
                                         quizbuilder.views.Drilldown),
                                        ('/employer/rpc/?',
                                         employer.rpc.RPCHandler),                                        

                                        ('/dev/load_topics/?',
                                         dev.views.LoadTopics),  

                                        ('/debug/?',
                                         dev.views.Debug),  
                                         
                                        ('/ranking/graph/?',
                                         ranking.views.Graph),  
                                                                                                                           
                                        ],
                                       debug=True)
  wsgiref.handlers.CGIHandler().run(application)



if __name__ == "__main__":
  url_handler()

