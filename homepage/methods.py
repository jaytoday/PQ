

ACTION_THRESHOLD = 20

def load_action_feed():
	action_feed = []
	from model.account import Sponsorship, Award
	recent_sponsorships = Sponsorship.all().order('-date').fetch(ACTION_THRESHOLD)
	recent_awards = Award.all().order('-date').fetch(ACTION_THRESHOLD)
	action_feed.extend(recent_sponsorships)
	action_feed.extend(recent_awards)
	from operator import attrgetter
	action_feed.sort(key = attrgetter('date'), reverse = True)
	from google.appengine.api import memcache
	memcache.set('action_feed',action_feed, 60000)
	memcache.set('next_items',action_feed, 60000)
	return update_action_feed()
	


def update_action_feed():
	from google.appengine.api import memcache
	all_next_items = memcache.get('next_items')
	if len(all_next_items) < 6: next_items = all_next_items
	return all_next_items
