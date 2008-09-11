from google.appengine.ext import db
from google.appengine.api import users
import logging

# Log a message each time this module get loaded.
logging.info('Loading %s', __name__)



class Score(db.Model):
  # Yay for Grades.
  author = db.StringProperty()
  score = db.StringProperty()
  date = db.DateTimeProperty(auto_now_add=True)
  picked_answer = db.StringProperty()
  correct_answer = db.StringProperty()


class List(db.Model):
  # Beta List
  email = db.StringProperty()
  date = db.DateTimeProperty(auto_now_add=True)



class QuizItem(db.Model):
  # Yay for Grades.
  slug = db.StringProperty()
  index = db.StringProperty()
  answers = db.StringListProperty()
  proficiency = db.StringProperty()
  date = db.DateTimeProperty(auto_now_add=True)
  
