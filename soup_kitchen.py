import logging
import random
import string
import re
from utils import *
from model import *
from BeautifulSoup import BeautifulSoup, BeautifulStoneSoup, SoupStrainer  # HTML Parsing Library


# class for semantic analysis - semanticproxy, class for parsing. 

semanticproxy_url = "http://service.semanticproxy.com/processurl/aq9r8pmcbztd4s7s427uw7zg/microformat/"
tilde_base_url = "http://tilde.jamslevy.user.dev.freebaseapps.com/"

class Soup(webapp.RequestHandler):

    def get(self):
        raw_quiz_items = []
        semanticproxy_url = "http://service.semanticproxy.com/processurl/aq9r8pmcbztd4s7s427uw7zg/microformat/"
        url = "http://oreilly.com/pub/a/oreilly/frank/rossum_1099.html"
        soup_url = semanticproxy_url + url 
        page = urlfetch.fetch(soup_url)
        soup = BeautifulSoup(page.content)  #whole page
        tags = [tag.contents[0] for tag in soup.findAll(rel="tag")]
        paragraphs = soup.findAll('p')
        for tag in tags:
            if (tag !="Java") : continue
            raw_quiz_item = {"similar_topics" : get_similar_topics(tag), "paragraphs_containing_tag": get_paragraphs_containing_tag(paragraphs, tag), "correct_answer": tag }
            raw_quiz_items.append(raw_quiz_item)
           
        
        template_values = {}    
        template_values["raw_quiz_items"] = raw_quiz_items
        path = tpl_path('create_quiz.html')
        self.response.out.write(template.render(path, template_values))

            
            
            
        """            
        for tag in tags:
            
            for paragraph in paragraphs:
                
                if paragraph.find(text=re.compile(tag)):
                    print ""
                    if (paragraph.find('p')):  #Don't Include Paragraphs with children paragraphs
                        continue
                    else:
                        next_paragraph = paragraph.findNextSibling('p')
                        previous_paragraph = paragraph.findPreviousSibling('p')
                        print previous_paragraph
                        print str.upper(str(paragraph))
                        print next_paragraph
                        
                        # Add <b> tag to first instance of tag found in paragraph
                        
                    
                    print tag
                    print ""
                    
            
            
            
        # Find passage containing tag, and print it.     
        """
          
                        
                        

class TildeClient(webapp.RequestHandler):

    def get(self):
        print
        url = "http://oreilly.com/pub/a/oreilly/frank/rossum_1099.html"

        soup_url = semanticproxy_url + url 
        page = urlfetch.fetch(soup_url)
        soup = BeautifulSoup(page.content)  #whole page
        
        tags = soup.findAll(rel="tag")
        for tag in tags:
            tilde_request = tilde_base_url + "?format=rison&request=" + tag
            tilde_response = urlfetch.fetch(tilde_request)
            print tilde_response
            
        
          
                        
                        



def get_similar_topics(tag):
    tilde_request = tilde_base_url + "?format=xml&request=" + tag
    tilde_response = urlfetch.fetch(tilde_request)
    tilde_soup = BeautifulStoneSoup(tilde_response.content)
    similar_topics = [topic.contents[0] for topic in tilde_soup.findAll('title')][1:11]
    return similar_topics


def get_paragraphs_containing_tag(paragraphs,tag):
    for paragraph in paragraphs:
        if paragraph.find(text=re.compile(tag)):
            if (paragraph.find('p')):  #Don't Include Paragraphs with children paragraphs
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
     return text.replace(str_tag, '<span style="font-weight:bold;" class="answer_span">%s</span>' % str_tag)
