import logging
import random
from utils import *
from model import *

class CreateScoreStubs(webapp.RequestHandler):
 # Creates Fake Scores. May Take A While to Run At High Volume
    score_amount = 20

    def get(self):
        import string
        query = db.GqlQuery("SELECT * FROM QuizItem")
        items = query.fetch(1000)
        total_scores = str(self.score_amount * len(items))
        print "creating " + total_scores + " scores"
        for i in range(self.score_amount):
            quiz_taker = random.sample('ABCDEFGHIJKLMNOPQRSTUVWXYZ',5)  # sample characters
            random.shuffle(quiz_taker) # shuffle characters
            quiz_taker = string.join(quiz_taker) # turn list into string - we have a stub user!
            for item in items:     # TODO: Use list comprehensions         # Generate a bunch of items for each quiz_taker
                new_score = StubItemScore()
                new_score.quiz_taker = quiz_taker
                new_score.quiz_item = item.slug 
                picked_answer = random.sample(item.answers, 1)  # Random. Try to map closer to realistic scores.
                new_score.picked_answer = picked_answer[0]
                new_score.correct_answer = item.index
                if new_score.picked_answer == new_score.correct_answer:
                    new_score.score = 1
                else:
                    new_score.score = 0
                new_score.put()
                print " QUIZ TAKER: " + new_score.quiz_taker + " QUIZ ITEM: " + new_score.quiz_item + " PICKED ANSWER: " + new_score.picked_answer +  " CORRECT ANSWER: " +new_score.correct_answer

            
            

class ViewScoreStubs(webapp.RequestHandler):            

    def get(self):
            query = db.GqlQuery("SELECT * FROM StubItemScore")
            scores = query.fetch(500)
            query = db.GqlQuery("SELECT * FROM QuizItem")
            items = query.fetch(1000)
            
            print "ITEM RANKINGS -- the lower the rank, the more difficult the item"
            for item in items:             # TODO: Use list comprehensions
                item.difficulty = 0
                for score in scores:
                    if (score.quiz_item == item.slug) and (score.score == 1):#For each correct score per item
                        item.difficulty += 1
                            
                            
                print ""
                print str(item.slug) + " is ranked " + str(item.difficulty)   #Load /view_scores/ to see printed difficulty keys
                item.put()     # Save difficulty keys to datastore       
                        



class GetProficiencyLevelForItemScore(webapp.RequestHandler):             # localhost:8080/set_difficulties/   

    def get(self):
        
        query = db.GqlQuery("SELECT * FROM ItemScore") # Add conditions to only get certain types of scores.
        itemscores = query.fetch(1000)
        for item_score in itemscores:
            this_quiz_taker = item_score.quiz_taker
            """
             We don't know the proficiency from the score, so
             we need to look up the QuizItem entry for this quiz item
            """
            get_quiz_item  = db.GqlQuery("SELECT * FROM QuizItem WHERE slug = :slug",
                                          slug=item_score.quiz_item)
            this_quiz_item = get_quiz_item.fetch(1)
            this_proficiency = this_quiz_item.proficiency
            """
            We have a proficiency -- this_proficiency
            and we have the quiz taker -- this_quiz_taker
            
            Now we need the ProficiencyLevel for this quiz taker, and
            this proficiency

            """            
            get_proficiency_level = db.GqlQuery("SELECT * FROM ProficiencyLevel WHERE proficiency = :proficiency AND quiz_taker = :quiz_taker",
                                        proficiency=this_proficiency, quiz_taker = this_quiz_taker)
            this_proficiency_level = get_proficiency_level.fetch(1)
            
            proficiency_value = this_proficiency_level.proficiency_level
                                                            

                
                
class Set_Difficulties(webapp.RequestHandler):             # localhost:8080/set_difficulties/   

    def get(self):
        
        
            query = db.GqlQuery("SELECT * FROM QuizItem")
            items = query.fetch(1000)

            for item in items:
                item.difficulty = random.randint(1,1000)  # Difficulty is random number from 1-1000
                item.put() # Wow, Writing to the Datastore is so easy!
                list_index = items.index(item) # Get the index of the item in the list -- [0], [1], etc.
                this_difficulty = items[list_index].difficulty   
                print str(this_difficulty) + " is equal to " + str(item.difficulty)  # These values should be the same


                                    
            
            
            
                        
class Set_Proficiencies(webapp.RequestHandler):         # localhost:8080/set_proficiencies/   

    def get(self):
            query = db.GqlQuery("SELECT * FROM StubItemScore")
            scores = query.fetch(3)     # Keep This Number Low, For Testing
            query = db.GqlQuery("SELECT * FROM Proficiency")
            proficiencies = query.fetch(10)
            quiz_takers = []
            for score in scores:
                quiz_takers.append(score.quiz_taker)
            quiz_takers = set(quiz_takers)       # We now have a list of every quiz taker
            for quiz_taker in quiz_takers:
                for proficiency in proficiencies:
                    proficiency_level = ProficiencyLevel()
                    proficiency_level.quiz_taker = quiz_taker
                    proficiency_level.proficiency = proficiency.proficiency
                    proficiency_level.proficiency_level = 0
                    # Now We Have To Decide the Proficiency Level.
                    user_scores = StubItemScore.gql("WHERE quiz_taker = :quiz_taker",
                                                    quiz_taker=quiz_taker)
                    for score in user_scores:
                          this_item = QuizItem.gql("WHERE slug = :slug",
                                                  slug=score.quiz_item)
                          for item in this_item:
                              if item.proficiency == proficiency.proficiency:
                                  item_proficiency_level = score.score * this_item[0].difficulty  # Each Item's Proficiency Is difficulty x score.
                                  proficiency_level.proficiency_level += item_proficiency_level   # Add Together Item Proficiency Scores
                    proficiency_level.put()
                    print ""
                    print "New Proficiency Level -- User: " + str(proficiency_level.quiz_taker) + " for Proficiency: " + str(proficiency_level.proficiency) + " With Proficiency Level: " + str(proficiency_level.proficiency_level)
