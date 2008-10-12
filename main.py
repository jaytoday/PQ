import logging
from utils import utils
import model
from utils import stubs as stubs
from dev import *
import quiztaker.views
import quiztaker.rpc
import quizbuilder.views
import quizbuilder.rpc


import quizbuilder




    
    
def url_handler():
  logging.getLogger().setLevel(logging.DEBUG)
  
  application = webapp.WSGIApplication(
                                       [
                                        ('/demo/?',
                                         quiztaker.views.PQDemo),
                                        ('/preview/ad_embed/?',
                                         quiztaker.views.PQDemo),                                         
                                         ('/intro/?',
                                         quiztaker.views.PQIntro),
                                        ('/rpc/?',
                                         quiztaker.rpc.RPCHandler),                                                                                                                     
                                        ('/viewscore/?',
                                         quiztaker.views.ViewScore),
                                        ('/quiz_complete/?',
                                         quiztaker.views.QuizComplete),                                         
                                        ('/view_quiz/?',
                                         quiztaker.views.ViewQuiz), 
                                        ('/view_quiz/close/?',
                                         quiztaker.views.ViewNone),                                         
                                        ('/quiz/?',
                                         quiztaker.views.QuizItemTemplate),                                         
                                        ('/?',
                                         quiztaker.views.PQHome),  
                                        ('/refresh_data/?',
                                         quiztaker.views.RefreshData),
                                        ('/dump_data/?',
                                         quiztaker.views.DumpData),                                          
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
                                         ('/dev/?(.*)/?', 
                                         URIRouter),
                                        ('/quiz_frame/?',
                                         quiztaker.views.QuizFrame),
                                        ],
                                       debug=True)
  wsgiref.handlers.CGIHandler().run(application)



if __name__ == "__main__":
  url_handler()

