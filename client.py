import socket
import asyncio

class IRCClient(object):
    host = input("Enter the server to connect to\n")
    port = 6667
    connected = False
    nickname = input("Enter your nickname\n")
    realname = input("Enter your real name\n")

    def __init__(self):
        self.socket = socket.socket()
        self.socket.connect((self.host, self.port))
        #password?
        self.socket.send(str.encode('NICK %s \r\n' % self.nickname))
        self.socket.send(str.encode('USER %(nick)s 8 * :%(real)s\r\n'% {'nick':self.nickname,'real':self.realname}))
        
        while True:
            msg = self.socket.recv(4096).decode()
            lines = msg.split('\n')

            for data in lines:
                data = str(data).strip()

                if data == '':
                    continue
                print(data)

                if data.find('PING') != -1:
                    self.socket.send(str.encode('PONG %s' % data[5:]))



IRCClient()



