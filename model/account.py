from google.appengine.ext import db
from google.appengine.api import users
import logging
from model.user import Profile
from model.proficiency import Proficiency

# Log a message each time this module get loaded.
logging.info('Loading %s', __name__)

      




class Account(db.Model):
    #key_name = unique_identifier 
    unique_identifier = db.StringProperty(required=True) # redundant
    nickname = db.StringProperty(required=False)  # redundant
    pass_count = db.IntegerProperty(required=False)
    date = db.DateTimeProperty(auto_now=True)
    #sponsorships - RefProperty 



class Award(db.Model):
    type = db.StringProperty(required=True, choices=set(["fluency", "excellence"]))
    topics = db.ListProperty(db.Key)
    levels = db.ListProperty(int)          # these dual lists can be zipped together as key:value pairs. 
    proficiency = db.ReferenceProperty(Proficiency,
                                    required=True,
                                    collection_name='awards')

    winner = db.ReferenceProperty(Profile,
                                    required=True,
                                    collection_name='awards')
    date = db.DateTimeProperty(auto_now=True)
    #sponsorships - RefProperty
    #pledges - RefProperty                                    
                                    
                                    
                                    
    
   


class SponsorPledge(db.Model):    
    sponsor = db.ReferenceProperty(Profile,
                                    required=True,
                                    collection_name='pledged_sponsorships')
    sponsor_type = db.StringProperty(required=True, choices=set(["personal", "corporate"])) # target one person, or many people.
    award_type = db.StringProperty(required=True, choices=set(["fluency", "excellence", "any award"]))  
    package = db.StringProperty(required=False, choices=set(["micro", "medium", "magna_cum_laude"]))                                    
    target = db.ListProperty(db.Key)#Profile   # paired list.    
    activated = db.ListProperty(bool)      # micro, medium or magna cum laude
    # Instead of activated, maybe sponsorship reference?
    proficiency = db.ReferenceProperty(Proficiency,
                                    required=False, # if False, then any proficiency is assumed. 
                                    collection_name='pledges')    
    date = db.DateTimeProperty(auto_now=True)
    # sponsorships - RefProperty
 

"""


Corporate sponsorships have no targets, or different targets. 

Should a sponsorship generator class be used? Sponsorship would only have one target. 


"""


class Sponsorship(db.Model):
    # There needs to be a sponsorship generator, for when the sponsorship is for a class of people. 
    sponsor = db.ReferenceProperty(Profile,
                                    required=True,
                                    collection_name='given_sponsorships')
    recipient = db.ReferenceProperty(Profile,
                                    required=True,
                                    collection_name='sponsorships')                                    
    package = db.StringProperty(required=True, choices=set(["micro", "medium", "magna_cum_laude"]))      # redundancy                              
    sponsor_type = db.StringProperty(required=False, choices=set(["personal", "corporate"])) # target one person, or many people.
    award_type = db.StringProperty(required=True, choices=set(["fluency", "excellence"]))  
    award = db.ReferenceProperty(Award,
                                    required=True,
                                    collection_name='sponsorships')
    pledge = db.ReferenceProperty(SponsorPledge,
                                    required=True,
                                    collection_name='sponsorships')                                        

    date = db.DateTimeProperty(auto_now=True)    

