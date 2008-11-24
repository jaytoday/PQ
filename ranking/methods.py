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
		for score in quiz_taker.scores:
			this_score = ItemScore.get(score)
			print this_score.score
			try: 
				current_value = topic_scores[this_score.quiz_item.topic.key()]['value']
				current_sum = topic_scores[this_score.quiz_item.topic.key()]['sum']
				current_product = current_value * current_sum
				new_product = current_product + this_score.score
				new_sum = current_sum + 1
				new_value = new_product / new_sum
			except:# no current value
				topic_scores[this_score.quiz_item.topic.key()] = {}
				new_sum = 1
				new_value = this_score.score
				
			topic_scores[this_score.quiz_item.topic.key()]['sum'] = new_sum
			topic_scores[this_score.quiz_item.topic.key()]['value'] = new_value
			
		print topic_scores
		# seperate topic_scores into individual topics
		for topic_pair in topic_scores.items():
			print topic_pair[0]
			print quiz_taker
			tl_keyname = str(quiz_taker.unique_identifier) + "_" + str(topic_pair[0])
			if TopicLevel.get_by_key_name(tl_keyname):
				topic_level = TopicLevel.get_by_key_name(tl_keyname)
				topic_level.topic_level = topic_pair[1]['value']
			else:
			    topic_level = TopicLevel(key_name = tl_keyname,
										topic = topic_pair[0],
										quiz_taker = quiz_taker,
										topic_level = topic_pair[1]['value'])
			topic_level.put()
			
			 
			
		
			
		  
					

        	
class ProficiencyLevelData():               
    def get(self, quiz_taker):
    	print quiz_taker.proficiency_levels

                                                            


    def set(self, quiz_taker):
		pro_scores = {}
		for tl in quiz_taker.topic_levels.fetch(1000):
			try: 
				current_value = pro_scores[tl.topic.proficiency.key()]['value']
				current_sum = pro_scores[tl.topic.proficiency.key()]['sum']
				current_product = current_value * current_sum
				new_product = current_product + tl.topic_level
				new_sum = current_sum + 1
				new_value = new_product / new_sum
			except: # no current value
				pro_scores[tl.topic.proficiency.key()] = {}
				new_sum = 1
				new_value = tl.topic_level
			pro_scores[tl.topic.proficiency.key()]['sum'] = new_sum
			pro_scores[tl.topic.proficiency.key()]['value'] = new_value

		print pro_scores
		for pro_pair in pro_scores.items():
				pl_keyname = str(quiz_taker.unique_identifier) + "_" + str(pro_pair[0])
				if ProficiencyLevel.get_by_key_name(pl_keyname):
					proficiency_level = ProficiencyLevel.get_by_key_name(pl_keyname)
					proficiency_level.proficiency_level = pro_pair[1]['value']
				else:
					 proficiency_level = ProficiencyLevel(key_name = pl_keyname,
															proficiency = pro_pair[0],
															quiz_taker = quiz_taker,
															proficiency_level = pro_pair[1]['value'])
				proficiency_level.put()
