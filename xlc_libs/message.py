import re

class message():
    def __init__(self, message):
        self._source = message
        self.channel = message.target
        self._fullMessage = message._message
        self._parse_msg()
        self._fullIdent = message.source
        self._parse_nick()
        
    def getChannel(self):
        print self.channel
        
    def getSender(self):
        return self.sender
    
    def getRecipient(self):
        return self.recipient
        
    def getText(self):
        return self.text
        
    def _parse_msg(self):
        #FIXME: unit test needed
        reObj = re.match(r'[\s]*([0-9A-Za-z_-~]{0,9})[\s]*:[\s]*(.*)', self._fullMessage)
        if reObj:
            self.recipient = reObj.group(1)
            self.text = reObj.group(2)
        else:
            self.recipient = ""
            self.text = self._fullMessage

    def _parse_nick(self):
        reObj = re.match(r'([.]{0,9})!.*') #FIXME: what if is \! in identity
        self.sender = reObj.group(1)