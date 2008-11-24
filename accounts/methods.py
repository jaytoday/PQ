import logging
# Log a message each time this module get loaded.
logging.info('Loading %s', __name__)
import cgi
from .model.user import QuizTaker



def registered(user_key):
	this_user = QuizTaker.get_by_key_name(user_key)
	if this_user: return this_user
	else: return False
	
	



def register_user(user_key, nickname, email):
	profile_path = nickname.lower()
	profile_path = profile_path.replace(' ','_')
	new_user = QuizTaker.get_or_insert(user_key,
						  unique_identifier = user_key, # redundancy
						  nickname = nickname,
						  fullname = nickname,
						  profile_path = profile_path,
						  email = email)
						  
	new_user.put()
	return new_user 




