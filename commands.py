import json
from humbug_helper import SupportBundleHelper
from collections import OrderedDict


class BotCommands(object):
   # list of valid commands

   HELP = u"/help"
   PING = u"/ping"

   LIST_SUPPORT_BUNDLES = u"/listSB"

   # end list of commands

   #
   # check if given command is valid
   #
   @classmethod
   def is_valid_command(cls, cmd):
      return cmd in BotCommands._commands

   #
   # check if given command is only available to authenticated users
   #
   @classmethod
   def is_authenticated(cls, cmd):
      try:
         return cls._commands[cmd]['authenticated']
      except Exception, e:
         print e
         return True

   #
   # check if given command is only available to admin users
   #
   @classmethod
   def is_admin_only(cls, cmd):
      try:
         return cls._commands[cmd]['admin']
      except Exception, e:
         print e
         return True

   @classmethod
   def bot_help(cls, botmessage):
      help_str = ""
      cmd = botmessage.command
      for cmd in BotCommands._commands:
         if BotCommands.is_admin_only(cmd) and \
               (not botmessage.user.is_admin()):
            continue
         help_str += '%s%s%s : %s\n' % \
            (cmd,
             " [opts]" if BotCommands._commands[cmd]['subcommands'] else "",
             " <args>" if BotCommands._commands[cmd]['args'] else "",
             BotCommands._commands[cmd]['help'])
         if BotCommands._commands[cmd]['subcommands']:
            help_str += "  subcommands:\n"
            for subcommand in BotCommands._commands[cmd]['subcommands']:
               _subcommand = BotCommands._commands[cmd]['subcommands'][subcommand]
               help_str += "    %s%s : %s\n" % \
                  (subcommand,
                  " <args>" if _subcommand['args'] else "",
                  _subcommand['help'])
      return help_str

   @classmethod
   def bot_ping(cls, botmessage):
      return "ping!"

   @classmethod
   def bot_support_bundle_list_get(cls, botmessage):
      sbHelper = SupportBundleHelper(botmessage.messagetext.split(" ")[1])
      return sbHelper.getList()

   @classmethod
   def process_command(cls, botmessage):
      cmd = botmessage.command
      if BotCommands.is_valid_command(cmd):
         return BotCommands._commands[cmd]["callback"](botmessage)
      return "Yo! What's this command? Tried /help?"


# command definitions
BotCommands._commands = OrderedDict()

BotCommands._commands.update({
   BotCommands.HELP: {
      "authenticated": True,
      "admin": False,
      "subcommands": None,
      "callback": BotCommands.bot_help,
      "help": "show this help",
      "args": False
   }})

BotCommands._commands.update({
   BotCommands.PING: {
      "authenticated": True,
      "admin": False,
      "subcommands": None,
      "callback": BotCommands.bot_ping,
      "help": "check if server is responsive",
      "args": False
   }})

BotCommands._commands.update({
   BotCommands.LIST_SUPPORT_BUNDLES: {
      "authenticated": True,
      "admin": False,
      "subcommands": None,
      "callback": BotCommands.bot_support_bundle_list_get,
      "help": "get list of support bundles. usage: /listSB <PR number>",
      "args": False
   }})


