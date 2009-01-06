import logging
import random
import string
import re
from google.appengine.api import urlfetch
import cgi
import wsgiref.handlers
import os
import datetime, time
from .model.quiz import ContentPage,  RawQuizItem
from .model.proficiency import Proficiency, ProficiencyTopic
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp

from google.appengine.ext.webapp import util


# Relevency Tally for Semantic Tags
from collections import defaultdict
import operator 


from utils.BeautifulSoup import BeautifulSoup, BeautifulStoneSoup, SoupStrainer  # HTML Parsing Library
from utils import rdfxml



# class for semantic analysis - semanticproxy, class for parsing. 
SEMANTICPROXY_URL = "http://service.semanticproxy.com/processurl/aq9r8pmcbztd4s7s427uw7zg/rdf/" # USE RDF ENDPOINT
SEMANTICPROXY_MICRO_URL = "http://service.semanticproxy.com/processurl/aq9r8pmcbztd4s7s427uw7zg/microformat/" 
TILDE_BASE_URL = "http://tilde.jamslevy.user.dev.freebaseapps.com/"
TILDE_TYPE_LIMIT = 50 # Maximum number of types to query per request topic.
TILDE_TOPIC_LIMIT = 20 # Maximum number of topics per type to list in response. 
TILDE_EXCLUDE = 'music,film' # should be array
TRUNCATE_URL = "http://pqstage.appspot.com/truncate_page/?url=" 

DEFAULT_PAGES = [#"http://en.wikipedia.org/wiki/Inference", 
                 "http://en.wikipedia.org/wiki/Renewable_energy",
                 ]

AC_LIMIT = 100 # Limit of answer choice candidates per quiz item
AC_MIN = 5 # Minimum of answer choices required.

RAW_ITEMS_PER_PAGE = 15 # Limit of quiz items created per page 

MIN_TAG_CHARS = 4 # Minimum characters per tag

RAW_ITEMS_PER_TAG = 5 # Limit of quiz items created per tag.




class RawItemInduction(webapp.RequestHandler):  
 
    def get(self, *args):
		try: urlfetch.fetch(args[0][0]) #check for valid url
		except: return ["error", "invalid url"]    
		proficiency = self.save_proficiency(args[0][1])
		page = self.save_url(args[0][0], proficiency)  
		build_items = BuildItemsFromPage()
		raw_quiz_items = build_items.get(page)
		if raw_quiz_items[0] == "error": return ["error", raw_quiz_items[1]]
		saved_items = []
		for item in raw_quiz_items:
			save_item = self.save_item(item)
			if save_item:
				saved_items.append(save_item)
			else: 
				logging.error("unable to save item: ") 
				logging.error(str(item))
			continue     
		return saved_items 

       
                
        #self.response.out.write(template.render(path, template_values))
            

    def save_url(self, page, this_proficiency):
        saved_page = ContentPage.gql("WHERE url = :1", page)
        if saved_page.get(): # check value
            return saved_page.get()
        else:
            new_page = ContentPage(url = page, proficiency = this_proficiency.key() ) # make sure page is urlencoded.
            new_page.put()
            return new_page

    def save_proficiency(self, proficiency):
        this_proficiency = Proficiency.get_or_insert(proficiency, name=proficiency)
        if not this_proficiency.is_saved: this_proficiency.put()
        return this_proficiency

            
                             
    def save_item(self, item):
        try: # encode text
            this_pre_content = db.Text(item['raw_content'][0], encoding='utf-8')
            this_content = db.Text(item['raw_content'][1], encoding='utf-8')
            this_post_content = db.Text(item['raw_content'][2], encoding='utf-8')
        except:
            this_pre_content = db.Text(item['raw_content'][1])
            print "Unable to decode item content"
            logging.error('Unable to decode item content')
            return False
        try:
            new_raw_item = RawQuizItem(page = item['page'],
                                    answer_candidates = item['similar_topics'],
                                    index = item['correct_answer'],
                                    pre_content = this_pre_content,
                                    content = this_content,
                                    post_content = this_post_content,
                                    moderated = False)
            new_raw_item.put()
            return new_raw_item 
        except:
             
            #new_raw_item.put()
            print 'Unable to save raw quiz item' 
            logging.error(item)
            logging.error('Unable to save raw quiz item')
            return False
           


            



