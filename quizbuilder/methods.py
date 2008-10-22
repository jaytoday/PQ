from utils.gql_encoder import GqlEncoder, encode
from .model.quiz import QuizItem, RawQuizItem, ProficiencyTopic, ContentPage, Proficiency
from .utils.utils import tpl_path, ROOT_PATH, raise_error
import simplejson
#import views
import induction




def dump_data(self, gql_query):
	try:
		objects = gql_query.fetch(1000)
		return encode(objects)
		#for object in objects:
	except:
		return "unable to encode objects"
		

def load_data(data_type, verbose):
    data = DataMethods()
    return data.load_data(data_type)


def refresh_data(data_type, verbose):
    data = DataMethods()
    query = {"proficiencies": Proficiency.all(), 'proficiency_topics': ProficiencyTopic.all(), 'content_pages': ContentPage.all(), 'raw_items' : RawQuizItem.all()}
    data.delete_data(query[data_type])
    return data.load_data(data_type)



class DataMethods():

  def delete_data(self, query):
     print ""
     entities = query.fetch(1000)
     for entity in entities:
     	print "DELETED"
     	print entity.__dict__
     	entity.delete()

    
  def load_data(self, data_type):
		print data_type
		print ""
		json_file = open(ROOT_PATH + "/data/" + str(data_type) + ".json")
		json_str = json_file.read()
		newdata = simplejson.loads(json_str) # Load JSON file as object
		for entity in newdata:
			if data_type == 'proficiencies':
				save_entity = Proficiency.get_or_insert(entity['name'], name = entity['name']) 
			if data_type == 'proficiency_topics':
				this_proficiency = Proficiency.gql("WHERE name = :1", entity['proficiency'])
				print entity['proficiency']
				save_entity = ProficiencyTopic.get_or_insert(entity['name'], name = entity['name'], 
											   proficiency = this_proficiency.get())
			if data_type == 'content_pages':
				 this_proficiency = Proficiency.gql("WHERE name = :1", entity['proficiency']['name'])
				 print entity['url']
				 
				 save_entity = ContentPage(url = entity['url'], proficiency = this_proficiency.get()) 
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

			try: save_entity.put()	
			except:
				logging.error('Unable to save new entity')
				print 'Unable to save raw quiz item'
			print "ADDED"
			print save_entity.__dict__ 	
			print save_entity.key()   



  def dump_raw_items(self, list_of_items, *response):
      return encode(list_of_items)
 	




