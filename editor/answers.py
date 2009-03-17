

SETS_URL = "http://labs.google.com/sets?"

class Answers():
	"""

	Load Answer Suggestions for Quiz Editor

	"""

	def load(self, correct_answer, item_text):
		args = [correct_answer]
		# Rank words in item by size - we can improve this part later.
		text_list = list( set( item_text.split() ) )
		lower_text_list = [s.lower() for s in text_list]
		length_list = map(len,text_list)
		allzip = zip(length_list,text_list)
		allzip.sort()
		allzip.reverse()
		for arg in allzip[:3]: args.append(arg[1])
		# Format Argument for Request
		self.formatted_args = {"btn": "Large+Set"}
		key_index = 1
		for arg in args:
			key = "q" + str(key_index)
			key_index += 1
			self.formatted_args[key] = arg 

		# Filter Out Answers That Are Too Verbose
		# Send Request to Service and Open Response for Parsing
		sets = self.get_sets()
		# Extract List of Strings From Response
		answers = [a.contents[0] for a in sets.findAll('table')[1].contents[1].findAll('table')[0].findAll('a')]
		return [a for a in answers if a.lower() not in lower_text_list and len(a.split()) < 3]

		
	def get_sets(self):	
		# Send Request to Service and Open Response for Parsing
		import urllib
		self.formatted_args = urllib.urlencode(self.formatted_args)
		from google.appengine.api import urlfetch
		fetch_page = urlfetch.fetch(url = SETS_URL + self.formatted_args,
									method = urlfetch.GET) 
		from utils.BeautifulSoup import BeautifulSoup
		return BeautifulSoup(fetch_page.content)
