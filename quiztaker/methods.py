from model.quiz import Proficiency, ProficiencyTopic, QuizTaker, QuizItem, ItemScore 
from .utils.utils import tpl_path, ROOT_PATH, raise_error
import simplejson
from utils.gql_encoder import GqlEncoder, encode
    

def refresh_data(query, verbose):
  data = DataMethods()
  data.delete_data(query, verbose) 
  data.refresh_data("quiz_items", verbose) 
     
     
 
def dump_data(gql_query):
  objects = gql_query.fetch(1000)
  try:
	objects = gql_query.fetch(1000)
	return encode(objects)
	#for object in objects:
  except:
	return "unable to encode objects"     

 
 
     
     
class DataMethods():


  def delete_data(self, query, *verbose):
		objects = query.fetch(1000)
		for object in objects:
			if verbose[0] == "loud":
				print ""
				print "deleted: " + str(object.__dict__) 
			object.delete()
			
			
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
	for item in newdata["quiz_items"]:
		this_proficiency = Proficiency.gql("WHERE name = :proficiency",
									   proficiency=item['proficiency']).get()
		if not this_proficiency:
			this_proficiency = Proficiency(name=item['proficiency'])
			this_proficiency.put()
			if verbose[0] == "loud":
				print ""
				print "added proficiency: " + str(this_proficiency.name)
	# Store Item in Datastore
		
		quiz_item = QuizItem(slug = item['slug'],
							 category = item['content'][0],
							 content = item['content'][1],
							 proficiency = this_proficiency.key(),
							 answers = item['answers'],
							 index = item['index'] )
	   
							  #Add List of Answers
		quiz_item.put()
		if verbose[0] == "loud":
			print ""
			print "added quiz item: " + str(quiz_item.slug) + " + " + str(quiz_item.proficiency.name)




  						

