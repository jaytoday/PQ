
from google.appengine.ext import db
from google.appengine.api import users
import logging



# Log a message each time this module get loaded.
logging.info('Loading %s', __name__)



class Proficiency(db.Model):
  name = db.StringProperty(required=True)  # Proficiency Tag (startup_financing)
  date = db.DateTimeProperty(auto_now_add=True)
  modified = db.DateTimeProperty(auto_now=True)
  blurb = db.TextProperty(required=False)
  status = db.StringProperty(required=False)
  #images - RefProperty
  def tag(self): # for views
  	tag = self.name.replace(' ', '_')
  	return tag
  #quizitems -- QuizItem reference
  ## pages  
  




class ProficiencyTopic(db.Model):  # sub-topics within proficiencies - These map to content URLs.
  name = db.StringProperty(required=True)
  proficiency = db.ReferenceProperty(Proficiency, collection_name='topics') # Proficiency Tag (startup_financing)
  date = db.DateTimeProperty(auto_now=True)    
  #freebase_guid ?
  
  

class SubjectImage(db.Model):
    proficiency = db.ReferenceProperty(Proficiency, collection_name='images', required=True) # Proficiency Tag (startup_financing)    
    small_image = db.BlobProperty(required=True)
    large_image = db.BlobProperty(required=True)
