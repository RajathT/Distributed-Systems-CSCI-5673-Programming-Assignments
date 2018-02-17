import socket
import sys
import datetime
import pytz

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

if int(sys.argv[1])<10000:
	raise e

# Bind the socket to the port
server_address = ('localhost', int(sys.argv[1]))

#print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)

while True:
    print('\nWaiting to receive message')
    data, address = sock.recvfrom(4096)
   
    #print('received {} bytes from {}'.format(data), address))
    #print(data)

    if data:
    	a = datetime.datetime.utcnow().replace(tzinfo=pytz.UTC)
    	b = str(a)
    	sent = sock.sendto(b.encode(), address)
    	print('sent {} bytes back to {}'.format(sent, address))