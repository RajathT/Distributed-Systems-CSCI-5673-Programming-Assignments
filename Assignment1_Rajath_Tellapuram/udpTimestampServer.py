import socket
import sys
import datetime
import time

def sendServerTime():
	while True:
		data, address = sock.recvfrom(4096)
		if data:
			a=datetime.datetime.utcnow().timestamp()
			b = str(a)
			message = b + ','
			a=datetime.datetime.utcnow().timestamp()
			b = str(a)
			message = message + b
			sent = sock.sendto(message.encode('utf-8'), address)

if __name__ == '__main__':
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	if int(sys.argv[1]) is None:
		raise e

	server_address = ('localhost', int(sys.argv[1]))
	sock.bind(server_address)
	sendServerTime()
	sock.close()
