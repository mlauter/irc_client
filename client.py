import socket
import asyncio
import sys

def translate(msg):
    cmd, *msg = msg.strip().split()

    if cmd == '/join':
        # not going to allow multiple joins for now
        channel = msg[0]
        if channel[0] != '#':
            raise Exception('channels must begin with #')
        if len(msg) == 2:
            password = msg[1]
            return 'JOIN ' + channel + ' ' + password + '\r\n'
        else:
            return 'JOIN ' + channel + '\r\n' 

    elif cmd == '/msg':
        target = msg[0]
        if len(msg) == 1:
            raise Exception("not enough arguments")
        else:
            return 'PRIVMSG ' + target + ' :' + ' '.join(msg[1:]) + '\r\n'

    elif cmd == '/leave':
        if len(msg) < 1:
            raise Exception("not enough arguments")
        else:
            return 'PART ' + ' '.join(msg) +'\r\n'
    elif cmd == '/whois':
        if len(msg) < 1:
            raise Exception("not enough arguments")
        else:
            return 'WHOIS ' + ' '.join(msg) +'\r\n'
    else:
        raise Exception("unknown command")

class IRCProtocol(asyncio.Protocol):

    def __init__(self,*args,**kwargs):
        self.buffer = ''
        super().__init__(*args,**kwargs)

    def connection_made(self, trans):
        self.trans = trans
        trans.write(str.encode('NICK cLannister \r\n'))
        trans.write(str.encode('USER cLannister 8 * :Cersei Lannister\r\n'))
        print("I connected")
        loop = asyncio.get_event_loop()
        loop.add_reader(sys.stdin, self.user_input)

    def user_input(self):
        user_msg = sys.stdin.readline()
        try:
            msg_to_send = translate(user_msg)
            self.trans.write(msg_to_send.encode())
        except Exception as e:
            print(e)

    def data_received(self, data):
        '''Add any new messages to the buffer. Split on new lines, pop all messages ending in newline off the buffer, return the remainder (incomplete message) to the buffer. If PING is found, respond PONG.'''
        self.buffer = self.buffer + data.decode()

        *lines, self.buffer = self.buffer.split('\r\n')

        for data in lines:
            data = data.strip()

            if data == '':
                continue
            print(data)

            if data.find('PING') != -1:
                self.trans.write(str.encode('PONG %s' % data[5:]))
                print('PONG %s' % data[5:])

    def connection_lost(self, exc):
        print("Connection lost!!")

loop = asyncio.get_event_loop()
coro = loop.create_connection(IRCProtocol, host="irc.freenode.net", port=6667)
loop.run_until_complete(coro)

try:
    loop.run_forever()
finally:
    loop.close()