class BuildItemsFromPage():
    
  def get(self, page):
        raw_quiz_items = []
        tag_threshold = 0
        soup = self.get_soup(page)
        if not soup.findAll('c:document'): return ["error", "unable to read the soup"]
        tags = self.get_tags(soup)
        if not tags: return ["error", "SemanticProxy unable to find tags"]
        for tag in tags: 
            if tag_threshold >= RAW_ITEMS_PER_PAGE: continue

            
            similar_topics = self.get_similar_topics(tag)
            if similar_topics: # not just if it exists, but if there's a list.
               tag_threshold += 1
               raw_content_groups = self.get_raw_content_groups(soup.findAll('c:document'), tag)
               for raw_content in raw_content_groups:
                     #If len(get_similar_topics(tag)) < 1, add synonym tags or related tags in Answer Candidate
                    raw_quiz_item = {"similar_topics" : similar_topics, "raw_content": raw_content, "correct_answer": tag, "page": page }
                    raw_quiz_items.append(raw_quiz_item)
                    continue 

        if len(raw_quiz_items) == 0: return ["error", str({"tag_threshold": tag_threshold, "tags": tags})]
        return raw_quiz_items


  def get_soup(self, page):
	#in case we need to meet 100k limit, truncate page.
	soup_url = SEMANTICPROXY_URL +  str(page.url)    # + TRUNCATE URL + 
	# timeout for fetch_page (and all fetch pages)
	fetch_page = urlfetch.fetch(soup_url)              # perform semantic analysis
	soup = BeautifulSoup(fetch_page.content) #whole page
	try: # look for error
		exception = soup.findAll('exception')[0].contents[0]
		print exception
		return False
	except: return soup 
	
	  
  def get_tags(self, soup):
	page_tags = soup.findAll('c:exact')
	if len(page_tags) == 0: return False 
	tags = [] # for a page, get a relevency-ranked list of topics found in the text. 
	for tag in page_tags:
		# escape "" or ' ' 
		if 'http://' in tag: continue
		if len(tag.contents[0]) >= MIN_TAG_CHARS: tags.append(str(tag.contents[0]))
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
    tilde_request = str(TILDE_BASE_URL) + "?format=xml&topic_limit=" + str(TILDE_TOPIC_LIMIT) + "&type_limit=" + str(TILDE_TYPE_LIMIT) + "&exclude=" + str(TILDE_EXCLUDE) + "&request=" + str(tag)
    try:
        tilde_response = urlfetch.fetch(tilde_request)
    except:
        logging.debug('Unable to fetch tilde response')
        return False 
    tilde_soup = BeautifulStoneSoup(tilde_response.content)
    similar_topics = []
    for topic in tilde_soup.findAll('title'):
    	try: encoded_topic = unicode(topic.contents[0]).encode('utf-8')
    	except: continue
    	try: encoded_topic.decode('ascii')
    	except: continue
        if len(encoded_topic) < len(tag) + 10: similar_topics.append(encoded_topic)
    similar_topics = self.rank_tags(similar_topics)
    if len(similar_topics) >= AC_MIN:
        return similar_topics[1:AC_LIMIT]
    else:
        return False 
        
  def get_raw_content_groups(self, page_text,tag):
	# find paragraph in text containing a tag.    
	# todo: Templates for mediawiki and google knol
	raw_content_groups = []
	w = re.compile(tag)
	if not page_text: return False
	sentences = str(page_text[0].contents).split(".")
	for this_sentence in sentences:
		#main_sentence = sentence.find(text=re.compile(r'\W%s\W' % tag ))
		if tag in this_sentence:  # Is tag in this sentence? 
			# previous two sentences
			prev_two_sentences = ""
			prev_two = [sentences.index(this_sentence) - 1, sentences.index(this_sentence) - 2]
			for s in prev_two:
				try: prev_two_sentences = prev_two_sentences + str(sentences[s]) + "."
				except: pass
			# next two sentences
			next_two_sentences = ""
			next_two = [sentences.index(this_sentence) + 1, sentences.index(this_sentence) + 2]
			for s in next_two:
				try: next_two_sentences = next_two_sentences + str(sentences[s]) + "."
				except: pass
			paragraphs = (str(prev_two_sentences), str(this_sentence + "."), str(next_two_sentences))
			clean_paragraphs = []
			for p in paragraphs:
				p = p.replace('\\n', '')
				p = p.replace("\\'", "'")
				footnote = re.compile( '\[.*\]' )
				p = footnote.sub('', p)				
				p = unicode(p).encode('utf-8')
				p = self.highlightAnswer(p, tag)
				clean_paragraphs.append(p) 
				raw_content_groups.append(clean_paragraphs)#return paragraph_containing_tag # this only returns the first instance.
		else:
			continue  # tag not found in paragraph
	return raw_content_groups[0:RAW_ITEMS_PER_TAG]  # This slice could also be a threshold, or randomized, to avoid bias to the top of the document. 
			
 
                
  def highlightAnswer(self, text, tag):
    # apply HTML markup to answer within quiz item content
     text = str(text)
     str_tag = str(tag)
     tag_word = re.compile(r'\W%s\W' % tag, re.IGNORECASE)
     return tag_word.sub('<span id="blank">%s</span>' % tag, text)
     #return tag_word.sub('^b%sb$' % tag, text)                
                 
                 



  def truncate_page(self, url):
    # Truncate page to meet OpenCalais 100k limit.
    fetch_page = urlfetch.fetch(soup_url)   
    soup = BeautifulSoup(fetch_page.content) # necessary?
    
    # truncate HTML document. 
    












           
class Drilldown(webapp.RequestHandler):

    def get(self):
        template_values = {}
        path = tpl_path('drilldown.html')
        self.response.out.write(template.render(path, template_values))
        
            
