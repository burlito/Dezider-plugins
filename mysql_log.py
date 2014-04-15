from pyhwole.core import plugin, utils
from xlc_libs.message import message as bMessage


class MysqlLogger(plugin.Plugin):
    def __init__(self, irc):
        self.irc = irc
        self.name = self.__class__.__name__
        try:
            self.config = utils.get_config("MysqlLogger")
            self.db_name = self.config.get("db_name")
            self.db_user = self.config.get("db_user")
            self.db_pass = self.config.get("db_password")
            try:
                self.db_type = self.config.get("db_type")
            except:
                self.db_type = "mysql"

        except Exception:
            print "Could not load MysqlLogger"
            self.disabled = True

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
