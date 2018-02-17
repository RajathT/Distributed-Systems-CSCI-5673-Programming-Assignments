import socket
import sys
import datetime
import pytz
import time

def getServerTime(sock, server_address):
	a = datetime.datetime.utcnow().replace(tzinfo=pytz.UTC)
	t0 = str(a)
	print('(T0): {!r}'.format(t0))
	sent = sock.sendto(t0.encode(), server_address)

	ts, server = sock.recvfrom(4096)
	print('(Ts): {!r}'.format(ts.decode()))

	a = datetime.datetime.utcnow().replace(tzinfo=pytz.UTC)
	t1 = str(a)
	print('(T1): {!r}'.format(t1))
	
	return t0,ts,t1

if __name__ == '__main__':
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	if int(sys.argv[1]) is None:
		raise e

	server_address = ('localhost', int(sys.argv[1]))
	timeframe=[]
	
	starttime=time.time()
	while (time.time()-starttime) < 120.0:
  		t0,ts,t1=getServerTime(sock,server_address)
  		tup = (t0,ts,t1)
  		timeframe.append(tup)
  		time.sleep(5.0 - ((time.time() - starttime) % 5.0))
	
	print(timeframe)

	sock.close()