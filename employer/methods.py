from model.quiz import QuizItem, ItemScore
from model.user import QuizTaker
from .model.proficiency import Proficiency, ProficiencyTopic
from .model.employer import Employer 
from .utils.utils import tpl_path, ROOT_PATH, raise_error
from utils import simplejson
from google.appengine.ext import db
from utils.gql_encoder import GqlEncoder, encode
import logging


     
     
class DataMethods():
	


  def create_business_account(self, uid, proficiencies=False):
	from accounts.methods import register_account, register_user
	import string
	fullname = string.capwords(uid.replace("_", " "))
	business_account = register_account(uid, fullname)
	business_profile = register_user(uid, fullname, fullname, False)
	business_employer = self.register_employer(uid, fullname, proficiencies)
	return business_account, business_profile, business_employer 


  def register_employer(self, business_name, fullname, proficiencies=False):
	  print "registering ", business_name
	  new_employer = Employer.get_or_insert(key_name=business_name, unique_identifier = business_name, name = fullname)
	  if proficiencies: new_employer.proficiencies = proficiencies
	  self.refresh_employer_images([new_employer])
	  new_employer.put()
	  return new_employer


  def delete_employer_images(self):
		from model.user import Profile, ProfilePicture
		for e in Employer.all().fetch(1000):
			try:  
				this_profile = Profile.get_by_key_name(e.unique_identifier)
				if this_profile.photo.type != "pq": this_profile.photo.delete()
			except: pass 	
			
  def refresh_employer_images(self, employer_list=False):

		from google.appengine.api import images
		save_profiles = []
		from model.user import Profile, ProfilePicture
		self.delete_employer_images()
		if not employer_list: employers = Employer.all().fetch(1000)
		else: employers = employer_list
		for e in employers:
			p_path = ROOT_PATH + "/data/img/business/"
			try: image_file = open(p_path + str(e.unique_identifier) + ".png")
			except: continue
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
		logging.info('refreshed %d employer images', len(save_profiles))
		if save_profiles: print "refreshed employer images for", [p.unique_identifier for p in save_profiles]
			
