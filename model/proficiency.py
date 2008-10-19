
from google.appengine.ext import db
from google.appengine.api import users
import logging



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
  ## pages  
  
