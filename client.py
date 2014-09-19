import socket
import asyncio
import sys

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
        user_msg = sys.stdin.readline() + '\r\n'
        self.trans.write(user_msg.encode())

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

    def connection_lost(self, exc):
        print("Connection lost!!")


# class IRCClient(object):

#     def __init__(self):
#         self.get_connect_info()
#         self.port = 6667
#         self.socket = socket.socket()

#         self.socket.connect((self.host, self.port))
#         #password?
#         self.socket.send(str.encode('NICK %s \r\n' % self.nickname))
#         self.socket.send(str.encode('USER %(nick)s 8 * :%(real)s\r\n'% {'nick':self.nickname,'real':self.realname}))


#     def pingPong(self):
        
#             msg = self.socket.recv(4096).decode()
#             lines = msg.split('\n')

#             for data in lines:
#                 data = data.strip()

#                 if data == '':
#                     continue
#                 print(data)

#                 if data.find('PING') != -1:
#                     self.socket.send(str.encode('PONG %s' % data[5:]))

#     def get_connect_info(self):
#         self.host = input("Enter the server to connect to\n")
#         connected = False
#         self.nickname = input("Enter your nickname\n")
#         self.realname = input("Enter your real name\n")



loop = asyncio.get_event_loop()
coro = loop.create_connection(IRCProtocol, host="irc.freenode.net", port=6667)
loop.run_until_complete(coro)
# loop.create_connection(IRCProtocol, host="localhost", port=1234)

try:
    loop.run_forever()
finally:
    loop.close()

# IRCClient()


