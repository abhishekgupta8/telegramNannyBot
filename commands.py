import json
from humbug_helper import SupportBundleHelper
from collections import OrderedDict
from bugzilla_helper import BugzillaHelper
from coresummary import CoreSummary

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
   CORESUMMARY_GET_REPORT = u"/getCoreSummary"
   SET_PR = u"/setPR"
   SET_LDAP = u"/setLDAPUsername"
   SET_SB = u"/setSB"
   SET_SEARCH_KEYWORD = u"/setKeyword"
   SET_COMMENT = u"/setComment"
   SET_SAVED_SEARCH = u"/setSavedSearch"

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
   def create_keyboard_dict(cls, text):
      return {'isKeyboard':True, 'text': text}

   @classmethod
   def create_text_dict(cls, text):
      return {'isKeyboard':False, 'text': text}

   @classmethod
   def check_pr(cls, context, userid):
      return context[userid]['PR'] != None

   @classmethod
   def check_sb(cls, context, userid):
      return context[userid]['SB'] != None

   @classmethod
   def check_ldap_username(cls, context, userid):
      return context[userid]['LDAP_username'] != None

   @classmethod
   def check_comment(cls, context, userid):
      return context[userid]['comment'] != None

   @classmethod
   def check_search_keyword(cls, context, userid):
      return context[userid]['search_keyword'] != None

   @classmethod
   def check_saved_search(cls, context, userid):
      return context[userid]['saved_search'] != None

   @classmethod
   def get_pr(cls, context, userid):
      return context[userid]['PR']

   @classmethod
   def get_sb(cls, context, userid):
      return context[userid]['SB']

   @classmethod
   def get_ldap_username(cls, context, userid):
      return context[userid]['LDAP_username']

   @classmethod
   def get_comment(cls, context, userid):
      return context[userid]['comment']

   @classmethod
   def get_search_keyword(cls, context, userid):
      return context[userid]['search_keyword']

   @classmethod
   def get_saved_search(cls, context, userid):
      return context[userid]['saved_search']

   @classmethod
   def bot_help(cls, botmessage, context):
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
      return BotCommands.create_keyboard_dict(help_str)

   @classmethod
   def bot_ping(cls, botmessage, context):
      return BotCommands.create_text_dict("pong!")

   @classmethod
   def bot_set_pr(cls, botmessage, context):
      context[botmessage.user.userid]['PR'] = botmessage.args[0]
      return "PR successfully added!"

   @classmethod
   def bot_set_sb(cls, botmessage, context):
      context[botmessage.user.userid]['SB'] = botmessage.args[0]
      return "Support Bundle successfully added!"

   @classmethod
   def bot_set_ldap_username(cls, botmessage, context):
      context[botmessage.user.userid]['LDAP_username'] = botmessage.args[0]
      return "LDAP username successfully added!"

   @classmethod
   def bot_set_comment(cls, botmessage, context):
      context[botmessage.user.userid]['comment'] = ' '.join(botmessage.args)
      return "Comment successfully added!"

   @classmethod
   def bot_set_search_keyword(cls, botmessage, context):
      context[botmessage.user.userid]['search_keyword'] = ' '.join(botmessage.args)
      return "Search keyword successfully added!"

   @classmethod
   def bot_set_saved_search(cls, botmessage, context):
      context[botmessage.user.userid]['saved_search'] = ' '.join(botmessage.args)
      return "Saved search successfully added!"

   @classmethod
   def bot_bugzilla_support_bundle_list(cls, botmessage, context):
      try:
         userid = botmessage.user.userid
         if (not BotCommands.check_pr(context, userid)):
            return "Set PR first using /setPR <PR number>"
         sbHelper = SupportBundleHelper(BotCommands.get_pr(context, userid))
         return sbHelper.getList()
      except Exception as e:
         return str(e)

   @classmethod
   def bot_humbug_support_bundle_search(cls, botmessage, context):
      try:
         userid = botmessage.user.userid
         if (not BotCommands.check_pr(context, userid)):
            return "Set PR first using /setPR <PR number>"
         if (not BotCommands.check_search_keyword(context, userid)):
            return "Set search keyword first using /setKeyword <search keyword>"
         sbHelper = SupportBundleHelper(BotCommands.get_pr(context, userid))
         return sbHelper.TextSearchInBundleId(0,
                                              BotCommands.get_search_keyword(context, userid))
      except Exception as e:
         return str(e)

   @classmethod
   def bot_bugzilla_get_summary(cls, botmessage, context):
      try:
         bugzillaHelper = BugzillaHelper()
         userid = botmessage.user.userid
         if (not BotCommands.check_pr(context, userid)):
            return "Set PR first using /setPR <PR number>"
         return bugzillaHelper.getSummary(BotCommands.get_pr(context, userid))
      except Exception as e:
         return str(e)

   @classmethod
   def bot_bugzilla_get_reporter(cls, botmessage, context):
      try:
         bugzillaHelper = BugzillaHelper()
         userid = botmessage.user.userid
         if (not BotCommands.check_pr(context, userid)):
            return "Set PR first using using /setPR <PR number>"
         return bugzillaHelper.getReporter(BotCommands.get_pr(context, userid))
      except Exception as e:
         return str(e)

   @classmethod
   def bot_bugzilla_get_assignee(cls, botmessage, context):
      try:
         userid = botmessage.user.userid
         if (not BotCommands.check_pr(context, userid)):
            return "Set PR first using using /setPR <PR number>"
         bugzillaHelper = BugzillaHelper()
         return bugzillaHelper.getAssignee(BotCommands.get_pr(context, userid))
      except Exception as e:
         return str(e)

   @classmethod
   def bot_bugzilla_get_saved_search(cls, botmessage, context):
      try:
         userid = botmessage.user.userid
         if (not BotCommands.check_ldap_username(context, userid)):
            return "Set LDAP username first using /setLDAPUsername <LDAP username>"
         bugzillaHelper = BugzillaHelper()
         return bugzillaHelper.getSavedQueries(BotCommands.get_ldap_username(context, userid))
      except Exception as e:
         return str(e)

   @classmethod
   def bot_bugzilla_get_bug_list(cls, botmessage, context):
      try:
         userid = botmessage.user.userid
         if (not BotCommands.check_ldap_username(context, userid)):
            return "Set LDAP username first using /setLDAPUsername <LDAP username>"
         if (not BotCommands.check_saved_search(context, userid)):
            return "Set saved search first using /setSavedSearch <saved search name>"

         bugzillaHelper = BugzillaHelper()
         return bugzillaHelper.getBugList(BotCommands.get_ldap_username(context, userid),
                                          BotCommands.get_saved_search(context, userid))
      except Exception as e:
         return str(e)

   @classmethod
   def bot_bugzilla_get_description(cls, botmessage, context):
      try:
         userid = botmessage.user.userid
         if (not BotCommands.check_pr(context, userid)):
            return "Set PR first using using /setPR <PR number>"
         bugzillaHelper = BugzillaHelper()
         return bugzillaHelper.getUpdate0(BotCommands.get_pr(context, userid))
      except Exception as e:
         return str(e)

   @classmethod
   def bot_bugzilla_post_comment(cls, botmessage, context):
      try:
         userid = botmessage.user.userid
         if (not BotCommands.check_pr(context, userid)):
            return "Set PR first using using /setPR <PR number>"
         if (not BotCommands.check_comment(context, userid)):
            return "Set comment first using using /setComment <comment>"
 
         bugzillaHelper = BugzillaHelper()
         bugzillaHelper.addComment(BotCommands.get_pr(context, userid),
                                   BotCommands.get_comment(context, userid))
         return "Comment successfully posted."
      except Exception as e:
         return str(e)

   @classmethod
   def bot_coresummary_get_report(cls, botmessage, context):
      try:
         userid = botmessage.user.userid
         if (not BotCommands.check_pr(context, userid)):
            return "Set PR first using using /setPR <PR number>"
         if (not BotCommands.check_sb(context, userid)):
            return "Set support bundle first using using /setSB <SB name>"
 
         coreSummary = CoreSummary(BotCommands.get_pr(context, userid),
                                   BotCommands.get_sb(context, userid))
         return coreSummary.run_report()
      except Exception as e:
         return str(e)


   @classmethod
   def process_command(cls, botmessage, context):
      cmd = botmessage.command
      if BotCommands.is_valid_command(cmd):
         return BotCommands._commands[cmd]["callback"](botmessage, context)
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
      "help": "",
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
      "help": "search SB for a string. usage: /searchSB <PR number> <bundleID> <search string>",
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

