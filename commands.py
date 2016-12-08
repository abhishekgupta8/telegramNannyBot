import json
from humbug_helper import SupportBundleHelper
from collections import OrderedDict
from bugzilla_helper import BugzillaHelper

class BotCommands(object):
   # list of valid commands

   HELP = u"/help"
   PING = u"/ping"

   BUGZILLA_LIST_SUPPORT_BUNDLES = u"/listSB"
   BUGZILLA_SEARCH_SUPPORT_BUNDLE = u"/searchSB"
   BUGZILLA_GET_SUMMARY = u"/summarize"
   BUGZILLA_GET_BUG_DESCRIPTION = u"/getBugDescription"
   BUGZILLA_POST_BUG_COMMENT = u"/postBugComment"
   BUGZILLA_GET_REPORTER = u"/getReporter"
   BUGZILLA_GET_ASSIGNEE = u"/getAssignee"
   BUGZILLA_GET_SAVED_SEARCH = u"/getSavedSearch"
   BUGZILLA_GET_BUG_LIST = u"/getBugList"

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
   def bot_bugzilla_support_bundle_list(cls, botmessage):
      try:
         sbHelper = SupportBundleHelper(botmessage.messagetext.split(" ")[1])
         return sbHelper.getList()
      except Exception as e:
         return str(e)

   @classmethod
   def bot_humbug_support_bundle_search(cls, botmessage):
      try:
         params = botmessage.messagetext.split(" ")
         sbHelper = SupportBundleHelper(params[1])
         return sbHelper.TextSearchInBundleId(int(params[2]), params[3])
      except Exception as e:
         return str(e)

   @classmethod
   def bot_bugzilla_get_summary(cls, botmessage):
      try:
         bugzillaHelper = BugzillaHelper()
         return bugzillaHelper.getSummary(botmessage.messagetext.split(" ")[1])
      except Exception as e:
         return str(e)

   @classmethod
   def bot_bugzilla_get_reporter(cls, botmessage):
      try:
         bugzillaHelper = BugzillaHelper()
         return bugzillaHelper.getReporter(botmessage.messagetext.split(" ")[1])
      except Exception as e:
         return str(e)

   @classmethod
   def bot_bugzilla_get_assignee(cls, botmessage):
      try:
         bugzillaHelper = BugzillaHelper()
         return bugzillaHelper.getAssignee(botmessage.messagetext.split(" ")[1])
      except Exception as e:
         return str(e)

   @classmethod
   def bot_bugzilla_get_saved_search(cls, botmessage):
      try:
         bugzillaHelper = BugzillaHelper()
         return bugzillaHelper.getSavedQueries(botmessage.messagetext.split(" ")[1])
      except Exception as e:
         return str(e)

   @classmethod
   def bot_bugzilla_get_bug_list(cls, botmessage):
      try:
         bugzillaHelper = BugzillaHelper()
         params = botmessage.messagetext.split(" ")
         return bugzillaHelper.getBugList(params[1], params [2])
      except Exception as e:
         return str(e)

   @classmethod
   def bot_bugzilla_get_description(cls, botmessage):
      try:
         bugzillaHelper = BugzillaHelper()
         params = botmessage.messagetext.split(" ")
         return bugzillaHelper.getUpdate0(params[1])
      except Exception as e:
         return str(e)

   @classmethod
   def bot_bugzilla_post_comment(cls, botmessage):
      try:
         bugzillaHelper = BugzillaHelper()
         params = botmessage.messagetext.split(" ")
         comment = ' '.join(params[2:])
         bugzillaHelper.addComment(params[1], comment)
         return "Comment successfully posted."
      except Exception as e:
         return str(e)

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
   BotCommands.BUGZILLA_LIST_SUPPORT_BUNDLES: {
      "authenticated": True,
      "admin": False,
      "subcommands": None,
      "callback": BotCommands.bot_bugzilla_support_bundle_list,
      "help": "get list of support bundles. usage: /listSB <PR number>",
      "args": False
   }})

BotCommands._commands.update({
   BotCommands.BUGZILLA_SEARCH_SUPPORT_BUNDLE: {
      "authenticated": True,
      "admin": False,
      "subcommands": None,
      "callback": BotCommands.bot_humbug_support_bundle_search,
      "help": "get list of support bundles. usage: /searchSB <PR number> <bundleID> <search string>",
      "args": False
   }})

BotCommands._commands.update({
   BotCommands.BUGZILLA_GET_SUMMARY: {
      "authenticated": True,
      "admin": False,
      "subcommands": None,
      "callback": BotCommands.bot_bugzilla_get_summary,
      "help": "gets the summary of the bug. usage: /summarize <PR number>",
      "args": False
   }})

BotCommands._commands.update({
   BotCommands.BUGZILLA_GET_REPORTER: {
      "authenticated": True,
      "admin": False,
      "subcommands": None,
      "callback": BotCommands.bot_bugzilla_get_reporter,
      "help": "gets the reporter of the bug. usage: /getReporter <PR number>",
      "args": False
   }})

BotCommands._commands.update({
   BotCommands.BUGZILLA_GET_ASSIGNEE: {
      "authenticated": True,
      "admin": False,
      "subcommands": None,
      "callback": BotCommands.bot_bugzilla_get_assignee,
      "help": "gets the assignee of the bug. usage: /getAssignee <PR number>",
      "args": False
   }})

BotCommands._commands.update({
   BotCommands.BUGZILLA_GET_SAVED_SEARCH: {
      "authenticated": True,
      "admin": False,
      "subcommands": None,
      "callback": BotCommands.bot_bugzilla_get_saved_search,
      "help": "gets the list of saved searches for a user. usage: /getSavedSearch <LDAP username>",
      "args": False
   }})

BotCommands._commands.update({
   BotCommands.BUGZILLA_GET_BUG_LIST: {
      "authenticated": True,
      "admin": False,
      "subcommands": None,
      "callback": BotCommands.bot_bugzilla_get_bug_list,
      "help": "gets the list of bug for a saved search. usage: /getBugList <LDAP username> <query>",
      "args": False
   }})

BotCommands._commands.update({
   BotCommands.BUGZILLA_GET_BUG_DESCRIPTION: {
      "authenticated": True,
      "admin": False,
      "subcommands": None,
      "callback": BotCommands.bot_bugzilla_get_description,
      "help": "gets bugs description. usage: /getBugDescription <PR number>",
      "args": False
   }})

BotCommands._commands.update({
   BotCommands.BUGZILLA_POST_BUG_COMMENT: {
      "authenticated": True,
      "admin": False,
      "subcommands": None,
      "callback": BotCommands.bot_bugzilla_post_comment,
      "help": "posts comment to the bug. usage: /postBugComment <PR number> <comment>",
      "args": False
   }})
