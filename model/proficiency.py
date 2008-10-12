"""

from google.appengine.ext import db
from google.appengine.api import users
import logging
import quiz as quiz


# Log a message each time this module get loaded.
logging.info('Loading %s', __name__)



class Proficiency(db.Model):
  name = db.StringProperty(required=True)  # Proficiency Tag (startup_financing)
  date = db.DateTimeProperty(auto_now_add=True)
  #quizitems -- QuizItem reference




class ProficiencyTopic(db.Model):  # sub-topics within proficiencies - These map to content URLs.
  name = db.StringProperty(required=True)
  proficiency = db.ReferenceProperty(Proficiency,
                                    collection_name='topics') # Proficiency Tag (startup_financing)
  date = db.DateTimeProperty(auto_now_add=True)    
  #freebase_guid ?
  # urls 
      
  
  




class ProficiencyLevel(db.Model):
  proficiency = db.ReferenceProperty(Proficiency,
                                    required=True,
                                    collection_name='level') # Proficiency Tag (startup_financing)
  quiz_taker = db.ReferenceProperty(quiz.QuizTaker,
                                    required=True,
                                    collection_name='proficiency_levels')
  proficiency_level = db.IntegerProperty()
  date = db.DateTimeProperty(auto_now_add=True)

  
  
 
"""
