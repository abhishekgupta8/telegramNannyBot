import os
import xmlrpclib
from login import getServer

class BugzillaHelper(object):
   def __init__(self):
      self.server = getServer()

   # Get bug data-structure corresponding to a PR number
   def getInfo(self, pr):
      try:
         bugInfo = self.server.Bug.show_bug(int(pr))
         return bugInfo
      except ValueError as value_err:
         raise Exception(value_err)
      except xmlrpclib.Fault as not_found_err:
         raise Exception(not_found_err)
      except:
         raise Exception("Error in get summary")

   # Get summary, which is the title, for a PR
   def getSummary(self, pr):
      try:
         bugInfo = self.getInfo(pr)
         return bugInfo['short_desc']
      except Exception as e:
         raise Exception(e)

   def getAssignee(self, pr):
      try:
         bugInfo = self.getInfo(pr)
         return bugInfo['assigned_to']
      except Exception as e:
         return Exception(e)

   def getReporter(self, pr):
      try:
         bugInfo = self.getInfo(pr)
         return bugInfo['reporter']
      except Exception as e:
         return Exception(e)

   def getSavedQueries(self, uName):
      try:
         savedSearch = self.server.Search.get_all_saved_queries(uName)
         return savedSearch
      except ValueError as value_err:
         raise Exception(value_err)
      except xmlrpclib.Fault as not_found_err:
         raise Exception(not_found_err)
      except:
         raise Exception("Error in get summary")

   def getBugList(self, uName, query):
      try:
         bugList = self.server.Search.run_saved_query(uName, query)['bugidlist']
         return str(bugList)
      except ValueError as value_err:
         raise Exception(value_err)
      except xmlrpclib.Fault as not_found_err:
         raise Exception(not_found_err)
      except Exception as e:
         raise Exception(e)

   def getUpdate0(self, pr):
      try:
         bugInfo = self.getInfo(pr)
         return bugInfo['description']
      except Exception as e:
         return Exception(e)


if __name__ == '__main__':
    test = BugzillaHelper()
    print test.getSavedQueries('kotwala')
