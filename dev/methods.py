import logging
import itertools
from utils.gql_encoder import GqlEncoder, encode
from google.appengine.ext import db
from .model.quiz import QuizItem, RawQuizItem, ProficiencyTopic, ContentPage, Proficiency
from .utils.utils import tpl_path, ROOT_PATH
from utils import simplejson
from employer.methods import DataMethods as emp_data
from google.appengine.api import images
from .model.user import ProfilePicture	
from .model.proficiency import SubjectImage
from model.employer import Employer
from model.account import MailingList


DATA_TYPES = {"proficiencies": Proficiency.all(), 'proficiency_topics': ProficiencyTopic.all(), 
              'content_pages': ContentPage.all(), 'raw_items' : RawQuizItem.all(), 'quiz_items': QuizItem.all(),
               'mailing_list': MailingList.all(), 'employers': Employer.all()}


#Refresh One Data Type
def refresh_data(data_type, verbose):
    data = DataMethods()
    data.delete_data(DATA_TYPES.get(data_type, False))
    data.execute_delete()
    data.load_data(data_type, "")
    data.special_processes(data_type)
    data.execute_load()

# Full Datastore Refresh
def restore_backup():
	build = Build()
	build.refresh_profile_images(refresh=True)
	data = DataMethods()
	destroy_everything()  # TODO: This wipes all user data!!!! 
	for query in DATA_TYPES.values():
		data.delete_data(query)
	data.execute_delete()
	for data_type in DATA_TYPES.keys():
		data.load_data(data_type, "/backup/")
		data.special_processes(data_type)
		data.execute_load()
	build.refresh_subject_images()




def dump_data(data_type):
	try:
		query = DATA_TYPES[data_type]
		objects = query.fetch(1000)
		return encode(objects)
	except:
		return "unable to encode objects"
		

def load_data(data_type, verbose):
    logging.info('loading data for %s', data_type)
    data = DataMethods()
    return data.load_data(data_type, "")



#TODO: This should go in Build 
def destroy_everything():
  	 from model.user import QuizTaker, ProficiencyLevel, TopicLevel
  	 from model.account import Profile, Account, Award, Sponsorship
  	 account_classes = [QuizTaker, ProficiencyLevel, TopicLevel, Profile, Account, Award, Sponsorship]
  	 destroy_list = []
  	 for c in account_classes:
  	 	for entity in c.all().fetch(1000): destroy_list.append(entity)
  	 db.delete(destroy_list)
  	 print "destroyed ", len(destroy_list), " account entries"
  	 logging.info('deleted %d account entries', len(destroy_list))  	 
  	 
  	 
    

class Build():

	def refresh_profile_images(self, refresh=False):
		self.delete_profile_images(refresh)
		image_range = range(3) # change this as you add more. range() is always one int ahead.
		save_images = []
		for i in image_range:
			image_file = open(ROOT_PATH + "/data/img/profile/profile_" + str(i) + ".png")
			image = image_file.read()
			small_image = images.resize(image, 45, 45)
			large_image = images.resize(image, 95, 95)
			new_image = ProfilePicture(small_image = small_image,
									   large_image = large_image,
									   type="pq")
			save_images.append(new_image)
		db.put(save_images)
		print "saved %d new profile images" % len(save_images)
		logging.info("saved %d new profile images", len(save_images))

									
	def delete_profile_images(self, refresh=False):
		if refresh: pics =  ProfilePicture.all().fetch(1000)
		else: pics = ProfilePicture.gql("WHERE type = :1", "pq").fetch(1000)
		print "deleting profiles images:", pics
		db.delete(pics)	

		  		
	def refresh_subject_images(self, this_proficiency=False):
		if not this_proficiency: 
		    proficiencies = Proficiency.all().fetch(1000)
		    self.delete_subject_images()
		    self.refresh_default_subject_image()
		else: 
		    proficiencies = [this_proficiency]
		    self.delete_subject_images(subject=this_proficiency)
		for p in proficiencies:
			p_path = ROOT_PATH + "/data/img/subject/" + str(p.name) + "/"
			save_images = []
			for n in range(3):
				try: image_file = open(p_path + str(n) + ".png")
				except: continue
				image = image_file.read()
				small_image = images.resize(image, 120, 80)
				large_image = images.resize(image, 360, 240)
				new_image = SubjectImage(key_name = str(p.name + "_" + str(n)), #unique keyname
				                         small_image = small_image,
				                         large_image = large_image,
				                         proficiency = p
									     )
				save_images.append(new_image)
			db.put(save_images)
			logging.info('refreshed %d subject images', len(save_images))
					
		
	def delete_subject_images(self, subject=False):
		if not subject: pics = SubjectImage.all().fetch(1000)
		else: pics = SubjectImage.gql("WHERE proficiency = :1", subject).fetch(1000)
		print "deleting %d subject images" % len(pics)
		logging.info("deleting %d subject images", len(pics))
		db.delete(pics)
				
				

		
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
		logging.info('saved default image: %s', default_image)
		print "saved default image: ", default_image							     
								
			
				
   	    		
	
