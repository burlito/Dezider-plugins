import re


class event(object):
    def __init__(self, event):
        #FIXME: event is expected to be irc.client.Event
        self._source = event
        self.channel = event.target
        self._fullIdent = event.source
        self._parse_nick()
        self._type = event.type
        self._parse_nick()

    def getChannel(self):
        reObj = re.match(r'([^\s]*).*', self.channel)
        try:
            return reObj.group(1)
        except:
            return ""

    def getSenderIdent(self):
        return self._senderIdent

    def getSender(self):
        return self.sender

    def getType(self):
        return self._type

    def _parse_nick(self):
        #FIXME: what if is \! in identity
        reObj = re.match(r'(.*)!(.*)', self._fullIdent)
        self.sender = reObj.group(1)
        self._senderIdent = reObj.group(2)
