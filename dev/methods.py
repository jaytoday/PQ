import logging
# Log a message each time this module get loaded.
logging.info('Loading %s', __name__)
from utils.gql_encoder import GqlEncoder, encode
from google.appengine.ext import db
from .model.quiz import QuizItem, RawQuizItem, ProficiencyTopic, ContentPage, Proficiency
from .utils.utils import tpl_path, ROOT_PATH, raise_error
from utils import simplejson
from .quiztaker.methods import DataMethods as quiztaker_methods
from .employer.methods import DataMethods as employer_methods
from google.appengine.api import images
from .model.user import ProfilePicture	
from .model.proficiency import SubjectImage

def dump_data(gql_query):
	try:
		objects = gql_query.fetch(1000)
		return encode(objects)
		#for object in objects:
	except:
		return "unable to encode objects"
		

def load_data(data_type, verbose):
    data = DataMethods()
    return data.load_data(data_type, "")


def refresh_data(data_type, verbose):
    data = DataMethods()
    query = {"proficiencies": Proficiency.all(), 'proficiency_topics': ProficiencyTopic.all(), 'content_pages': ContentPage.all(), 'raw_items' : RawQuizItem.all()}
    data.delete_data(query[data_type])
    return data.load_data(data_type, "")

def restore_backup():
	build = Build()
	build.refresh_profile_images()
	data = DataMethods()
	data_types =  ["proficiencies", 'proficiency_topics', 'employers', 'content_pages', 
	                'raw_items', 'raw_items', 'quiz_items', 'mailing_list']
	                #TODO - These will break after refresh, and should be wiped during deletion process, if not restored. 
	                #'accounts', 'proficiency_level', 'topic_level',
	                #TODO 'awards', 'sponsorships', 
	for data_type in data_types:
		data.load_data(data_type, "/backup/")
	build.refresh_subject_images()
    

class Build():

	def refresh_profile_images(self):
		self.delete_profile_images()
		image_range = range(3) # change this as you add more. range() is always one int ahead.
		for i in image_range:
			print "loading image"
			image_file = open(ROOT_PATH + "/data/img/profile/profile_" + str(i) + ".png")
			image = image_file.read()
			small_image = images.resize(image, 45, 45)
			large_image = images.resize(image, 95, 95)

			new_image = ProfilePicture(small_image = small_image,
									   large_image = large_image,
									   type="pq")
			new_image.put()
			new_image.key_name = str(new_image.key())# or this?
			new_image.put()
									
	def delete_profile_images(self):
		pq_pics = ProfilePicture.gql("WHERE type = :1", "pq").fetch(1000)
		print "deleting profiles images:", pq_pics
		for p in pq_pics:
		  p.delete()	

		  		
	def refresh_subject_images(self, *args):
		self.delete_subject_images()
		self.refresh_default_subject_image()
		proficiencies = Proficiency.all().fetch(1000)
		for p in proficiencies:
			p_path = ROOT_PATH + "/data/img/subject/" + str(p.name) + "/"
			print p_path
			for n in range(3):
				try: image_file = open(p_path + str(n) + ".png")
				except: continue
				print "image found:", str(p_path + str(n) + ".png")
				image = image_file.read()
				small_image = images.resize(image, 120, 80)
				large_image = images.resize(image, 360, 240)
				new_image = SubjectImage(small_image = small_image,
				                         large_image = large_image,
				                         proficiency = p
									     )
				new_image.put()
				new_image.key_name = str(new_image.key()) # why would I do this?
				new_image.put()
					
		
	def delete_subject_images(self):
		pics = SubjectImage.all().fetch(1000)
		print "deleting %d subject images" % len(pics)
		for p in pics:
		  p.delete()			
				

		
	def refresh_default_subject_image(self):
		tile_path = ROOT_PATH + "/data/img/base/pq_tile.png"
		image_file = open(tile_path)
		image = image_file.read()
		small_image = images.resize(image, 120, 80)
		large_image = images.resize(image, 360, 240)
		from model.proficiency import DefaultSubjectImage
		for i in DefaultSubjectImage.all().fetch(1000): i.delete() # delete old images 
		default_image = DefaultSubjectImage(small_image = small_image,
									 large_image = large_image)
		default_image.put()
		print ""
		print "saved default image: ", default_image							     
								
			
				
   	    		
	
class DataMethods():

  def delete_data(self, query):
     print ""
     entities = query.fetch(1000)
     for entity in entities:
     	print "DELETED"
     	print entity.__dict__
     	entity.delete()

    
  def load_data(self, data_type, path):
		print data_type
		print ""
		json_file = open(ROOT_PATH + "/data/" + path + str(data_type) + ".json")
		json_str = json_file.read()
		newdata = simplejson.loads(json_str) # Load JSON file as object
		entities = []
		for entity in newdata:
			if data_type == 'proficiencies':
				save_entity = Proficiency.get_or_insert(key_name=entity['name'], name = entity['name'], blurb = entity.get("blurb", ""))
				save_entity.status = entity.get('status', None)
				save_entity.vlurb = entity.get('blurb', None)
			if data_type == 'proficiency_topics':
				this_proficiency = Proficiency.gql("WHERE name = :1", entity['proficiency']['name'])
				print entity['proficiency']
				save_entity = ProficiencyTopic.get_or_insert(key_name=entity['name'], name = entity['name'], 
											   proficiency = this_proficiency.get())
			if data_type == 'content_pages':
				 try: this_proficiency = Proficiency.gql("WHERE name = :1", entity['proficiency']['name'])
				 except TypeError: continue # some old content pages dont have proficiencies
				 print entity['url']
				 save_entity = ContentPage(key_name=entity['url'], url = entity['url'], proficiency = this_proficiency.get()) 
			if data_type == 'raw_items':
				print entity['page']['url']
				this_url = ContentPage.gql("WHERE url = :1", entity['page']['url'])
				save_entity = RawQuizItem(
										  index = entity['index'],
										  answer_candidates = entity['answer_candidates'],
										  pre_content = entity['pre_content'],
										  content = entity['content'],
										  post_content = entity['post_content'],
										  page = this_url.get(),
										  moderated = False)
			if data_type == 'quiz_items': 
				qtm = quiztaker_methods()
				return qtm.refresh_quiz_items("loud")
			if data_type == 'employers':
				emp = employer_methods()
				return emp.load_data("employers", "")
			if data_type == 'mailing_list':
				from model.account import MailingList
				save_entity = MailingList(fullname = entity.get('fullname', ""), email = entity['email'], type = entity.get('type', ""))
			entities.append(save_entity)
		try:
			print "saving", str(entities)
			db.put(entities)
		except:
			logging.error('Unable to save new entities')
			print 'Unable to save raw quiz items'
			


  def dump_raw_items(self, list_of_items, *response):
      return encode(list_of_items)
 	


