from pyhole.core import plugin, utils
from xlc_libs.message import message as bMessage
from sqlalchemy import create_engine
from sqlalchemy import Table, Column
from sqlalchemy import Integer, String, Timestamp, MetaData

class MysqlLogger(plugin.Plugin):
    def __init__(self, irc):
#        super(plugin.Plugin, self).__init__(irc)
        self.irc = irc
        self.name = self.__class__.__name__
#        self.disabled = False
        try:
            self.config = utils.get_config("MysqlLogger")
            db_name = self.config.get("db_name")
            db_user = self.config.get("db_user")
            db_pass = self.config.get("db_password")
            db_host = self.config.get("db_host")
            try:
                #FIXME: not implemented
                db_type = self.config.get("db_type")
            except:
                db_type = "mysql"

        except Exception:
            print "Could not load MysqlLogger"
            #self.disabled = True
        #DbConnect
        #FIXME: add try, case block
        self.db_engine = create_engine(
            '' + db_type + '://' + db_user + ':' + db_pass + '@' + db_host +
            '/' + db_name
        )
        self.db_metadata = MetaData()
        self.db_chanlog = Table(
            'chanlog', self.db_metadata,
            Column('ID', Integer, primary_key=True),
            Column('sender', String),
            Column('sender_user', String),
            Column('message', String),
            Column('timestamp', Timestamp)
        )
        #FIXME: if table didn't exist call _installPlugin

    def _installPlugin(self):
        self.db_metadata.create_all(self.db_engine)

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
