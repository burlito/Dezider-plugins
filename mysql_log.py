from pyhole.core import plugin, utils, log
from xlc_libs.message import message as bMessage
from xlc_libs.event import event as bEvent
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, func
from sqlalchemy import Integer, String, TIMESTAMP, TEXT, MetaData
from sqlalchemy.exc import OperationalError


class MysqlLogger(plugin.Plugin):
    def __init__(self, irc):
#        super(plugin.Plugin, self).__init__(irc)
        self.irc = irc
        self.name = self.__class__.__name__
        self.disabled = False
        self._connectToDatabase()

    def _connectToDatabase(self):
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
            'irc_chanlog', self.db_metadata,
            Column('ID', Integer, primary_key=True),
            Column('channel', String(14)),
            Column('sender', String(14), nullable=False),
            Column('sender_user', String(40)),
            Column('message', TEXT),
            Column(
                'timestamp',
                TIMESTAMP,
                nullable=False,
                default=func.now()
                )
        )
        self.db_chanevs = Table(
            'irc_chanevs', self.db_metadata,
            Column('ID', Integer, primary_key=True),
            Column('channel', String(14)),
            Column('sender', String(14), nullable=False),
            Column('sender_user', String(40)),
            Column('evtype', String(10)),
            Column(
                'timestamp',
                TIMESTAMP,
                nullable=False,
                default=func.now()
            )
        )
        try:
            self.db_conn = self.db_engine.connect()
        except OperationalError:
            print 'Nedalo sa mi pripojit sa do databazy'
            #FIXME: send warning to user/channel
        #FIXME: if table didn't exist call _installPlugin

    def _installPlugin(self):
        self.db_metadata.create_all(self.db_engine)

    @plugin.hook_add_command('MysqlLogRefresh')
    @utils.admin
    def refresh(self, message, params=None, **kwargs):
        """Reload configuration and recconect\
Database"""
        try:
            self.db_conn.close()
            message.dispatch('Database disconected.')
        except:
            message.dispatch('Can`t disconnect from database.')
            message.dispatch('Are you even connectet to one?')

        try:
            self._connectToDatabase()
            message.dispatch('Plugin refreshed')
        except:
            message.dispatch('Guess what. Something went wrong')

    @plugin.hook_add_chan_event('*')
    def event_logger(self, message, params=None, **kvargs):
        ev = bEvent(message)
        ins = self.db_chanevs.insert().values(
            channel=ev.getChannel(),
            sender=ev.getSender(),
            sender_user=ev.getSenderIdent(),
            evtype=ev.getType()
        )
        ins.compile().params
        try:
            self.db_conn.execute(ins)
        except Exception:
            log.get_logger().log('Could not execute SQL to db.')

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
        try:
            self.db_conn.execute(ins)
        except OperationalError:
            message.dispatch(
                'Mam nejake problemi z databazou, teraz chvilu neviem logovat\
 co pisete.'
            )
        except Exception:
            message.dispatch(
                'MysqlLogger je asi zle loadnuty. Niekto to resetnite.'
            )
