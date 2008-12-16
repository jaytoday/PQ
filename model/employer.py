from google.appengine.ext import db
from google.appengine.api import users
import logging
from proficiency import Proficiency
import quiz

# Log a message each time this module get loaded.
logging.info('Loading %s', __name__)



class Employer(db.Model):
    unique_identifier = db.StringProperty(required=False) # should be soon...
    email = db.EmailProperty(required=False)
    name = db.StringProperty()
    proficiencies = db.StringListProperty() 



class AutoPledge(db.Model):
    employer = db.ReferenceProperty(Employer,
                                    required=True, collection_name='auto_pledges')
    count = db.IntegerProperty(required=True) #  number of autopledges yet.                                   
    proficiency = db.ReferenceProperty(Proficiency,
                                    required=True, collection_name='auto_pledges')
                                    
    # Put BP down 5000 for Automotive Industry. Then give out pledges as people take tests.                             
