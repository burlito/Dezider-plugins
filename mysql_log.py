from pyhole.core import plugin, utils
from xlc_libs import message as bMessage


class mysql_log(plugin.Plugin):
    def __init__(self, irc):
        self.irc = irc
        self.name = self.__class__.__name__
        self.disabled = False

        @plugin.hook_add_msg_regex(".*")
        def _mysql_logger(self, message, params=None, **kwargs):
            msg = bMessage(message)
            print "from:", msg.getSender()
            print "to:", msg.getRecipient()
            print "channel:", msg.getChannel()
            print "text:", msg.getText()