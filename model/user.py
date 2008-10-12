from google.appengine.ext import db
from google.appengine.api import users
import logging



# Log a message each time this module get loaded.
logging.info('Loading %s', __name__)

      
  
  
  

  
class InviteList(db.Model):
  # Beta Invite List
  email = db.StringProperty()
  date = db.DateTimeProperty(auto_now_add=True)

