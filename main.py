#!/usr/bin/env python

import json
import time

import telepot
from commands import BotCommands
from message import BotMessage


class Main(object):
   def __init__(self):
      self.reload_config()
      self.bot = telepot.Bot(self.config.get('apikey', ''))
      #self.bot.sendMessage(221735159, 'Bot started')

   def send_error_message(self, message):
      self.bot.sendMessage(221735159, message)

   def reload_config(self):
      with open("config.json") as f:
         self.config = json.load(f)

   def check_cmd_access(self, botmessage):
      if BotCommands.is_authenticated(botmessage.command):
         if not botmessage.user.is_allowed():
            print '%s not in allowed list' % botmessage.user.name
            return False
         if BotCommands.is_admin_only(botmessage.command) and \
               (not botmessage.is_admin_user()):
            print '%s not in admin list' % botmessage.user.name
            return False
      return True

   def _handle(self, msg):
      print msg
      botmessage = BotMessage(msg, self.config)

      # check if user is allowed to access
      if not self.check_cmd_access(botmessage):
         self.bot.sendMessage(botmessage.user.userid,
            'Poking around without permission! Ask Ajay for details.')
         self.send_error_message('Unauthorized access by %s (%s) at %s. Cmd: %s' %
               (botmessage.user.name, botmessage.user.userid,
                botmessage.date, botmessage.command))
         return

      # check if command is valid
      if not BotCommands.is_valid_command(botmessage.command):
         self.bot.sendMessage(botmessage.user.userid,
            "Yo! What's this command? Check /help")
         return

      rc = BotCommands.process_command(botmessage)
      if rc:
         self.bot.sendMessage(botmessage.user.userid, rc)

   def start(self):
      self.bot.message_loop(self._handle)

if __name__ == '__main__':
   #counter = 0
   main = Main()
   main.start()

   while (1):
      time.sleep(1)
      # reload config every minute
      #if counter == 60:
      #   counter = 0
      #   main.reload_config()
      #   print 'reloaded config'
      #counter += 1
   print 'done'

