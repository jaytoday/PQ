import logging
import random
import string
import re
from google.appengine.api import urlfetch
import cgi
import wsgiref.handlers
import os
import datetime, time
from model import *
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
 
from google.appengine.ext.webapp import util
import simplejson

# Relevency Tally for Semantic Tags
from collections import defaultdict
import operator 


from .utils.utils import tpl_path
from .lib.BeautifulSoup import BeautifulSoup, BeautifulStoneSoup, SoupStrainer  # HTML Parsing Library
from .lib import rdfxml

from rpc import *

# class for semantic analysis - semanticproxy, class for parsing. 
SEMANTICPROXY_URL = "http://service.semanticproxy.com/processurl/aq9r8pmcbztd4s7s427uw7zg/rdf/" # USE RDF ENDPOINT
SEMANTICPROXY_MICRO_URL = "http://service.semanticproxy.com/processurl/aq9r8pmcbztd4s7s427uw7zg/microformat/" 
TILDE_BASE_URL = "http://tilde.jamslevy.user.dev.freebaseapps.com/"
TILDE_TYPE_LIMIT = 7 # Maximum number of types to query per request topic.
TILDE_TOPIC_LIMIT = 4 # Maximum number of topics per type to list in response. 
TRUNCATE_URL = "http://pqstage.appspot.com/truncate_page/?url=" 

DEFAULT_PAGES = [#"http://en.wikipedia.org/wiki/Inference", 
                 "http://en.wikipedia.org/wiki/Renewable_energy",
                 ]

AC_LIMIT = 21 # Limit of answer choice candidates per quiz item
AC_MIN = 8 # Minimum of answer choices required. 

QUIZBUILDER_PATH = 'quizbuilder/'


class RawItemInduction(webapp.RequestHandler):  
 
    def get(self, *args):  
        topic = self.save_topic(args[0][1],args[0][2])
        page = self.save_url(args[0][0], topic)
        build_items = BuildItemsFromPage()
        raw_quiz_items = build_items.get(page)
        for item in raw_quiz_items:
            print item['raw_content'][0].__class__
            print item['raw_content'][1].__class__
            print item['raw_content'][2].__class__

            self.save_item(item)
        #self.response.out.write(template.render(path, template_values))
            

    def save_url(self, page, this_topic):
        saved_page = ContentPage.gql("WHERE url = :1", page).get()
        if saved_page: # check value
            return saved_page
        else:
            new_page = ContentPage(url = page, topic = this_topic )
            new_page.put()
            return new_page

    def save_topic(self, topic, proficiency):
        saved_topic = ProficiencyTopic.gql("WHERE name = :1", topic).get()
        if saved_topic: # check value
            return saved_topic
        else:
            this_proficiency = Proficiency.gql("WHERE name = :1", proficiency).get()
            print this_proficiency
            new_topic = ProficiencyTopic(name = topic, proficiency = this_proficiency)
            new_topic.put()
            return new_topic
                             
    def save_item(self, item):
        try:
            this_pre_content = db.Text(item['raw_content'][0])
            this_content = db.Text(item['raw_content'][1])
            this_post_content = db.Text(item['raw_content'][2])
        except UnicodeDecodeError:
            print "ruh roh"
            print str(item['raw_content'][1])

            return
        new_raw_item = RawQuizItem(page = item['page'],
                                    answer_candidates = item['similar_topics'],
                                    index = item['correct_answer'],
                                    pre_content = this_pre_content,
                                    content = this_content,
                                    post_content = this_post_content,
                                    moderated = False)
        print new_raw_item.__dict__
        return
        
        if saved_topic: # check value
            return saved_topic
        else:
            this_proficiency = Proficiency.gql("WHERE name = :1", proficiency).get()
            print this_proficiency
            new_topic = ProficiencyTopic(name = topic, proficiency = this_proficiency)
            new_topic.put()
            return new_topic
                                   
                  
class QuizBuilder(webapp.RequestHandler):

    def get(self):

        raw_quiz_items = self.load_raw_items()
        template_values = {}    
        template_values["raw_quiz_items"] = raw_quiz_items
        path = tpl_path(QUIZBUILDER_PATH + 'quizbuilder.html')
        #self.response.out.write(template.render(path, template_values))


    def load_raw_items(self):
        topic_items = []
        all_items = RawQuizItem.all().get()
        if self.request.get('topic'): 
            for item in all_items:
                if item.url.topic.name == self.request.get('topic'):
                    topic_items.append(item)
                else: continue
            return topic_items
        else: return all_items


            
            

            



