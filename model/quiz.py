from google.appengine.ext import db
from google.appengine.api import users
import logging
from proficiency import *
from user import *


# Log a message each time this module get loaded.
logging.info('Loading %s', __name__)




class ContentPage(db.Model):
    url = db.LinkProperty()    # Where quiz material is from - wikipedia.org/en/neuroscience/
    date = db.DateTimeProperty(auto_now_add=True)
    proficiency = db.ReferenceProperty(Proficiency,
                                    collection_name='pages') # Proficiency Tag (startup_financing) 
                                    
    # for more than one topic, use list of keys. 
    # raw_items



class RawQuizItem(db.Model):
    page = db.ReferenceProperty(ContentPage,
                                    collection_name='raw_items') # Proficiency Tag (startup_financing)
    answer_candidates = db.StringListProperty() # List of Answers
    index = db.StringProperty() # Correct Answer
    pre_content = db.TextProperty() 
    content = db.TextProperty() 
    post_content = db.TextProperty() 
    moderated = db.BooleanProperty()
    




class QuizItem(db.Model):
  
  
  #slug = db.StringListProperty()  #Unique name ["wiki", "bayesian"] - [0] is source and [1] item is url path, like /science/cs/algorithm 
  #category = db.StringProperty()
  content = db.TextProperty()  # Content of Quiz Item
  index = db.StringProperty() # Correct Answer 
  answers = db.StringListProperty() # List of Answers
  proficiency = db.ReferenceProperty(Proficiency,
                                    collection_name='quizitems') # Proficiency Tag (startup_financing)
  topic = db.ReferenceProperty(ProficiencyTopic,
                                    required=False, collection_name='quizitems') # Proficiency Tag (startup_financing)                                  
  difficulty = db.IntegerProperty(default=0)  # 0-10000
  content_url = db.LinkProperty(required=False)    # Where quiz material is from - wikipedia.org/en/neuroscience/
  theme = db.StringProperty(required=False, default="default")
  date = db.DateTimeProperty(auto_now_add=True)



  def get_theme(self, url):
		#todo: fill this up 
		# eventually, store this in external json. 
		themes= [("wikipedia.org" "wiki"), ("knol.google.com", "knol")]
		for theme in themes:
			if theme[0] in url: return theme[1]

  """      
  @property
  def get_takers(self):   # Get all QuizTakers who have taken items
        this_items_scores = ItemScore.gql("WHERE quiz_item = :1", self.slug).get() 
        this_items_takers = [score.quiz_taker for score in this_items_scores]
        return this_items_takers



  def put(self): 
  self.proficiency_name = self.proficiency.name #Call put() on the super class. return db.SearchableModel.put(self)
  
  """ 



    
class ItemScore(db.Model):
  # Saved Scores for Quiz 
  quiz_taker = db.ReferenceProperty(QuizTaker,
                                    collection_name='itemscores')
  picked_answer = db.StringProperty() 
  correct_answer = db.StringProperty()                                 
  score = db.IntegerProperty()
  date = db.DateTimeProperty(auto_now_add=True)
  quiz_item = db.ReferenceProperty(QuizItem,
                                    required=True,
                                    collection_name='scores') # item slug - ["wiki", "bayesian"]
                                    
  type = db.StringProperty() # demo, stub, etc.
 

  



class QuizTakerFilter(db.Model):
  quiz_taker = db.ReferenceProperty(QuizTaker,
                                    collection_name='filter')  # One Quiz Taker Can Have Many Filters
  mean = db.IntegerProperty(default=0)
  variance = db.IntegerProperty(default=0)
  manhattan = db.IntegerProperty(default=0)
  nudges_count = db.IntegerProperty(default=0)
  trained = db.IntegerProperty(default=0)    # Either this can be integer for re-use, or new filter can be made if its True. 
  date = db.DateTimeProperty(auto_now_add=True)


class QuizItemFilter(db.Model):
  quiz_item = db.ReferenceProperty(QuizItem,
                                    collection_name='filter')  
  mean = db.IntegerProperty(default=0)
  variance = db.IntegerProperty(default=0)
  manhattan = db.IntegerProperty(default=0)
  nudges_count = db.IntegerProperty(default=0)
  trained = db.IntegerProperty(default=0)    # Either this can be integer for re-use, or new filter can be made if its True. 
  date = db.DateTimeProperty(auto_now_add=True)



class ItemScoreFilter(db.Model):
  score = db.ReferenceProperty(ItemScore,
                                    collection_name='filter')  
  trained = db.IntegerProperty(default=0)  
  residual = db.IntegerProperty(default=0)  
