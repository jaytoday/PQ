from google.appengine.ext import db
from google.appengine.api import users
import logging
import user 


# Log a message each time this module get loaded.
logging.info('Loading %s', __name__)

      




class Account(db.Model):
    #key_name = unique_identifier 
    unique_identifier = db.StringProperty(required=True) # redundant
    pass_count = db.IntegerProperty(required=False) 
