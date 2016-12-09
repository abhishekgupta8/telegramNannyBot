#!/usr/bin/env python

import json
import time

import telepot
from commands import BotCommands
from message import BotMessage


class Main(object):
   def __init__(self):
      self.context = {}
      self.reload_config()
      self.bot = telepot.Bot(self.config.get('apikey', ''))

   def send_error_message(self, message, userid):
      print message
      self.bot.sendMessage(userid, message)

   def reload_config(self):
      with open("config.json") as f:
         self.config = json.load(f)

   def check_cmd_access(self, botmessage):
      if BotCommands.is_authenticated(botmessage.command):
         if not botmessage.user.is_allowed():
            print '%s not in allowed list' % botmessage.user.name
            return False
         if BotCommands.is_admin_only(botmessage.command) and \
               (not botmessage.user.is_admin()):
            print '%s not in admin list' % botmessage.user.name
            return False
      return True

   def _handle(self, msg):
      chat_id = msg['chat']['id']
      botmessage = BotMessage(msg, self.config)
      if botmessage.user.userid not in self.context:
         self.context[botmessage.user.userid] = {'LDAP_username': None,
                                                 'PR': None,
                                                 'SB': None,
                                                 'search_keyword': None,
                                                 'comment': None,
                                                 'saved_search': None}

      # check if user is allowed to access
      if not self.check_cmd_access(botmessage):
         self.bot.sendMessage(botmessage.user.userid,
            'You are not authorized to use this bot.')
         self.send_error_message('Unauthorized access by %s (%s) at %s. Cmd: %s' %
               (botmessage.user.name, botmessage.user.userid,
                botmessage.date, botmessage.command), botmessage.user.userid)
         return

      # check if command is valid
      if not BotCommands.is_valid_command(botmessage.command):
         self.bot.sendMessage(botmessage.user.userid,
            "Unrecognized command! Check /help")
         return

      rc = BotCommands.process_command(botmessage, self.context)
      maxLen = 4000
      if rc:
         for i in range(0, len(rc), maxLen):
            self.bot.sendMessage(chat_id, rc[i:i+maxLen])

   def start(self):
      self.bot.message_loop(self._handle)

if __name__ == '__main__':
   #counter = 0
   main = Main()
   main.start()

   while (1):
      time.sleep(1/1000000)
      # reload config every minute
      #if counter == 60:
      #   counter = 0
      #   main.reload_config()
      #   print 'reloaded config'
      #counter += 1
   print 'done'

