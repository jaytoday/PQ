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
from google.appengine.api import memcache

DATA_TYPES = {"proficiencies": Proficiency.all(), 'proficiency_topics': ProficiencyTopic.all(), 'content_pages': ContentPage.all(), 'raw_items' : RawQuizItem.all(),
               'quiz_items': QuizItem.all(),
               'mailing_list': MailingList.all(), 'employers': Employer.all()}

LOAD_INCREMENT = 10 # How many entities are loaded into datastore at a time
IMAGE_INCREMENT = 1 # How many entities are loaded into datastore at a time

#Refresh One Data Type
def refresh_data(data_type):
    data = DataMethods()
    data.delete_data(DATA_TYPES.get(data_type, False))
    data.load_data(data_type, "")
    data.special_processes(data_type)
    data.execute_load()


def delete_data(data_type):
    data = DataMethods()
    data.delete_data(DATA_TYPES.get(data_type, False))
    deleted_count = data.execute_delete()
    return str("deleted " + str(deleted_count) + " rows of " + data_type)


def load_data(data_type):
    data = DataMethods()
    MIN_SLICE = memcache.get("MIN_SLICE_" + data_type)
    if MIN_SLICE == None:
    	MIN_SLICE = 0 
        data.special_processes(data_type)
        data.load_json(data_type, "")
    MAX_SLICE = MIN_SLICE + LOAD_INCREMENT
    data_load = data.load_data(data_type, MIN_SLICE, MAX_SLICE)
    if data_load == "Finished": 
        memcache.set("MIN_SLICE_" + data_type, None, 60000) # reset min-slice'
        return "Finished"
    elif data_load > 0:
    	data.execute_load() 
        memcache.set("MIN_SLICE_" + data_type, MIN_SLICE + 10, 60000) # reset min-slice
        print str("Added Data Rows " + str(MIN_SLICE) + "-" + str(MAX_SLICE) + " For " + data_type + " Data")

 
 
					
def refresh_subject_images(this_subject=False):
	#no argument refreshes all subject images. argument refresh a single subject.
	if this_subject: 
		import string 
		subject = Proficiency.get_by_key_name(string.capwords(this_subject))
		return build.refresh_subject_images(subject)
		
	data_type = "subject_images"
	proficiencies = memcache.get("subject_image_queue")
	if not proficiencies: proficiencies = Proficiency.all().fetch(1000)

	# Get the next proficiency in sequence 
	next_proficiency = proficiencies.pop()
	build = Build()
	data_load = build.refresh_subject_images(next_proficiency)
	memcache.set("subject_image_queue", proficiencies, 60000) # reset min-slice
	print "Added ", data_load, " Subject Images for Proficiency ", next_proficiency.name
	print len(proficiencies), " subjects left"	
	if len(proficiencies) == 0: 
	    memcache.set("subject_image_queue", None, 60000) # reset min-slice'
	    build.refresh_default_subject_image() # refresh default
	    print "Data Load Is Finished"
	    return		  	
	   


# Full Datastore Refresh
def restore_backup():
	build = Build()
	build.refresh_profile_images(refresh=True)
	build.destroy_everything()  # TODO: This wipes all user data!!!! 
	data = DataMethods()
	for query in DATA_TYPES.values():
		data.delete_data(query)
	data.execute_delete()
	for data_type in DATA_TYPES.keys():
		data.load_data(data_type, "/backup/")
		data.special_processes(data_type)
		data.execute_load()
	build.refresh_subject_images()



    
    
    

# Display data in JSON format, for backups
def dump_data(data_type):
	try:
		query = DATA_TYPES[data_type]
		objects = query.fetch(1000)
		return encode(objects)
	except:
		return "unable to encode objects"
		


    

class Build():

	def refresh_profile_images(self, refresh=False):
		if refresh: self.delete_default_profile_images() 
		else: self.archive_default_profile_images() 
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

									
	def delete_default_profile_images(self): # delete images, since all profiles are being refreshed.
		pics =  ProfilePicture.all().fetch(1000)
		logging.info("deleting %d profiles images", pics)
		db.delete(pics)	

	def archive_default_profile_images(self): # image types are re-assigned, since deleting would cause a ReferenceError.
		pics = ProfilePicture.gql("WHERE type = :1", "pq").fetch(1000)
		logging.info("archiving %d profiles images", pics)
		for p in pics: p.type = "pq_old"
		db.put(pics)
		
			    	
   	    	
   	    	
   	    			  		
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
			return len(save_images)
					
		
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
								


	def destroy_everything(self):
		 from model.user import QuizTaker, ProficiencyLevel, TopicLevel
		 from model.account import Profile, Account, Award, Sponsorship, SponsorPledge
		 from model.employer import AutoPledge
		 from model.quiz import ItemScore
		 account_classes = [ItemScore, QuizTaker, ProficiencyLevel, TopicLevel, Profile, Account, Award, Sponsorship, SponsorPledge, AutoPledge]
		 destroy_list = []
		 for c in account_classes:
			for entity in c.all().fetch(1000): destroy_list.append(entity)
		 db.delete(destroy_list)
		 print "destroyed ", len(destroy_list), " account entries"
		 logging.info('deleted %d account entries', len(destroy_list))  	 
					

   	    	
   	    	
   	    		
	
