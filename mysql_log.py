from pyhole.core import plugin, utils
from xlc_libs.message import message as bMessage

class MysqlLogger(plugin.Plugin):
#    def __init__(self, irc):
#        self.irc = irc
#        self.name = self.__class__.__name__
        
        @plugin.hook_add_command('ahoj')
        def ahoj(self, message, params=None, **kwargs):
            message.dispatch("no, cau")
        
        @plugin.hook_add_msg_regex('.*')
        def mysql_logger(self, message, params=None, **kwargs):
            print "hook zareagoval"
            msg = bMessage(message)
            print "from:", msg.getSender(), "EOL"
            print "to:", msg.getRecipient(), "EOL"
            print "channel:", msg.getChannel(), "EOL"
            print "text:", msg.getText(), "EOL"