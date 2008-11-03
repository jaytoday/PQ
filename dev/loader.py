from google.appengine.ext import bulkload
from google.appengine.api import datastore_types
from google.appengine.ext import search

class TopicLoader(bulkload.Loader):
  def __init__(self):
    bulkload.Loader.__init__(self, 'FreebaseTopic',
                         [('topic', str),
                          ('type', str),
                          ])

  def HandleEntity(self, entity):
    ent = search.SearchableEntity(entity)
    return ent

if __name__ == '__main__':
  bulkload.main(TopicLoader())