class DataMethods():

  def __init__(self):
	  self.delete_entities = {}
	  self.load_entities = {}
  
  
  def delete_data(self, query):
     logging.info('preparing delete for %s', query)
     entities = query.fetch(1000) # variable?
     self.delete_entities[query]= entities


    
    
  def load_data(self, data_type, path):
		logging.info('loading data type %s', data_type)
		print ""
		print 'loading data type: ', data_type
		print ""
		json_file = open(ROOT_PATH + "/data/" + path + str(data_type) + ".json")
		json_str = json_file.read()
		newdata = simplejson.loads(json_str) # Load JSON file as object
		entities = []
		# Setup, Imports
		if data_type == 'employers': emp = emp_data()
		for entity in newdata: # Could this be more efficient? 
			
			if data_type == 'proficiencies':
				save_entity = Proficiency.get_or_insert(key_name=entity['name'], name = entity['name'], status = entity.get("status", ""), blurb = entity.get("blurb", ""))
				save_entity.status = entity.get('status', None)

				save_entity.blurb = entity.get('blurb', None)
				
			if data_type == 'proficiency_topics':
				this_proficiency = Proficiency.get_by_key_name(entity['proficiency']['name'])
				save_entity = ProficiencyTopic.get_or_insert(key_name=entity['name'], name = entity['name'], 
											   proficiency = this_proficiency)
											   
			if data_type == 'content_pages':
				 this_proficiency = Proficiency.get_by_key_name(entity['proficiency']['name'])
				 save_entity = ContentPage(key_name=entity['url'], url = entity['url'], proficiency = this_proficiency) 
				 
			if data_type == 'raw_items':
				this_url = ContentPage.get_by_key_name(entity['page']['url'])
				save_entity = RawQuizItem(#key_name?
										  index = entity['index'],
										  answer_candidates = entity['answer_candidates'],
										  pre_content = entity['pre_content'],
										  content = entity['content'],
										  post_content = entity['post_content'],
										  page = this_url,
										  moderated = False)

			if data_type == 'quiz_items': 
				this_proficiency = Proficiency.get_by_key_name(entity['proficiency']['name'])
				if not this_proficiency: logging.error('proficiency %s not found for quiz item', entity['proficiency']['name']) 
				this_topic = ProficiencyTopic.get_by_key_name(entity['topic']['name'])
				if not this_topic: logging.error('proficiency %s not found for quiz item', entity['proficiency']['name']) 
				save_entity = QuizItem( content = entity['content'],
									 theme = entity['theme'],
									 proficiency = this_proficiency.key(),
									 answers = entity['answers'],
									 index = entity['index'],
									 topic = this_topic.key())

				
			if data_type == 'employers': 
				for e in emp.create_business_account(entity['unique_identifier'], entity['proficiencies'], batch=True):
					entities.append(e)
					save_entity = False
			if data_type == 'mailing_list':
				save_entity = MailingList(key_name=entity['email'], fullname = entity.get('fullname', ""), email = entity['email'], type = entity.get('type', ""))
			if save_entity: entities.append(save_entity)

		try:
			entity_num = 0
			self.load_entities[data_type] = entities
			for entity in entities: entity_num += 1
			logging.info('finished preparing data load for %d %s' % (len(entities), data_type))
			print 'finished preparing data load for' , len(entities), data_type
		except:
			logging.error('Unable to save %s at number %d' % (data_type, entity_num))
			print 'Unable to save', data_type, "at number ", entity_num






  def execute_delete(self):
     delete_list = []
     for i in itertools.chain(*[list[1] for list in self.delete_entities.items()]): delete_list.append(i)     
     db.delete(delete_list) # inefficient! why wont itertools work....
     #db.delete(itertools.chain(*[list[1] for list in self.delete_entities.items()]))
     for list in self.delete_entities.items():
     	logging.info('executed delete for %s', list[0]._model_class)
     	print "DELETED ", len(list[1]), " rows of ", list[0]._model_class
     self.delete_entities = {}
     	
     	
  def execute_load(self):
     load_list = []
     for i in itertools.chain(*[list[1] for list in self.load_entities.items()]): load_list.append(i)
     db.put(load_list)
     #db.put(itertools.chain(*[list[1] for list in self.load_entities.items()])) # still a list of lists  
     self.special_processes(list[0])
     for list in self.load_entities.items():
     	logging.info('executed load for %s', list[0])
     	print "executed load for ", len(list[1]), " rows of ", list[0]
     self.load_entities = {}


  def dump_raw_items(self, list_of_items, *response):
      return encode(list_of_items)
 	



  def special_processes(self, data_type):
     if data_type == 'employers': 
       emp = emp_data()
       emp.refresh_employer_images()
