import logging
import itertools
from utils.gql_encoder import GqlEncoder, encode
from google.appengine.ext import db
from .model.quiz import QuizItem, RawQuizItem, ProficiencyTopic, ContentPage, Proficiency
from .utils.utils import ROOT_PATH
from utils import simplejson
from employer.methods import DataMethods as emp_data
from google.appengine.api import images
from .model.user import ProfilePicture	
from .model.proficiency import SubjectImage
from model.employer import Employer
from model.account import MailingList
from google.appengine.api import memcache
from model.dev import Setting

DATA_TYPES = {"proficiencies": Proficiency.all(), 'proficiency_topics': ProficiencyTopic.all(), 'content_pages': ContentPage.all(), 'raw_items' : RawQuizItem.all(),
               'quiz_items': QuizItem.all(),
               'mailing_list': MailingList.all(), 'employers': Employer.all(), 'settings': Setting.all()}

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
    logging.info("deleted %s rows of %s entities" % ( str(deleted_count), data_type) )


def load_data(data_type):
    data = DataMethods()
    MIN_SLICE = memcache.get("MIN_SLICE_" + data_type)
    if MIN_SLICE == None:
    	MIN_SLICE = 0 
        data.special_processes(data_type)
        data.load_json(data_type, "")
    MAX_SLICE = MIN_SLICE + LOAD_INCREMENT
    data_load = data.load_data(data_type, MIN_SLICE, MAX_SLICE)
    if data_load == "Data Load Is Finished": 
        memcache.set("MIN_SLICE_" + data_type, None, 60000) # reset min-slice'
        return "Data Load Is Finished"
    else:
    	data.execute_load() 
        memcache.set("MIN_SLICE_" + data_type, MIN_SLICE + 10, 60000) # reset min-slice
        print str("Added Data Rows " + str(MIN_SLICE) + "-" + str(MAX_SLICE) + " For " + data_type + " Data")


# as of now, this results in print statements...not suitable for background processes.
def load_at_once(data_type):
    data = DataMethods()
    data.load_json(data_type, "")
    data_load = data.load_data(data_type)
    data.execute_load()


 
 
					
def refresh_subject_images(this_subject=False):
	#no argument refreshes all subject images. argument refresh a single subject.
	if this_subject: 
		import string 
		subject = Proficiency.get_by_key_name(string.capwords(this_subject))
		return build.refresh_subject_images(subject)
		
	data_type = "subject_images"
	proficiencies = memcache.get("subject_image_queue")
	if not proficiencies: proficiencies = Proficiency.all().fetch(1000)

	if proficiencies is None: 
	    return "No Proficiencies Found"
	    
	# Get the next proficiency in sequence 
	next_proficiency = proficiencies.pop()
	build = Build()
	data_load = build.refresh_subject_images(next_proficiency)
	memcache.set("subject_image_queue", proficiencies, 60000) # reset min-slice
	print len(proficiencies), " subjects left"	
	if len(proficiencies) == 0: 
	    memcache.set("subject_image_queue", None, 60000) # reset min-slice'
	    build.refresh_default_subject_image() # refresh default
	    print "Data Load Is Finished"
	    return "Data Load Is Finished"
	    		  	
	   


