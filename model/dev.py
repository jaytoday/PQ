
from google.appengine.ext import db
from google.appengine.api import users


class Admin(db.Model):
  user = db.UserProperty(required=True) 
  date = db.DateTimeProperty(auto_now_add=True)

  

