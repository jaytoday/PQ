
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0


""" Plopquiz Demo




"""





from views import *



    
    
def main():
  logging.getLogger().setLevel(logging.DEBUG)
  
  application = webapp.WSGIApplication(
                                       [
                                        ('/demo/?',
                                         PQDemo),
                                        ('/preview/ad?',
                                         PQDemo),                                         
                                         ('/intro/?',
                                         PQIntro),
                                        ('/rpc/?',
                                         RPCHandler),                                                                                                                     
                                        ('/viewscore/?',
                                         ViewScore),
                                        ('/view_quiz/?',
                                         ViewQuiz), 
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
                                        ('/soup/?',
                                         Soup),
                                        ],
                                       debug=True)
  wsgiref.handlers.CGIHandler().run(application)



if __name__ == "__main__":
  main()

