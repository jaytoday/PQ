from __init__ import *

import logging
import random
from utils import *
from model import *
from BeautifulSoup import BeautifulSoup, BeautifulStoneSoup, SoupStrainer  # HTML Parsing Library


# This program calculate the degrees of difficulty and degree of proficiency as well as the consistencies of the quiz items and the quiz takers.
# Note: Difficulty, Proficiency are normalized to range from 0 to range_max = 10,000
# Fuzzy logic is used ranging from 0 to range_max. 0 = false range_max = true. intermediate values are allowed.



class test(controller):

    def index(self,test_arg=None):
        self.echo ('your argument is: ' + str(test_arg))


    def test_function(self,test_arg=None):
        self.echo ('your other argument is: ' + str(test_arg))

    def test_tilde(self,test_arg=None):
        webpage = urlfetch.fetch("http://tilde.jamslevy.user.dev.freebaseapps.com/?format=xml")
        page = BeautifulSoup(webpage.content)
        print webpage.content

