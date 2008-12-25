
from google.appengine.ext import db


class Admin(db.Model):
  user = db.UserProperty(required=True) 
  date = db.DateTimeProperty(auto_now_add=True)

  

