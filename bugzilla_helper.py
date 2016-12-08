import os
import xmlrpclib
from login import getServer

class BugzillaHelper(object):
   def __init__(self, pr):
      self.pr = pr
      self.server = getServer()


   def getInfo(self):
      try:
         bugInfo = self.server.Bug.show_bug(int(self.pr))
         return bugInfo
      except ValueError as value_err:
         raise ValueError(value_err)
      except xmlrpclib.Fault as not_found_err:
         raise Exception(not_found_err)
      except:
         raise Exception("Error in get summary")


   def getSummary(self):
      try:
         bugInfo = self.getInfo()
         return bugInfo['short_desc']
      except Exception as e:
         return str(e)

   def getAssignee(self):
      try:
         bugInfo = self.getInfo()
         return bugInfo['assigned_to']
      except Exception as e:
         return str(e)

   def getReporter(self):
      try:
         bugInfo = self.getInfo()
         return bugInfo['reporter']
      except Exception as e:
         return str(e)

   def getSavedQueries(self, uName):
      try:
         savedSearch = self.server.Search.get_all_saved_queries(uName)
         return savedSearch
      except ValueError as value_err:
         raise ValueError(value_err)
      except xmlrpclib.Fault as not_found_err:
         raise Exception(not_found_err)
      except:
         raise Exception("Error in get summary")

   def getBugList(self, uName, query):
      try:
         bugList = self.server.Search.run_saved_query(uName, query)['bugidlist']
         return str(bugList)
      except ValueError as value_err:
         raise ValueError(value_err)
      except xmlrpclib.Fault as not_found_err:
         raise Exception(not_found_err)
      except Exception as e:
         raise Exception(e)


if __name__ == '__main__':
    test = BugzillaHelper('1777085')
    #print list(test.getInfo().keys())
    #print test.getSummary()
    mySavedQueries = test.getSavedQueries('kotwala')
    print (test.getBugList('kotwala', mySavedQueries[3]))
    #print len(bugList)
#    for bug in bugList:
#       print bug[
    mySavedQueries = test.getSavedQueries('gabhishek')
    print mySavedQueries