# Full Datastore Refresh -- Deprecated!
def restore_backup():
	build = Build()
	build.refresh_profile_images(refresh=True)
	build.destroy_everything()  # TODO: This wipes all user data!!!! 
	data = DataMethods()
	for query in DATA_TYPES.values():
		data.delete_data(query)
	data.execute_delete()
	for data_type in DATA_TYPES.keys():
		data.load_data(data_type, "/backup/") # Deprecated!!
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
		image_range = range(5) # change this as you add more. range() is always one int ahead.
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
		#print "saved %d new profile images" % len(save_images)
		logging.info("saved %d new profile images", len(save_images))

									
	def delete_default_profile_images(self): # delete images, since all profiles are being refreshed.
		pics =  ProfilePicture.all().fetch(1000)
		logging.info("deleting %d profiles images", len(pics))
		db.delete(pics)	

	def archive_default_profile_images(self): # image types are re-assigned, since deleting would cause a ReferenceError.
		pics = ProfilePicture.gql("WHERE type = :1", "pq").fetch(1000)
		logging.info("archiving %d profiles images", len(pics))
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
		all_images = []
		for p in proficiencies:
			p_path = ROOT_PATH + "/data/img/subject/" + str(p.name) + "/"
			save_images = []
			for n in range(4):
				try: image_file = open(p_path + str(n) + ".png")
				except: continue
				image = image_file.read()
				"""
				small_image = images.resize(image, 120, 80)
				large_image = images.resize(image, 360, 240)
				new_image = SubjectImage(key_name = str(p.name + "_" + str(n)), #unique keyname
				                         small_image = small_image,
				                         large_image = large_image,
				                         proficiency = p
									     )
				"""
				save_images.append(p.new_image(image))
				all_images.append(new_image)
			db.put(save_images)
			logging.info('refreshed %d subject images', len(save_images))
		return len(all_images)
					
		
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
		logging.info('saved default image: %s', default_image)
		return "saved default image: ", default_image							     
								


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
		json_file = open(ROOT_PATH + "/data/" + path + str(data_type) + ".json")
		json_str = json_file.read()
		json_data = simplejson.loads(json_str) # Load JSON file as object
		memcache.set("json_" + str(data_type), json_data, 60000)
		
		
		entities = []
		# Setup, Imports
		if data_type == 'employers': emp = emp_data()


    
    
  def load_data(self, data_type, MIN_SLICE = None, MAX_SLICE = None):
		logging.info('loading data type %s from %s to %s' % (data_type, str(MIN_SLICE), str(MAX_SLICE)))


		entities = []
		# Setup, Imports
		if data_type == 'employers': emp = emp_data()

		newdata = memcache.get("json_" + str(data_type))
		if len(newdata[MIN_SLICE:MAX_SLICE]) == 0: 
		                           return "Data Load Is Finished"
		for entity in newdata[MIN_SLICE:MAX_SLICE]: # Could this be more efficient? 
			
			if data_type == 'proficiencies':
				this_entity = Proficiency.get_by_key_name(entity['name'])
				if this_entity: save_entity = this_entity #if this exists, modify it
				else: save_entity = Proficiency(key_name=entity['name'], name = entity['name'])
				save_entity.name = entity['name']
				save_entity.status = entity.get("status", "")
				save_entity.link_html = entity.get("link_html", "")
				save_entity.video_html = entity.get("video_html", "") 
				save_entity.status = entity.get('status', None)
				save_entity.blurb = entity.get('blurb', None)
				save_entity.popularity = entity.get("popularity", 50) 
				save_entity.difficulty = entity.get("difficulty", 50)

			if data_type == 'proficiency_topics':
				this_proficiency = Proficiency.get_by_key_name(entity['proficiency']['name'])
				if not this_proficiency: 
				         print "proficiency ", entity['proficiency']['name'], " not found when inserting topic ", entity['name']
				         logging.error('proficiency %s not found for topic %s' % (entity['proficiency']['name'],  entity['name']))
				         continue
				this_entity = ProficiencyTopic.get_by_key_name(entity['proficiency']['name'] + str('_') + entity['name'])
				if this_entity: save_entity = this_entity #if this exists, modify it
				else: save_entity = ProficiencyTopic(key_name=entity['proficiency']['name'] + str('_') + entity['name'], name = entity['name'])
				save_entity.name = entity['name']
				save_entity.proficiency = this_proficiency
											   
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
				this_topic = ProficiencyTopic.get_by_key_name(entity['proficiency']['name'] + str('_') + entity['topic']['name'])
				if not this_topic: 
				    print "proficiency topic ", entity['topic']['name'], " not found when inserting quiz item"
				    logging.error('proficiency topic %s not found for quiz item', entity['topic']['name'])
				    continue

				import string
				if entity['index'].lower() not in [ a.lower() for a in entity['answers'] ]: logging.error('Quiz Item Index %s not in answers %s' % ( entity['index'], str(entity['answers'])))
				    
				save_entity = QuizItem( content = entity['content'],
									 theme = entity['theme'],
									 proficiency = this_proficiency.key(),
									 answers = [  ".".join( [ string.capwords(l) for l in a.split(".") ] ) for a in entity['answers']   ],
									 index = entity['index'],
									 topic = this_topic.key())
				if entity['content_url']: save_entity.content_url = entity['content_url']   
			if data_type == 'employers': 
				save_entity = False # employers.methods used to save 
				for e in emp.create_business_account(entity['unique_identifier'], entity.get('email', None), entity['proficiencies'], batch=True):
						entities.append(e)
						
			if data_type == 'mailing_list':
				save_entity = MailingList(key_name=entity['email'], fullname = entity.get('fullname', ""), email = entity['email'], type = entity.get('type', ""))
			
			if data_type == 'settings':
				save_entity = Setting(key_name=entity['name'], name = entity['name'], value = entity['value'])
		
			if save_entity: entities.append(save_entity)
		try:
			entity_num = 0
			self.load_entities[data_type] = entities
			for entity in entities: entity_num += 1
			logging.info('finished preparing data load for %d %s' % (len(entities), data_type))
			return len(entities)
		except:
			logging.error('Unable to save %s at number %d' % (data_type, entity_num))
			return False






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
     for i in itertools.chain(*[list[1] for list in self.load_entities.items()]): load_list.append(i) #inefficient
     db.put(load_list)
     #db.put(itertools.chain(*[list[1] for list in self.load_entities.items()])) # this doesn't work
     
     for list in self.load_entities.items():
     	self.special_processes(list[0])
     	logging.info('executed load for %s', list[0])
     self.load_entities = {}


  def dump_raw_items(self, list_of_items, *response):
      return encode(list_of_items)
 	



  def special_processes(self, data_type):
     if data_type == 'employers': 
       emp = emp_data()
       emp.refresh_employer_images()



def restore_settings(self):
  	from model.dev import Setting
  	save = []
  	s = Setting(key_name="excellence_proficiency_threshold", name="excellence_proficiency_threshold", value=float(.10))
  	save.append(s)
  	s = Setting(key_name="fluency_proficiency_threshold", name="fluency_proficiency_threshold", value=float(.55))
  	save.append(s) 	
  	s = Setting(key_name="excellence_topic_threshold",name="excellence_topic_threshold", value=float(90))
  	save.append(s)	
  	s = Setting(key_name="fluency_topic_threshold", name="fluency_topic_threshold", value=float(55))
  	save.append(s)
  	db.put(save)
