import asyncio
import sys
import socket

s = socket.socket()
s.connect(('irc.freenode.net',6667))
s.send(str.encode('NICK funkymonkey\r\n'))
s.send(str.encode('USER funkymonkey 8 * :Funky Monkey\r\n'))

def coolkid():
    print(sys.stdin.readline())

def pingPong():
    msg = s.recv(4096).decode()
    lines = msg.split('\n')

    for data in lines:
        data = data.strip()

        if data == '':
            continue
        print(data)

        if data.find('PING') != -1:
            s.send(str.encode('PONG %s' % data[5:]))

loop = asyncio.get_event_loop()

loop.add_reader(sys.stdin,coolkid)

loop.add_reader(s,pingPong)

try:
    loop.run_forever()
finally:
    loop.close()