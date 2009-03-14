import logging
import wsgiref.handlers
import datetime, time
from utils.webapp import template
from google.appengine.ext import db
from utils import webapp
from .utils.utils import tpl_path
from model.quiz_the_bill import Bill

BILL_LIMIT = 10
TEMPLATE_PATH = 'quiz_the_bill/'
OPENCONGRESS_INFO_URL = "http://www.opencongress.org/tools/bill_status_panel?" #bill_id=111-h45
GOVTRACK_URL = "http://www.govtrack.us/congress/billtext.xpd?"
OPENCONGRESS_BR_URL = "http://www.opencongress.org/battle_royale.xml?" 


class FrontPage(webapp.RequestHandler):
  def get(self):    
    template_values = {'bills': self.get_bills()}
    path = tpl_path(TEMPLATE_PATH + 'frontpage.html')
    self.response.out.write(template.render(path, template_values))
    return
    
  def get_bills(self):
      top_ten_bills = Bill.all().order('rank').fetch(10)
      return top_ten_bills 
      
    
class RenderBill(webapp.RequestHandler):
  def get(self):    
    template_values = {'url': self.get_bill_url() }
    path = tpl_path(TEMPLATE_PATH + 'iframe.html')
    self.response.out.write(template.render(path, template_values))
    return
    
    



  """
  Instead of screwing around with paths, just stick it in an iframe
  """
  def get_bill_url(self):	
	# Send Request to Service and Open Response for Parsing
	import urllib
	self.request_args = {'bill':  self.request.get('bill_id')}
	self.formatted_args = urllib.urlencode(self.request_args)
	return GOVTRACK_URL + self.formatted_args
	
	

  def get_bill(self):	
	# Send Request to Service and Open Response for Parsing
	import urllib
	self.formatted_args = urllib.urlencode(self.request_args)
	from google.appengine.api import urlfetch
	fetch_page = urlfetch.fetch( #url = GOVTRACK_URL + + "/text",
	                            url = GOVTRACK_URL + self.formatted_args,
								method = urlfetch.GET) 
	return fetch_page.content
	
	from utils.BeautifulSoup import BeautifulSoup	
	document = fetch_page.content #self.fix_urls( fetch_page.content ,"http://www.govtrack.us/")
	document = document.replace('</head>', '<base href="http://www.govtrack.us/" /></head>') 
	document = document.replace('src="/', 'src="http://www.govtrack.us/')
	document = document.replace('="billtext/', '="http://www.govtrack.us/congress/billtext/')
	document = document.replace('href="/', 'href="http://www.govtrack.us/')
	document = document.replace('background="/', 'background="http://www.govtrack.us/')	
	return document
	for i in list(document): print i
	logging.info(document)
	document = BeautifulSoup(fetch_page.content)
	return
	for i in list(document.contents): print str(i).replace
	return
	return document 	 



  def fix_urls(self, document, base_url): # Fix relative paths in document
    import re, urlparse
    regexes = [ re.compile(r'\bhref\s*=\s*("[^"]*"|\'[^\']*\'|[^"\'<>=\s]+)'),
                re.compile(r'\bsrc\s*=\s*("[^"]*"|\'[^\']*\'|[^"\'<>=\s]+)'),
                re.compile(r'\bbackground\s*=\s*("[^"]*"|\'[^\']*\'|[^"\'<>=\s]+)'), ]
    ret = []
    last_end = 0
    for find_re in regexes:
		for match in find_re.finditer(document):
			url = match.group(1)
			if url[0] in "\"'":
				url = url.strip(url[0])
			parsed = urlparse.urlparse(url)
			if parsed.scheme == parsed.netloc == '': #relative to domain
				url = urlparse.urljoin(base_url, url)
				ret.append(document[last_end:match.start(1)])
				ret.append('"%s"' % (url,))
				last_end = match.end(1)
		ret.append(document[last_end:])
		document = ''.join(ret)
    return ''.join(ret)


    



class UpdateStats(webapp.RequestHandler):
  def get(self):    
    self.save = []
    bills = self.get_top_bills()
    for bill in bills: self.update_bill(bill)
    db.put(self.save) # save new bills to datastore in one trip

    return
    
    
  def get_top_bills(self):	
	# Send Top Bills From OpenCongress Service
	import urllib
	self.request_args = {'order':  'desc',
	                     'page' :    1,
	                     'sort' :  'vote_count_1',
	                     'timeframe' : '1day' }
	self.formatted_args = urllib.urlencode(self.request_args)
	from google.appengine.api import urlfetch
	fetch_page = urlfetch.fetch(  url = OPENCONGRESS_BR_URL + self.formatted_args,
								method = urlfetch.GET) 
	from utils.BeautifulSoup import BeautifulStoneSoup	
	document = BeautifulStoneSoup(fetch_page.content)
	bills = []
	ids = [i.contents[0] for i in document.findAll('ident')]
	titles = [t.contents[0] for t in document.findAll('title-full-common')]
	current_rank = 1
	for i,t in zip(ids, titles)[:BILL_LIMIT]:
	    bills.append({'id': str(i), 
	                  'title': str(t),
	                  'rank' : current_rank })
	    current_rank += 1
	return bills



  def update_bill(self, bill):
    # Check if a bill exists in datastore, and update its stats.
	this_bill = Bill.get_by_key_name("bill_" + bill['id']) 
	if this_bill is None: this_bill = self.create_bill(bill)
	this_bill.rank = bill['rank']
	import urllib
	self.request_args = {'bill_id':  bill['id']}
	self.formatted_args = urllib.urlencode(self.request_args)
	from google.appengine.api import urlfetch
	fetch_page = urlfetch.fetch( url = OPENCONGRESS_INFO_URL + self.formatted_args,
								method = urlfetch.GET) 
	from utils.BeautifulSoup import BeautifulSoup	
	document = BeautifulSoup(fetch_page.content)
	property_count = 0	  
	this_bill.introduction_date = str(document.findAll('li')[property_count]).split('</strong> ')[1].split('</li>')[0]
	this_bill.status = str(document.findAll('li')[property_count + 1]).split('</strong> ')[1].split('</li>')[0]
	if this_bill.status == "This Bill Has Become Law": 
	    property_count = -1 # no next step
	else: this_bill.next_step = str(document.findAll('li')[property_count + 2]).split('</strong> ')[1].split('</li>')[0]
	this_bill.latest_action = str(document.findAll('li')[property_count + 3]).split('</strong> ')[1].split('</li>')[0]
	this_bill.sponsor = str(document.findAll('li')[property_count + 4]).split('</strong> ')[1].split('</li>')[0]
	self.save.append(this_bill)
	return


  def create_bill(self, bill):
    # Save a new bill to the datastore
    new_bill = Bill(key_name = "bill_" + bill['id'],
                    id = bill['id'],
                    title = bill['title'])
    print "created new bill"
    logging.info('saved new bill wih title %s,id %s, and rank %s' % (bill['title'], bill['id'], str(bill['rank'])))
    return new_bill              
                    