class BuildItemsFromPage():
    
  def get(self, page):

        raw_quiz_items = []
        
        #in case we need to meet 100k limit, truncate page.
        

        soup_url = SEMANTICPROXY_URL +  page.url    # + TRUNCATE URL + 
        # timeout for fetch_page (and all fetch pages)
        fetch_page = urlfetch.fetch(soup_url)              # perform semantic analysis
        soup = BeautifulSoup(fetch_page.content) #whole page
        tags = self.get_tags(soup.findAll('c:exact'))
                # rank tags by relevency
        for tag in tags: # Slice [1:...]
        
        # CHECK IF TAG IS A TYPED TOPIC ON FREEBASE 
            # Make sure that get_similar_topics and get_paragraphs_containing_tag are successful.
            similar_topics = self.get_similar_topics(tag)
            if similar_topics: # not just if it exists, but if there's a list.
                raw_content_groups = self.get_raw_content_groups(soup.findAll('c:document'), tag)
                for raw_content in raw_content_groups:
                     #If len(get_similar_topics(tag)) < 1, add synonym tags or related tags in Answer Candidate 
                    raw_quiz_item = {"similar_topics" : similar_topics, "raw_content": raw_content, "correct_answer": tag, "page": page }
                    raw_quiz_items.append(raw_quiz_item)
            continue 

        return raw_quiz_items
  
  def get_tags(self, doc_tags): 
  # for a page, get a relevency-ranked list of topics found in the text. 
    tags = []
    for tag in doc_tags:
        #print tag.contents[0]
        tags.append(str(tag.contents[0]))
    tags = self.rank_tags(tags)
    return tags  
    
  def rank_tags(self, l):
    # tag ranking helper function
    # take a list of tags ['tag1', 'tag2', 'tag2', tag3'....]
    # sort set of tags by order of frequency
    tally = defaultdict(int)
    for x in l:
        tally[x] += 1
    sorted_tags = sorted(tally.items(), key=operator.itemgetter(1))
    tags = []
    for tag in sorted_tags:
        tags.append(tag[0]) 
    tags.reverse()
    return tags
          
          
  def get_similar_topics(self, tag):
    # Freebase request to get similar topics for a tag.
    tag = tag.replace(' ','%20') #urlencode tag
    tilde_request = str(TILDE_BASE_URL) + "?format=xml&topic_limit=" + str(TILDE_TOPIC_LIMIT) + "&type_limit=" + str(TILDE_TYPE_LIMIT) + "&request=" + str(tag)
    try:
        tilde_response = urlfetch.fetch(tilde_request)
    except:
        logging.debug('Unable to fetch tilde response') 
    tilde_soup = BeautifulStoneSoup(tilde_response.content)
    similar_topics = [topic.contents[0] for topic in tilde_soup.findAll('title')][1:AC_LIMIT]
    if len(similar_topics) >= AC_MIN:
        return similar_topics
    else:
        return False 
        
  def get_raw_content_groups(self, page_text,tag):
    # find paragraph in text containing a tag. 

    raw_content_groups = []
    # THIS NEEDS WORK. 
    for p in page_text[0].contents:
        psoup = BeautifulSoup(p)
        for paragraph in psoup.findAll('p'):
            if paragraph.find(text=re.compile(tag)):  # Is tag in this paragraph? 
                the_paragraph = self.highlightAnswer(paragraph, tag)
                
                # GET NEXT AND PREV <P> ELEMENTS CONTAINING SIGNIFICANT CONTENT. 
                if (paragraph.findPreviousSibling('p') == None):
                    previous_paragraph = ""
                else:
                    previous_paragraph = paragraph.findPreviousSibling('p')
                if (paragraph.findNextSibling('p') == None):
                    next_paragraph = ""
                else:
                    next_paragraph = paragraph.findNextSibling('p')
                paragraph_containing_tag = (str(previous_paragraph.contents[0]), str(the_paragraph), str(next_paragraph.contents[0]))
                raw_content_groups.append(paragraph_containing_tag)#return paragraph_containing_tag # this only returns the first instance.
            else:
                continue  # tag not found in paragraph
        return raw_content_groups
                
     
                
  def highlightAnswer(self, text, tag):
    # apply HTML markup to answer within quiz item content
     text = str(text)
     str_tag = str(tag)
     return text.replace(str_tag, '<span class="answer_span">%s</span>' % str_tag)               
                 
  def truncate_page(self, url):
    # Truncate page to meet OpenCalais 100k limit.
    fetch_page = urlfetch.fetch(soup_url)   
    soup = BeautifulSoup(fetch_page.content) # necessary?
    
    # truncate HTML document. 
    




        


class InductionInterface(webapp.RequestHandler):

    def get(self):
        template_values = {}
        path = tpl_path(QUIZBUILDER_PATH + 'induction.html')
        self.response.out.write(template.render(path, template_values))
        


    














