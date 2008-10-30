from google.appengine.ext import db
from google.appengine.api import users
import logging
import proficiency 
import quiz

# Log a message each time this module get loaded.
logging.info('Loading %s', __name__)

      
  


class Employer(db.Model):
    email = db.EmailProperty(required=True)
    name = db.StringProperty()
    proficiencies = db.StringListProperty()
