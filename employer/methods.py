from model.quiz import QuizItem, ItemScore
from model.user import QuizTaker
from .model.proficiency import Proficiency, ProficiencyTopic
from .model.employer import Employer 
from .utils.utils import tpl_path, ROOT_PATH, raise_error
from utils import simplejson
from google.appengine.ext import db
from utils.gql_encoder import GqlEncoder, encode
    

def refresh_data(data_type, verbose):
  data = DataMethods()
  data.delete_data(data_type, verbose) 
  data.load_data(data_type, "") 
     

def load_data(data_type, verbose):
  data = DataMethods()
  data.load_data(data_type, "") 
       
 
def dump_data(gql_query):
  try:
	objects = gql_query.fetch(1000)
	return encode(objects)
  except:
	encode(objects)
	return "unable to encode objects"     
 

     
     
     
class DataMethods():
	
  def delete_data(self, data_type, *verbose):
		query = ""
		if data_type == "employers": query = db.GqlQuery("SELECT * FROM Employer")
		if not query: return False	
		objects = query.fetch(1000)
		for object in objects:
			if verbose[0] == "loud":
				print ""
				print "deleted: " + str(object.__dict__) 
			object.delete()
		return True
			
			
  def load_data(self, data_type, path):
		print data_type
		print ""
		json_file = open(ROOT_PATH + "/data/" + path + str(data_type) + ".json")
		json_str = json_file.read()
		newdata = simplejson.loads(json_str) # Load JSON file as object
		for entity in newdata:
			if data_type == 'employers':
				these_proficiencies = []
				for p in entity['proficiencies']:
				  these_proficiencies.append(Proficiency.get_or_insert(p, name = p).name)
				save_entity = Employer.get_or_insert(key_name=entity['name'],
				                                     unique_identifier = entity['unique_identifier'], 
				                                     name = entity['name'],
				                                     email = entity['email'],
				                                     proficiencies = these_proficiencies) 
			try: save_entity.put()	
			except:
				logging.error('Unable to save new entity')
				print 'Unable to save new entity'
			print "ADDED"
			print save_entity
			print save_entity.key()
		self.refresh_employer_images()   







  def register_employer(self, business_name, fullname):
	  new_employer = Employer(key_name=business_name, unique_identifier = business_name, name = fullname)
	  self.refresh_employer_images([new_employer])
	  new_employer.put()
	  return new_employer


  def delete_employer_images(self):
		from model.user import Profile, ProfilePicture
		for e in Employer.all().fetch(1000):
			try:  
				this_profile = Profile.get_by_key_name(e.unique_identifier)
				this_profile.photo.delete()
			except: pass 	
			
  def refresh_employer_images(self, employer_list=False):
		print "refreshing employer images"
		from google.appengine.api import images
		save_profiles = []
		from model.user import Profile, ProfilePicture
		self.delete_employer_images()
		if not employer_list: employers = Employer.all().fetch(1000)
		else: employers = employer_list
		for e in employers:
			print e.unique_identifier
			p_path = ROOT_PATH + "/data/img/business/"
			try: image_file = open(p_path + str(e.unique_identifier) + ".png")
			except: continue
			print "image found:", str(p_path + str(e.unique_identifier) + ".png")
			image = image_file.read()
			small_image = images.resize(image, 45, 45)
			large_image = images.resize(image, 95, 95)
			new_image = ProfilePicture(small_image = small_image,
									 large_image = large_image,
									 type = "employer"
									 )
			new_image.put()
			this_profile = Profile.get_by_key_name(e.unique_identifier)
			this_profile.photo = new_image
			save_profiles.append(this_profile)
		db.put(save_profiles)
			
