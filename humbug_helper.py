import requests
import zlib
import base64

hbURL = "http://humbug.eng.vmware.com/"
version = "2.1"

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
   
   def EncodeReq(self, inStr):
      compressedStr = zlib.compress(inStr)
      encodedStr = base64.b64encode(compressedStr)
      return "".join(encodedStr.split("\n"))
   
   def SupportBundleTextSearch(sbPrefix, sbBody, sbSuffix, searchTerm):
      entryPoint = "hb"
      payload = {'searchterm': searchTerm,
                 'prefix': sbPrefix,
                 'url': EncodeReq(sbBody),
                 'suffix': sbSuffix,
                 'v': version}
   
      r = requests.get(hbURL + entryPoint, params=payload)
      print(r.url)

   def getList(self):
      return self.SupportBundlesListGet()
#      SupportBundleTextSearch(prefix, diff[0], suffix, "test2")
