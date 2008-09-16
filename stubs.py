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
            for item in items:            # Generate a bunch of items for each quiz_taker
                new_score = StubScore()
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
            query = db.GqlQuery("SELECT * FROM StubScore")
            scores = query.fetch(500)
            print "stored score stubs"
            for score in scores:
                print " QUIZ TAKER: " + score.quiz_taker + " QUIZ ITEM: " + score.quiz_item + " PICKED ANSWER: " + score.picked_answer +  " CORRECT ANSWER: " +score.correct_answer

            """

            Here is an opportunity to try out creating a graph of users and items. 
            Examples of the SQL-like syntax for selecting data are above.
            If you'd like to edit or view the models, they're in model.py.
            You may also want to reference views in views.py.
            
            Two simple initial goals:
            
             1. Add an integer property to the StubScore model called "rank". 
            The top-scoring stub user should be ranked 1, and down to the last user.
            
            
            2. Assign difficulty keys to quiz items.
            
            There is already a difficulty integer property for QuizItem, but it is empty.
            
            You could either use decimals 0-1, or rank similarly to users.
            Do whatever you think will be most useful!
            
            
            
            Important note - the stub data is created with a simple random() method, so the ranking/difficulty data won't be realistic. 
            Let's try to improve the stub creation process to more resemble a realistic score curve.
            
            
            """
            
            
