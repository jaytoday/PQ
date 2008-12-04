import logging
# Log a message each time this module get loaded.
logging.info('Loading %s', __name__)
import cgi
from .model.user import Profile, QuizTaker, ProfilePicture
from model.account import Account
import random


def registered(user_key):
    this_user = Profile.get_by_key_name(user_key)
    if this_user: return this_user
    else: return False
    
    



def register_user(user_key, nickname, email):
    profile_path = nickname.lower()
    profile_path = profile_path.replace(' ','_')
    photo = default_photo()
    new_user = Profile.get_or_insert(key_name = user_key,
                          unique_identifier = user_key, # redundancy
                          nickname = nickname,
                          fullname = nickname,
                          profile_path = profile_path,
                          photo = photo,
                          )
                          
    if email: new_user.email = email
    new_user.put()
    return new_user 



def register_qt(user_key, nickname):
    new_qt = QuizTaker.get_or_insert(key_name = user_key,
                                     unique_identifier = user_key, # redundancy
                                     nickname = nickname,
                                     )
    new_qt.put()
    return new_qt                                   
    

def register_account(user_key):
    new_account = Account.get_or_insert(key_name = user_key,
                                     unique_identifier = user_key # redundancy
                                     )
    new_account.put()
    return new_account                                   
    
        

def default_photo():
	photos = ProfilePicture.gql("WHERE type = :1", "pq").fetch(10)
	photo = random.sample(photos, 1) 
	return photo[0]



