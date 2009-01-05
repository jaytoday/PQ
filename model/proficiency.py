
from google.appengine.ext import db

"""

# Get or Insert when unique key_name isn't possible. 

from google.appengine.ext import db

class SuperModel(db.Model):
  @classmethod
  def get_or_insert_by(cls, parent=None, **kwds):
    query = db.Query(cls)
    if parent is not None:
      query.ancestor(parent)
    for kw in kwds:
      query.filter("%s =" % kw, kwds[kw])
    entity = query.get()
    if entity is not None:
      return entity
    entity = cls(parent, **kwds)
    return entity

class Movie(SuperModel):
  name = db.StringProperty()
  year = db.IntegerProperty()

movie = Movie.get_or_insert_by(name="Magnolia", year=1999)
if not movie.is_saved():
  movie.put()




"""

class Proficiency(db.Model):
  name = db.StringProperty(required=True)  # Proficiency Tag (startup_financing)
  date = db.DateTimeProperty(auto_now_add=True)
  modified = db.DateTimeProperty(auto_now=True)
  status = db.StringProperty(required=False)
  #subject material
  blurb = db.TextProperty(required=False)
  link_html = db.TextProperty()
  video_html = db.TextProperty()
  popularity = db.IntegerProperty()
  difficulty = db.IntegerProperty() 
 
  
  def tag(self): # for views
  	tag = self.name.replace(' ', '_')
  	return tag
  	
  #images - RefProperty
  #quizitems -- QuizItem reference
  ## pages  

  def default_image(self): 
      return DefaultSubjectImage.get()


      
class ProficiencyTopic(db.Model):  # sub-topics within proficiencies - These map to content URLs.
  name = db.StringProperty(required=True)
  proficiency = db.ReferenceProperty(Proficiency, collection_name='topics') # Proficiency Tag (startup_financing)
  date = db.DateTimeProperty(auto_now=True)    
  #freebase_guid ?
  
  

class SubjectImage(db.Model):
    proficiency = db.ReferenceProperty(Proficiency, collection_name='images', required=True) # Proficiency Tag (startup_financing)    
    small_image = db.BlobProperty(required=True)
    large_image = db.BlobProperty(required=True)


  	

class DefaultSubjectImage(db.Model):
    small_image = db.BlobProperty(required=True)
    large_image = db.BlobProperty(required=True)
