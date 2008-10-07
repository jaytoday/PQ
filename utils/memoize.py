import settings  # When using Django so as to skip the cache during testing.
def memoize(key, time=60):
    """Decorator to memoize functions using memcache."""
    def decorator(fxn):
        def wrapper(*args, **kwargs):
            data = memcache.get(key)
            if data is not None:
                return data
            data = fxn(*args, **kwargs)
            memcache.set(key, data, time)
            return data
        return wrapper
    return decorator if not settings.DEBUG else fxn
    
    
"""
from django.shortcuts import render_to_response
@memoize('index')
def index_view(request):
                                  #Render the index view.
    return render_to_response("index.html")
    
from django.shortcuts import render_to_response
from google.appengine.ext import db
@memoize('index_data')
def query_datastore():
                              #Return a list of datastore objects, not just a query.
    return [x for x in db.Query(model).all().filter('attribute =', True)]
def index(request):
    object_list = query_datastore()
    return render_to_response('index.html', {'object_list': object_list})
    
"""        
