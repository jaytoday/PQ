from views import *
from utils import *
from dev import *
import quizbuilder



    
    
def url_handler():
  logging.getLogger().setLevel(logging.DEBUG)
  
  application = webapp.WSGIApplication(
                                       [
                                        ('/demo/?',
                                         PQDemo),
                                        ('/preview/ad_embed/?',
                                         PQDemo),                                         
                                         ('/intro/?',
                                         PQIntro),
                                        ('/rpc/?',
                                         RPCHandler),                                                                                                                     
                                        ('/viewscore/?',
                                         ViewScore),
                                        ('/quiz_complete/?',
                                         QuizComplete),                                         
                                        ('/view_quiz/?',
                                         ViewQuiz), 
                                        ('/view_quiz/close/?',
                                         ViewNone),                                         
                                        ('/quiz/?',
                                         QuizItemTemplate),                                         
                                        ('/?',
                                         PQHome),  
                                        ('/refresh_data/?',
                                         RefreshData),
                                        ('/dump_data/?',
                                         DumpData),                                          
                                        ('/create_scores/?',
                                         CreateScoreStubs),
                                        ('/view_scores/?',
                                         ViewScoreStubs),
                                        ('/set_proficiencies/?',
                                         Set_Proficiencies),
                                        ('/set_difficulties/?',
                                         Set_Difficulties),
                                        ('/quizbuilder/?',
                                         QuizBuilder),
                                        ('/quizbuilder/induction/?',
                                         InductionInterface),
                                        ('/quizbuilder/rpc/?',
                                         quizbuilder.rpc.RPCHandler),
                                         ('/dev/?(.*)/?', 
                                         URIRouter),
                                        ('/quiz_frame/?',
                                         QuizFrame),
                                        ],
                                       debug=True)
  wsgiref.handlers.CGIHandler().run(application)



if __name__ == "__main__":
  url_handler()

