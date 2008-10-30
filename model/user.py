from google.appengine.ext import db
from google.appengine.api import users
import logging
import proficiency 
import quiz

# Log a message each time this module get loaded.
logging.info('Loading %s', __name__)

      
  


class QuizTaker(db.Model):
    email = db.EmailProperty(required=True)
    name = db.StringProperty()
    scores = db.ListProperty(db.Key) # ItemScore keys
    levels = db.ListProperty(db.Key) # ProficiencyLevel keys
    date = db.DateTimeProperty(auto_now_add=True)
    work_status = db.StringProperty(required=False)
    location = db.StringProperty(required=False)
    webpage = db.StringProperty(required=False)
    about = db.StringProperty(required=False)
    quote = db.TextProperty(required=False)
    # storing personal image? 
    #itemscores  -- ItemScore reference
    #proficiency_levels -- ProficiencyLevel reference
    """
    
    Foreign Key Usages
    
    james = QuizTaker.gql("WHERE email = James")
    for score_key in james.scores:
       ItemScore.get(score_key)
    
    newscore = Score()
    james = QuizTaker()
    james.scores.append(newscore.key())
    
    totalscore += score.score for score in james.itemscores
    
    for score in scores:
        if score.key() not in quiz_taker.scores 
    takers_score = Score.gql("
    
    """ 
    
    @property
    def get_level_for_proficiency(self, proficiency):   # Get proficiency_levels for user 
        return ProficiencyLevel.gql("WHERE quiz_taker = :1 AND proficiency = :2", self.key(), proficiency).get()
    




class ProficiencyLevel(db.Model):
  proficiency = db.ReferenceProperty(proficiency.Proficiency,
                                    required=True,
                                    collection_name='level') # Proficiency Tag (startup_financing)
  quiz_taker = db.ReferenceProperty(QuizTaker,
                                    required=True,
                                    collection_name='proficiency_levels')
  proficiency_level = db.IntegerProperty()
  date = db.DateTimeProperty(auto_now_add=True)

  
  
  

  
class InviteList(db.Model):
  # Beta Invite List
  email = db.StringProperty()
  date = db.DateTimeProperty(auto_now_add=True)

