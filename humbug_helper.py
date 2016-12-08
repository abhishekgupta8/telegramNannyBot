import requests
import zlib
import base64

hbURL = "http://10.146.205.34/"
#version = "2.1"

class SupportBundleHelper(object):
   def __init__(self, pr):
      self.pr = pr

   def SupportBundlesListGet(self):
      entryPoint = "arch"
      payload = {'urls': self.pr, 'ignore_timeout':'false'}
      r = requests.get(hbURL + entryPoint, params=payload)
      a = eval(r.text)
      if 'error' in a:
         if a['error'] == 256:
            return "This PR does not have any support bundles"
         else:
            return "An error occurred: %d" % a['error']
      prefix = a["prefix"]
      diff = a["diff"]
      suffix = a["suffix"]
      if len(diff) == 1:
         if diff[0] == self.pr:
            return "This PR does not exist"
      return "\n".join(diff)

   def SupportBundlesPathsGet(self, index):
      entryPoint = "arch"
      payload = {'urls': self.pr, 'ignore_timeout':'false'}
      r = requests.get(hbURL + entryPoint, params=payload)
      a = eval(r.text)
      if 'error' in a:
         if a['error'] == 256:
            return "This PR does not have any support bundles"
         else:
            return "An error occurred: %d" % a['error']
      prefix = a["prefix"]
      diff = a["diff"]
      suffix = a["suffix"]
      if len(diff) == 1:
         if diff[0] == self.pr:
            return "This PR does not exist"
      return "%s%s%s"  % (prefix, diff[index], suffix)


   def EncodeReq(self, inStr):
      compressedStr = zlib.compress(inStr)
      encodedStr = base64.b64encode(compressedStr)
      return "".join(encodedStr.split("\n"))

   def SupportBundleTextSearch(self, target, term):
      entryPoint = "hbapi/search"
      payload = {'target': target,
                 'term': term
                }
      r = requests.get(hbURL + entryPoint, params=payload)
      # XXX Check for error code
      return r.text

   def getList(self):
      return self.SupportBundlesListGet()

   def TextSearchInBundleId(self, supportBundleID, term):
      sbPath = self.SupportBundlesPathsGet(supportBundleID)
      result = self.SupportBundleTextSearch(sbPath, term)
      return result

if __name__ == '__main__':
   test = SupportBundleHelper('1772785')
#   print "getting path"
#   sbPath = test.SupportBundlesPathsGet(2)
#   print "path: %s" % (sbPath)
#   print test.SupportBundleTextSearch(sbPath, 'warning')
   print test.TextSearchInBundleId(2, 'warning')
