from google.appengine.ext import db
from google.appengine.api import users
import logging
import user 
from proficiency import Proficiency

# Log a message each time this module get loaded.
logging.info('Loading %s', __name__)

      




class Account(db.Model):
    #key_name = unique_identifier 
    unique_identifier = db.StringProperty(required=True) # redundant
    nickname = db.StringProperty(required=False)  # redundant
    pass_count = db.IntegerProperty(required=False) 



class Award(db.Model):
    type = db.StringProperty(required=True, choices=set(["Fluency", "Excellence"]))
    topics = db.ListProperty(db.Key)
    levels = db.ListProperty(int)          # these dual lists can be zipped together as key:value pairs. 
    proficiency = db.ReferenceProperty(Proficiency,
                                    required=True,
                                    collection_name='awards')
    winner = db.ReferenceProperty(user.Profile,
                                    required=True,
                                    collection_name='awards')
                                    
                                    
                                    
    
   


class Sponsor(db.Model):   #what is this needed for? if its not needed, maybe these values can be help in account or profile?
    #key_name = unique_identifier 
    unique_identifier = db.StringProperty(required=False) # redundant
    pass_count = db.IntegerProperty(required=False)


class SponsorPledge(db.Model):    
    package = db.StringProperty(required=False, choices=set(["micro", "medium", "magna cum laude"]))                                    
    type = db.StringProperty(required=False, choices=set(["personal", "corporate"])) # target one person, or many people.
    award = db.ReferenceProperty(Proficiency,
                                    required=False,
                                    collection_name='pledges')    
    target = db.ListProperty(db.Key)#Profile   # paired list.    
    activated = db.ListProperty(bool)      # micro, medium or magna cum laude
    

"""


Corporate sponsorships have no targets, or different targets. 

Should a sponsorship generator class be used? Sponsorship would only have one target. 


"""


class Sponsorship(db.Model):
    # There needs to be a sponsorship generator, for when the sponsorship is for a class of people. 
    sponsor = db.ReferenceProperty(Account,
                                    required=True,
                                    collection_name='sponsorships')
    recipient = db.ReferenceProperty(user.Profile,
                                    required=True,
                                    collection_name='sponsorships')                                    
    package = db.StringProperty(required=False, choices=set(["micro", "medium", "magna cum laude"]))      # redundancy                              
    type = db.StringProperty(required=False, choices=set(["personal", "corporate"])) # target one person, or many people.
    
    award = db.ReferenceProperty(Award,
                                    required=True,
                                    collection_name='sponsorships')
                                    
    pledge = db.ReferenceProperty(SponsorPledge,
                                    required=True,
                                    collection_name='sponsorships')                                        

    

