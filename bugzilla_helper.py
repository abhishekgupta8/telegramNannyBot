import os
import xmlrpclib
from login import getServer

class BugzillaHelper(object):
   def __init__(self, pr):
      self.pr = pr
      self.server = getServer()


   def getSummary(self):
      try:
         summary = self.server.Bug.show_bug(int(self.pr))['short_desc']
      except ValueError as value_err:
         return str(value_err)
      except xmlrpclib.Fault as not_found_err:
         return str(not_found_err)
      except:
         return "Error in get summary"
      return summary
         
if __name__ == '__main__':
    test = BugzillaHelper('235435727')
    print test.getSummary()
