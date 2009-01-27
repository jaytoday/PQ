import logging
import cgi
from .model.user import QuizTaker, ProficiencyLevel, TopicLevel
from .model.quiz import ItemScore
#from decimal import Decimal, ROUND_HALF_UP


# TODO: Much better documentation/logging!!

class TopicLevelData():               
    def get(self, quiz_taker):
    	print quiz_taker.topic_levels

                                                            


    def set(self, quiz_taker):
		topic_scores = {}
		edited_scores = False
		for score in quiz_taker.itemscores:
			this_score = ItemScore.get(score.key())
			if not this_score:
				logging.error("score not found. deleting key")
				edited_scores = True
				quiz_taker.scores.remove(score)  # remove key from list
			else:
				pass
			# TODO: could this be rewritten with .get()?
			try: 
				
				current_average = topic_scores[this_score.quiz_item.topic.key()]['average']
				current_count = topic_scores[this_score.quiz_item.topic.key()]['count']
				current_sum = current_average * current_count
				new_sum = current_sum + this_score.score
				new_count = current_count + 1
				new_average = new_sum / new_count

#				new_average = Decimal(new_sum) / Decimal(new_count)                This would only be necessary for division
#				new_average = new_average.quantize(Decimal("0.001"), ROUND_HALF_UP)
			except:# no current average
				try: topic_scores[this_score.quiz_item.topic.key()] = {}
				except: continue # Reference Property error for old scores. 
				new_count = 1
				new_average = this_score.score
				
			topic_scores[this_score.quiz_item.topic.key()]['count'] = new_count
			topic_scores[this_score.quiz_item.topic.key()]['average'] = new_average
			logging.info('new average: %d', new_average)
		if edited_scores: quiz_taker.put()		
		
		# seperate topic_scores into individual topics
		print topic_scores.items()
		for topic_pair in topic_scores.items():
			tl_keyname = str(quiz_taker.unique_identifier) + "_" + str(topic_pair[0])
			topic_pair[1]['average'] = int(topic_pair[1]['average']) 
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

		for pro_pair in pro_scores.items():
				pl_keyname = str(quiz_taker.unique_identifier) + "_" + str(pro_pair[0])
				pro_pair[1]['average'] = int(pro_pair[1]['average'])
				if ProficiencyLevel.get_by_key_name(pl_keyname):
					proficiency_level = ProficiencyLevel.get_by_key_name(pl_keyname)
					proficiency_level.proficiency_level = pro_pair[1]['average']
				else:
					 proficiency_level = ProficiencyLevel(key_name = pl_keyname,
															proficiency = pro_pair[0],
															quiz_taker = quiz_taker,
															proficiency_level = pro_pair[1]['average'])
				proficiency_level.put()
