import logging
import random
import string
import re
from google.appengine.api import urlfetch
import cgi
import wsgiref.handlers
import os
import datetime, time
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
#RPC - place in utils 
from google.appengine.ext.webapp import util
import simplejson


from .utils.utils import tpl_path
from model import *
from .lib.BeautifulSoup import BeautifulSoup, BeautifulStoneSoup, SoupStrainer  # HTML Parsing Library


# class for semantic analysis - semanticproxy, class for parsing. 
semanticproxy_rdf_url = "http://service.semanticproxy.com/processurl/aq9r8pmcbztd4s7s427uw7zg/rdf/" # USE RDF ENDPOINT
semanticproxy_url = "http://service.semanticproxy.com/processurl/aq9r8pmcbztd4s7s427uw7zg/microformat/" # USE RDF ENDPOINT
tilde_base_url = "http://tilde.jamslevy.user.dev.freebaseapps.com/"

DEFAULT_PAGES = ["http://en.wikipedia.org/wiki/Inference", 
                 "http://en.wikipedia.org/wiki/Renewable_energy",
                 ]

class QuizBuilder(webapp.RequestHandler):

    def get(self):
        raw_quiz_items = []
        pages = self.resolve_urls()
        for page in pages:
            contentpage = ContentPage(url = page)
            contentpage.put()
            raw_quiz_item = self.build_rdf_item(contentpage)
            save_item(raw_quiz_item)
            raw_quiz_items.append(raw_quiz_item)
        template_values = {}    
        template_values["raw_quiz_items"] = raw_quiz_items
        path = tpl_path('quizbuilder.html')
        #self.response.out.write(template.render(path, template_values))


    def build_rdf_item(self, page):
        raw_quiz_items = []
        soup_url = semanticproxy_url + page.url
        fetch_page = urlfetch.fetch(soup_url)              # perform semantic analysis
        soup = BeautifulSoup(fetch_page.content) #whole page
        tags = [tag.contents[0] for tag in soup.findAll(rel="tag")]
        paragraphs = soup.findAll('p')
        for tag in tags:    # CHANGE THIS VALUE FROM 1:3

            # Make sure that get_similar_topics and get_paragraphs_containing_tag are successful.
            tag_paragraphs = get_paragraphs_containing_tag(paragraphs, tag)
            if tag_paragraphs:
                
                 #If len(get_similar_topics(tag)) < 1, add synonym tags or related tags in Answer Candidate 
                raw_quiz_item = {"similar_topics" : get_similar_topics(tag), "raw_content": tag_paragraphs, "correct_answer": tag, "page": page }
                return raw_quiz_item
            else:
                continue #throw error
        return "unable to build item"
        
        
    def build_item(self, url):
        raw_quiz_items = []
        soup_url = semanticproxy_url + url.name
        page = urlfetch.fetch(soup_url)              # perform semantic analysis
        soup = BeautifulSoup(page.content) #whole page
        tags = [tag.contents[0] for tag in soup.findAll(rel="tag")]
        paragraphs = soup.findAll('p')
        for tag in tags:    # CHANGE THIS VALUE FROM 1:3

            # Make sure that get_similar_topics and get_paragraphs_containing_tag are successful.
            tag_paragraphs = get_paragraphs_containing_tag(paragraphs, tag)
            if tag_paragraphs:
                 #If len(get_similar_topics(tag)) < 1, add synonym tags or related tags in Answer Candidate 
                raw_quiz_item = {"answer_choices" : get_similar_topics(tag), "raw_content": tag_paragraphs, "correct_answer": tag, "url": url }
                return raw_quiz_item
            else:
                continue #throw error
        return "unable to build item"
    



            
                                    
                        
    def resolve_urls(self):
        if self.request.get('url'): 
            urls = self.request.get('url')
        else:
            urls = DEFAULT_PAGES
        return urls


    def ds_method(self):
         q = db.GqlQuery("SELECT * FROM RawItem")
         results = q.fetch(1000)
         for result in results:
             pass # FOR NOW                   
         raw_quiz_items = list(db.GqlQuery(
         'SELECT * FROM RawItem'))
         for item in raw_quiz_items:
             item.raw_content = (item.previous_paragraph, item.the_paragraph, item.next_paragraph)
         return raw_quiz_items            
        
        
    def save_item(self, raw_quiz_item):
            for topic in raw_quiz_item['similar_topics']:
                topic = str(topic)
            item_similar_topics = [str(item) for item in raw_quiz_item['similar_topics']]
            raw_item = RawQuizItem(similar_topics = item_similar_topics,
            previous_paragraph = raw_quiz_item['raw_content'][0], 
            the_paragraph = raw_quiz_item['raw_content'][1], 
            next_paragraph = raw_quiz_item['raw_content'][2], 
            correct_answer = str(raw_quiz_item['correct_answer']),
            url = url )
            raw_item.put()
            
            

        
class RDF(dict):
  def __init__(self, url):
    try:
      soup_url = semanticproxy_url + url 
      page = urlfetch.fetch(soup_url)
      soup = BeautifulSoup(page.content) #whole page
      #print soup.contents[2]
      for item in soup.contents[2]:
          print item.attrs
    except:
      self['contents'] = ''
  def links(self):
    [ item['rdf:Description'] for item in self['contents'].findAll('item') ]
  def exact(self):
      #print contents
      for item in contents.findAll('item'):
          print item
      
      self['exact'] = [ item['c:exact'] for item in self['contents'].findAll('item') ] 
          


def get_similar_topics(tag):
    tag = tag.replace(' ','%20') #urlencode tag
    tilde_request = tilde_base_url + "?format=xml&request=" + tag
    tilde_response = urlfetch.fetch(tilde_request)
    if tilde_response.content: 
        pass
    else:
        tilde_request = str(tilde_base_url + "?format=xml&request=neuroscience")
        tilde_response = urlfetch.fetch(tilde_request)
        
    tilde_soup = BeautifulStoneSoup(tilde_response.content)
    similar_topics = [topic.contents[0] for topic in tilde_soup.findAll('title')][1:11]
    return similar_topics


def get_paragraphs_containing_tag(paragraphs,tag):
    for paragraph in paragraphs:
        if paragraph.find(text=re.compile(tag)):
            if (paragraph.find('ps')):  #Don't Include Paragraphs with children paragraphs
                continue
            else:
                the_paragraph = highlightAnswer(paragraph, tag)
                if (paragraph.findPreviousSibling('p') == None):
                    previous_paragraph = ""
                else:
                    previous_paragraph = paragraph.findPreviousSibling('p')
                if (paragraph.findNextSibling('p') == None):
                    next_paragraph = ""
                else:
                    next_paragraph = paragraph.findNextSibling('p')                
                paragraphs_containing_tag = (previous_paragraph, the_paragraph, next_paragraph)
                return paragraphs_containing_tag
                 


def highlightAnswer(text, tag):
     text = str(text)
     str_tag = str(tag)
     return text.replace(str_tag, '<span class="answer_span">%s</span>' % str_tag)



