import logging
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
  data.load_data(data_type, verbose) 
     

def load_data(data_type, verbose):
  data = DataMethods()
  data.load_data(data_type, verbose) 
       
 
def dump_data(gql_query):
	objects = gql_query.fetch(1000)
	response = []
	try: return encode(objects)
	except: logging.debug('unable to encode objects')
	#return encode(object)
 

def new_topic(topic_name, proficiency_name): 
	this_proficiency = Proficiency.gql("WHERE name = :1", proficiency_name)
	new_topic = ProficiencyTopic(name=topic_name, proficiency=this_proficiency.get().key())
	new_topic.put()
	return new_topic.key()


     
     
     
class DataMethods():
	
  def delete_data(self, data_type, *verbose):
		query = ""
		if data_type == "quiz_items": query = db.GqlQuery("SELECT * FROM QuizItem")
		if data_type == "item_scores": query = db.GqlQuery("SELECT * FROM ItemScore")
		if not query: return False	
		objects = query.fetch(1000)
		for object in objects:
			if verbose[0] == "loud":
				print ""
				print "deleted: " + str(object.__dict__) 
			object.delete()
		return True
			

				
		
  def refresh_quiz_items(self, verbose):
	quiz_items= []		
	json_file = open(ROOT_PATH + "/data/quiz_items.json")
	json_str = json_file.read()
	newdata = simplejson.loads(json_str) # Load JSON file as object
	# Retrieve Proficiency. If new, then save it.
	for item in newdata:
		this_proficiency = Proficiency.gql("WHERE name = :proficiency",
									   proficiency=item['proficiency']['name']).get()
		if not this_proficiency:
			this_proficiency = Proficiency(name=item['proficiency']['name'])
			this_proficiency.put()
			if verbose[0] == "loud":
				print ""
				print "added proficiency: " + str(this_proficiency.name)
				
		this_topic = ProficiencyTopic.gql("WHERE name = :topic" ,
									   topic=item['topic']['name']).get()
		if not this_topic:
			print ""
			print item['topic']['name']
			this_topic = ProficiencyTopic(name=item['topic']['name'], proficiency=this_proficiency.key())
			this_topic.put()
			if verbose[0] == "loud":
				print ""
				print "added topic: " + str(this_topic.name)
	# Store Item in Datastore
		quiz_item = QuizItem(
							 content = item['content'],
							 theme = item['theme'],
							 proficiency = this_proficiency.key(),
							 answers = item['answers'],
							 index = item['index'],
							 topic = this_topic.key())
							  #Add List of Answers
		print quiz_item.__dict__
		quiz_items.append(quiz_item)
		if verbose[0] == "loud":
		  print encode(quiz_item)
	db.put(quiz_items) 




  def refresh_scores(self, verbose):
		scores = []		
		json_file = open(ROOT_PATH + "/data/item_scores.json")
		json_str = json_file.read()
		newdata = simplejson.loads(json_str) # Load JSON file as object
		# Retrieve Proficiency. If new, then save it.
		for item in newdata:
			# Store Item in Datastore
			if item['type'] == 'trash': continue
			if item['type'] == 'temp': continue
			this_taker = QuizTaker.get(item['quiz_taker']['key'])
			this_vendor = Employer.get(item['vendor']['key'])
			this_item = QuizItem.get(item['quiz_item']['key'])
			score = ItemScore(
								 quiz_taker = this_taker,
								 picked_answer = item['picked_answer'],
								 correct_answer = item['correct_answer'],
								 score = item['score'],
								 quiz_item = this_item,
								 vendor = this_vendor,
								 type = item['type'])
								  #Add List of Answers
			scores.append(score)
			if verbose[0] == "loud":
			  print encode(score)
		db.put(scores) # save scores 	   
							




  
			
  def load_data(self, data_type, *verbose):
		# Load External JSON fixture
		if data_type == "quiz_items": return self.refresh_quiz_items(verbose)
		if data_type == "item_scores": return self.refresh_scores(verbose)
		
		# refresh all?
