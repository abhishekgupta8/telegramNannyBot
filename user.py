class User(object):
   def __init__(self, userinfo, config):
      self.config = config
      self.name = userinfo.get('username', '')
      self.userid = userinfo.get('id', '')

   #
   # check if user is in the allowed list
   #
   def is_allowed(self):
      return self.name in self.config['allowed']

   #
   # check if user is an admin
   #
   def is_admin(self):
      return self.name in self.config['admin']

