from pyhole.core import plugin, utils
from xlc_libs.message import message as bMessage
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, func
from sqlalchemy import Integer, String, TIMESTAMP, TEXT, MetaData


class MysqlLogger(plugin.Plugin):
    def __init__(self, irc):
#        super(plugin.Plugin, self).__init__(irc)
        self.irc = irc
        self.name = self.__class__.__name__
        self.disabled = False
        try:
            self.config = utils.get_config("MysqlLogger")
            db_name = self.config.get("db_name")
            db_user = self.config.get("db_user")
            db_pass = self.config.get("db_password")
            db_host = self.config.get("db_host")
            try:
                db_type = self.config.get("db_type")
            except:
                db_type = "mysql"

        except Exception:
            print "Could not load MysqlLogger"
            #self.disabled = True
        #DbConnect
        self.db_engine = create_engine(
            '' + db_type + '://' + db_user + ':' + db_pass + '@' + db_host +
            '/' + db_name
        )
        self.db_metadata = MetaData()
        self.db_chanlog = Table(
            'chanlog', self.db_metadata,
            Column('ID', Integer, primary_key=True),
            Column('channel', String(14)),
            Column('sender', String(14), nullable=False),
            Column('sender_user', String(20)),
            Column('message', TEXT),
            Column(
                'timestamp',
                TIMESTAMP,
                nullable=False,
                default=func.now()
                )
        )
        #FIXME: add try, case block
        self.db_conn = self.db_engine.connect()
        #FIXME: if table didn't exist call _installPlugin

    def _installPlugin(self):
        self.db_metadata.create_all(self.db_engine)

    @plugin.hook_add_msg_regex('.*')
    def mysql_logger(self, message, params=None, **kwargs):
        msg = bMessage(message)
        ins = self.db_chanlog.insert().values(
            channel=msg.getChannel(),
            sender=msg.getSender(),
            sender_user=msg.getSenderIdent(),
            message=msg.getFullText()
        )
        ins.compile().params
        self.db_conn.execute(ins)
