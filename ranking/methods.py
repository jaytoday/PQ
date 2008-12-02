import logging
# Log a message each time this module get loaded.
logging.info('Loading %s', __name__)
import cgi
from .model.user import QuizTaker, ProficiencyLevel, TopicLevel
from .model.quiz import ItemScore

class TopicLevelData():               
    def get(self, quiz_taker):
    	print quiz_taker.topic_levels

                                                            


    def set(self, quiz_taker):
		topic_scores = {}
		edited_scores = False
		for score in quiz_taker.scores:
			this_score = ItemScore.get(score)
			if not this_score:
				print "score not found. deleting key"
				edited_scores = True
				quiz_taker.scores.remove(score)  # remove key from list
			else:
				print this_score.score
			try: 
				current_average = topic_scores[this_score.quiz_item.topic.key()]['average']
				current_count = topic_scores[this_score.quiz_item.topic.key()]['count']
				current_sum = current_average * current_count
				new_sum = current_sum + this_score.score
				new_count = current_count + 1
				new_average = new_sum / new_count
			except:# no current average
				try: topic_scores[this_score.quiz_item.topic.key()] = {}
				except: continue # Reference Property error for old scores. 
				new_count = 1
				new_average = this_score.score
				
			topic_scores[this_score.quiz_item.topic.key()]['count'] = new_count
			topic_scores[this_score.quiz_item.topic.key()]['average'] = new_average
		print topic_scores
		if edited_scores: quiz_taker.put()		
		
		# seperate topic_scores into individual topics
		for topic_pair in topic_scores.items():
			print topic_pair[0]
			print quiz_taker
			tl_keyname = str(quiz_taker.unique_identifier) + "_" + str(topic_pair[0])
			if TopicLevel.get_by_key_name(tl_keyname):
				topic_level = TopicLevel.get_by_key_name(tl_keyname)
				topic_level.topic_level = topic_pair[1]['average']
			else:
			    topic_level = TopicLevel(key_name = tl_keyname,
										topic = topic_pair[0],
										quiz_taker = quiz_taker,
										topic_level = topic_pair[1]['average'])
			topic_level.put()
			
			 
			
		
			
		  
					

        	
class ProficiencyLevelData():               
    def get(self, quiz_taker):
    	print quiz_taker.proficiency_levels

                                                            


    def set(self, quiz_taker):
		pro_scores = {}
		for tl in quiz_taker.topic_levels.fetch(1000):
			try: 
				current_average = pro_scores[tl.topic.proficiency.key()]['average']
				current_count = pro_scores[tl.topic.proficiency.key()]['count']
				current_sum = current_average * current_count
				new_sum = current_sum + tl.topic_level
				new_count = current_count + 1
				new_average = new_sum / new_count
			except: # no current average
				pro_scores[tl.topic.proficiency.key()] = {}
				new_count = 1
				new_average = tl.topic_level
			pro_scores[tl.topic.proficiency.key()]['count'] = new_count
			pro_scores[tl.topic.proficiency.key()]['average'] = new_average

		print pro_scores
		for pro_pair in pro_scores.items():
				pl_keyname = str(quiz_taker.unique_identifier) + "_" + str(pro_pair[0])
				if ProficiencyLevel.get_by_key_name(pl_keyname):
					proficiency_level = ProficiencyLevel.get_by_key_name(pl_keyname)
					proficiency_level.proficiency_level = pro_pair[1]['average']
				else:
					 proficiency_level = ProficiencyLevel(key_name = pl_keyname,
															proficiency = pro_pair[0],
															quiz_taker = quiz_taker,
															proficiency_level = pro_pair[1]['average'])
				proficiency_level.put()
