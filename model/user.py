from google.appengine.ext import db
from google.appengine.api import users
import logging
from model.proficiency import Proficiency, ProficiencyTopic

# Log a message each time this module get loaded.
logging.info('Loading %s', __name__)

      




class QuizTaker(db.Model):
    #key_name = unique_identifier 
    unique_identifier = db.StringProperty(required=False) # redundant
    nickname = db.StringProperty(required=False)    
    #Quiz Info 
    
    scores = db.ListProperty(db.Key) # ItemScore keys
    levels = db.ListProperty(db.Key) # ProficiencyLevel keys
    modified = db.DateTimeProperty(auto_now=True)

    #itemscores  -- ItemScore reference
    #proficiency_levels -- ProficiencyLevel reference         TODO: Rank from top to bottom? 
    #topic_levels - Topic Level reference

    @property
    def get_level_for_proficiency(self, proficiency):   # Get proficiency_levels for user 
        return ProficiencyLevel.gql("WHERE quiz_taker = :1 AND proficiency = :2", self.key(), proficiency).get()
    

    

class ProfilePicture(db.Model):
    small_image = db.BlobProperty(required=True)
    large_image = db.BlobProperty(required=True)	    
    date = db.DateTimeProperty(auto_now=True)
    type = db.StringProperty(required=False)        
    
    

class Profile(db.Model):
    #key_name = unique_identifier 
    unique_identifier = db.StringProperty(required=True) # redundant
    email = db.EmailProperty(required=False)
    nickname = db.StringProperty(required=True)
    profile_path = db.StringProperty(required=True)
    fullname = db.StringProperty(required=False)
    modified = db.DateTimeProperty(auto_now=True)
    
    #scores = db.ListProperty(db.Key) # ItemScore keys
    #levels = db.ListProperty(db.Key) # ProficiencyLevel keys    
    
    
    #Awards, Gifts and Scholarships - Use Family Structure
    # awards
    #gifts = 
    
    
    
    # Personal info 
    name = db.StringProperty()
    occupation = db.StringProperty(required=False)
    work_status = db.StringProperty(required=False)
    location = db.StringProperty(required=False)
    webpage = db.LinkProperty(required=False)
    aboutme = db.TextProperty(required=False)
    quote = db.TextProperty(required=False)
    
    # Image
    photo = db.ReferenceProperty(ProfilePicture,
                                    collection_name='profile')  # One Quiz Taker Can Have Many Filters
    
    # When Signed Up
    date = db.DateTimeProperty(auto_now_add=True)
    
    

class ProficiencyLevel(db.Model):
  proficiency = db.ReferenceProperty(Proficiency,required=True,collection_name='pro_levels') # Proficiency Tag (startup_financing)
  quiz_taker = db.ReferenceProperty(QuizTaker,required=True, collection_name='proficiency_levels')
  proficiency_level = db.IntegerProperty()
  percentile = db.IntegerProperty()  
  modified = db.DateTimeProperty(auto_now=True)


class TopicLevel(db.Model):
  topic = db.ReferenceProperty(ProficiencyTopic,required=True,collection_name='top_levels') # Proficiency Tag (startup_financing)
  quiz_taker = db.ReferenceProperty(QuizTaker,required=True,collection_name='topic_levels')
  topic_level = db.IntegerProperty()
  percentile = db.IntegerProperty(required=False)  
  modified = db.DateTimeProperty(auto_now=True)

  
  
  
  
  

  
class InviteList(db.Model):
  # Beta Invite List
  email = db.StringProperty()
  date = db.DateTimeProperty(auto_now_add=True)

