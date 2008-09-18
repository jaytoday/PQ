from google.appengine.ext import db
from google.appengine.api import users
import logging

# Log a message each time this module get loaded.
logging.info('Loading %s', __name__)



class TempItemScore(db.Model):
  # Scores for Quiz Item (Temporary Store for Demo)  TODO: Include Timer Data
  quiz_taker = db.StringProperty()
  score = db.IntegerProperty()   # 0-1, after Timer data is used
  date = db.DateTimeProperty(auto_now_add=True)
  picked_answer = db.StringProperty()
  correct_answer = db.StringProperty()
  quiz_item = db.StringProperty() # item slug - "wiki_bayesian"


class ItemScore(db.Model):
  # Saved Scores for Quiz 
  quiz_taker = db.StringProperty()
  score = db.IntegerProperty()
  date = db.DateTimeProperty(auto_now_add=True)
  picked_answer = db.StringProperty()
  correct_answer = db.StringProperty()
  quiz_item = db.StringProperty()
  

class StubItemScore(db.Model):
  # Saved Scores for Quiz - NOT REAL
  quiz_taker = db.StringProperty()
  score = db.IntegerProperty()  
  date = db.DateTimeProperty(auto_now_add=True)
  picked_answer = db.StringProperty()
  correct_answer = db.StringProperty()
  quiz_item = db.StringProperty()
  
  
    
# When user submits e-mail address, transfer each score to perm model, and change quiz_taker to e-mail address.
  


class QuizItem(db.Model):
  # 
  slug = db.StringProperty()  #Unique name (wiki_bayesian)
  index = db.StringProperty() # Correct Answer 
  answers = db.StringListProperty() # List of Answers
  proficiency = db.StringProperty() # Proficiency Tag (startup_financing)
  date = db.DateTimeProperty(auto_now_add=True)
  difficulty = db.IntegerProperty()  # 0-1
  
  

class Proficiency(db.Model):
  proficiency = db.StringProperty()  # Proficiency Tag (startup_financing)
  date = db.DateTimeProperty(auto_now_add=True)
  

class ProficiencyLevel(db.Model):
  proficiency = db.StringProperty()  # Proficiency Tag (startup_financing)
  quiz_taker = db.StringProperty()
  proficiency_level = db.IntegerProperty()
  date = db.DateTimeProperty(auto_now_add=True)

  
  
  
  
  
  
  
class InviteList(db.Model):
  # Beta Invite List
  email = db.StringProperty()
  date = db.DateTimeProperty(auto_now_add=True)