class DataMethods():

  def __init__(self):
	  self.delete_entities = {}
	  self.load_entities = {}
	  
  
  
  def delete_data(self, query):
     logging.info('preparing delete for %s', query)
     entities = query.fetch(1000) # variable?
     self.delete_entities[query]= entities



    
  def load_json(self, data_type, path):
		logging.info('loading json for data type %s', data_type)
		print ""
		print 'loading JSON data type: ', data_type
		print ""
		json_file = open(ROOT_PATH + "/data/" + path + str(data_type) + ".json")
		json_str = json_file.read()
		json_data = simplejson.loads(json_str) # Load JSON file as object
		memcache.set("json_" + str(data_type), json_data, 60000)
		
		
		entities = []
		# Setup, Imports
		if data_type == 'employers': emp = emp_data()


    
    
  def load_data(self, data_type, MIN_SLICE = None, MAX_SLICE = None):
		logging.info('loading data type %s from %s to %s' % (data_type, str(MIN_SLICE), str(MAX_SLICE)))
		print ""
		print 'loading data type: ', data_type, " from ", MIN_SLICE, " to ", MAX_SLICE
		print ""


		entities = []
		# Setup, Imports
		if data_type == 'employers': emp = emp_data()

		newdata = memcache.get("json_" + str(data_type))
		
		if len(newdata[MIN_SLICE:MAX_SLICE]) == 0: 
		                           print "Data Load Is Finished"
		                           return "Finished"
		for entity in newdata[MIN_SLICE:MAX_SLICE]: # Could this be more efficient? 
			
			if data_type == 'proficiencies':
				save_entity = Proficiency.get_or_insert(key_name=entity['name'], name = entity['name'], 
				status = entity.get("status", ""), link_html = entity.get("link_html", ""), 
				video_html = entity.get("video_html", ""), blurb = entity.get("blurb", ""), 
				popularity = entity.get("popularity", 50), difficulty = entity.get("difficulty", 50),
				status = entity.get('status', None), blurb = entity.get('blurb', None))
				# temporary upgrades
				save_entity.popularity = entity.get("popularity", 50) 
				save_entity.difficulty = entity.get("difficulty", 50)

			if data_type == 'proficiency_topics':
				this_proficiency = Proficiency.get_by_key_name(entity['proficiency']['name'])
				if not this_proficiency: 
				         print "proficiency ", entity['proficiency']['name'], " not found when inserting topic ", entity['name']
				         logging.error('proficiency %s not found for topic %s' % (entity['proficiency']['name'],  entity['name']))
				         continue
				save_entity = ProficiencyTopic.get_or_insert(key_name=entity['name'], name = entity['name'], proficiency = this_proficiency)
											   
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
				if not this_proficiency: 
				    print "proficiency ", entity['proficiency']['name'], " not found when inserting quiz item"
				    logging.error('proficiency %s not found for quiz item', entity['proficiency']['name'])
				    continue 
				this_topic = ProficiencyTopic.get_by_key_name(entity['topic']['name'])
				if not this_topic: 
				    print "proficiency topic ", entity['topic']['name'], " not found when inserting quiz item"
				    logging.error('proficiency topic %s not found for quiz item', entity['topic']['name'])
				    continue 
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
			return len(entities)
		except:
			logging.error('Unable to save %s at number %d' % (data_type, entity_num))
			print 'Unable to save', data_type, "at number ", entity_num






  def execute_delete(self):
     delete_list = []
     for i in itertools.chain(*[list[1] for list in self.delete_entities.items()]): delete_list.append(i)     
     db.delete(delete_list) # inefficient! why wont itertools work....
     #db.delete(itertools.chain(*[list[1] for list in self.delete_entities.items()]))
     for list in self.delete_entities.items():
     	logging.info('deleted %d rows of %s' % (len(list[1]), list[0]._model_class) )
     self.delete_entities = {}
     return len(list[1])
     	
     	
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
