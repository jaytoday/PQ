from model.quiz import QuizItem, ItemScore
from model.user import QuizTaker
from .model.proficiency import Proficiency, ProficiencyTopic 
from .utils.utils import tpl_path, ROOT_PATH, raise_error
import simplejson
from google.appengine.ext import db
from utils.gql_encoder import GqlEncoder, encode
    

def refresh_data(data_type, verbose):
  data = DataMethods()
  data.delete_data(data_type, verbose) 
  data.refresh_data(data_type, verbose) 
     

def load_data(data_type, verbose):
  data = DataMethods()
  data.refresh_data(data_type, verbose) 
       
 
def dump_data(gql_query):
  try:
	objects = gql_query.fetch(1000)
	for object in objects:
		if object.kind() != "QuizItem": continue
	return encode(objects)
  except:
	return "unable to encode objects"     

def new_topic(topic_name, proficiency_name): 
	this_proficiency = Proficiency.gql("WHERE name = :1", proficiency_name)
	new_topic = ProficiencyTopic(name=topic_name, proficiency=this_proficiency.get().key())
	new_topic.put()
	return new_topic.key()


     
     
     
class DataMethods():
	
  def delete_data(self, data_type, *verbose):
		query = ""
		if data_type == "quiz_items": query = db.GqlQuery("SELECT * FROM QuizItem")
		if not query: return False	
		objects = query.fetch(1000)
		for object in objects:
			if verbose[0] == "loud":
				print ""
				print "deleted: " + str(object.__dict__) 
			object.delete()
		return True
			
			
  def refresh_data(self, data_type, *verbose):
		# Load External JSON fixture
		if data_type == "quiz_items": return self.refresh_quiz_items(verbose)
		
		# refresh all?
				
		
  def refresh_quiz_items(self, verbose):
	proficiencies = []		
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
		quiz_item.put()
		if verbose[0] == "loud":
		  print encode(quiz_item) 




  						

