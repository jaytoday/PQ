import logging
# Log a message each time this module get loaded.
logging.info('Loading %s', __name__)
import cgi
from .model.user import Profile, QuizTaker
from google.appengine.api import images
from google.appengine.ext import db


def registered(user_key):
    this_user = Profile.get_by_key_name(user_key)
    if this_user: return this_user
    else: return False
    
    



def register_user(user_key, nickname, email):
    import random
    from model.user import ProfilePicture
    pq_pics = ProfilePicture.gql("WHERE type = :1", "pq")
    random_pic = random.sample(pq_pics, 1)[0]
    
    profile_path = nickname.lower()
    profile_path = profile_path.replace(' ','_')
    new_user = Profile.get_or_insert(key_name = user_key,
                          unique_identifier = user_key, # redundancy
                          nickname = nickname,
                          fullname = nickname,
                          profile_path = profile_path,
                          photo = random_pic
                          )
                          
    if email: new_user.email = email
    new_user.put()
    return new_user 



def register_qt(user_key, nickname):
    new_qt = QuizTaker.get_or_insert(key_name = user_key,
                                     unique_identifier = user_key, # redundancy
                                     nickname = nickname, # redundancy
                                     )
    new_qt.put()
    return new_qt                                   
    
    



def get_subjects(subjects, memberships):
	subject_list = []
	for s in subjects:
		is_member = False
		for m in memberships:
			if m.subject == s:
				if m.is_admin: is_member = "admin"
				else: is_member = "contributor"
		subject_list.append({"subject": s, "is_member": is_member})
	return subject_list 
