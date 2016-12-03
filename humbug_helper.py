import requests
import zlib
import base64

hbURL = "http://humbug.eng.vmware.com/"
version = "2.1"

class SupportBundleHelper(object):
   def __init__(self, pr):
#      self.config = config
      self.pr = pr

   def SupportBundlesListGet(self):
      entryPoint = "arch"
      payload = {'urls': self.pr, 'ignore_timeout':'false'}
      r = requests.get(hbURL + entryPoint, params=payload)
      a = eval(r.text)
      prefix = a["prefix"]
      diff = a["diff"]
      suffix = a["suffix"]
      return [prefix, diff, suffix]
   
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
      [prefix, diff, suffix] = self.SupportBundlesListGet()
      return diff[0]
#      SupportBundleTextSearch(prefix, diff[0], suffix, "test2")