BotCommands._commands.update({
   BotCommands.CORESUMMARY_GET_REPORT: {
      "authenticated": True,
      "admin": False,
      "subcommands": None,
      "callback": BotCommands.bot_coresummary_get_report,
      "help": "gets core summary for a support bundle. usage: /getCoreSummary <PR number> <bundle ID >",
      "args": False
   }})

BotCommands._commands.update({
   BotCommands.SET_SB: {
      "authenticated": True,
      "admin": False,
      "subcommands": None,
      "callback": BotCommands.bot_set_sb,
      "help": "sets SB. usage: /setSB <bundle ID >",
      "args": False
   }})

BotCommands._commands.update({
   BotCommands.SET_LDAP: {
      "authenticated": True,
      "admin": False,
      "subcommands": None,
      "callback": BotCommands.bot_set_ldap_username,
      "help": "sets LDAP username. usage: /setLDAPUsername <LDAP username>",
      "args": False
   }})

BotCommands._commands.update({
   BotCommands.SET_PR: {
      "authenticated": True,
      "admin": False,
      "subcommands": None,
      "callback": BotCommands.bot_set_pr,
      "help": "sets PR. usage: /setPR <PR number>",
      "args": False
   }})

BotCommands._commands.update({
   BotCommands.SET_SEARCH_KEYWORD: {
      "authenticated": True,
      "admin": False,
      "subcommands": None,
      "callback": BotCommands.bot_set_search_keyword,
      "help": "sets search keyword for Humbug. usage: /setKeyword <search keyword>",
      "args": False
   }})

BotCommands._commands.update({
   BotCommands.SET_COMMENT: {
      "authenticated": True,
      "admin": False,
      "subcommands": None,
      "callback": BotCommands.bot_set_comment,
      "help": "sets comment for Bugzilla. usage: /setComment <comment>",
      "args": False
   }})

BotCommands._commands.update({
   BotCommands.SET_SAVED_SEARCH: {
      "authenticated": True,
      "admin": False,
      "subcommands": None,
      "callback": BotCommands.bot_set_saved_search,
      "help": "sets saved search. usage: /setSavedSearch <saved search name>",
      "args": False
   }})
