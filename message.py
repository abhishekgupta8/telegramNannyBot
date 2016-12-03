import datetime
from user import User


class BotMessage(object):
   def __init__(self, botmessage, config):
      self.config = config
      self.message = botmessage  # entire message
      self.messagetext = botmessage.get('text', '')  # text portion of message
      self.messageid = botmessage.get('message_id', '')  # message id
      self.user = User(botmessage['from'], config)  # details about user who sent message

   #
   # return the first element of the message which is designated as the command
   # string
   #
   @property
   def command(self):
      return self.messagetext.split()[0]

   #
   # return subcommand if present else None. the first word after a command is
   # the subcommand
   #
   @property
   def subcommand(self):
      return self.messagetext.split()[1] if self.messagetext.split() > 2 else \
         None

   #
   # return message string after the command string. this comprises the
   # subcommands and args to the command
   #
   @property
   def args(self):
      return self.messagetext.split()[1:] if len(self.messagetext.split()) > 1 \
         else ""

   #
   # return date when the message was sent by the user
   #
   @property
   def date(self):
      return datetime.datetime.fromtimestamp(self.message['date']). \
         strftime('%Y-%m-%d %H:%M:%S')
