import socket
import sys
import datetime
import time
from matplotlib import pyplot as plt
import xlwt
import xlrd
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import numpy as np

def getServerTime(sock, server_address):
	a=datetime.datetime.utcnow().timestamp()
	t0 = str(a)
	sent = sock.sendto(t0.encode(), server_address)
	
	while True:
		try:
			sock.settimeout(5)
			ts, server = sock.recvfrom(4096)
			ts = ts.decode('utf-8')
			tempList = ts.split(',')
			t1 = tempList[0]
			t2 = tempList[1]
			if t1:
				break
		except socket.timeout:
			sent = sock.sendto(t0.encode(), server_address)
			print('Resending')
			
	a=datetime.datetime.utcnow().timestamp()
	t3 = str(a)
	return t0,t1,t2,t3

def createSocketToServer(PORT):
	timeframe=[]
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	server_address = ('localhost', int(PORT))

	starttime=time.time()
	while (time.time()-starttime) < 7200.0:
  		t0,t1,t2,t3=getServerTime(sock,server_address)
  		tup = (t0,t1,t2,t3)
  		timeframe.append(tup)
  		time.sleep(10.0 - ((time.time() - starttime) % 10.0))
	
	sock.close()

	return timeframe

def computeLatency(timeFrameList):
	latencyList = []
	for i,tup in enumerate (timeFrameList):
		latency = float(tup[3])-float(tup[0])
		latencyList.append(latency)
	return latencyList

def plotGraph(clockDifference,offset,delay):
	
	x_data = [x for x in range(len(clockDifference))]
	y_data = clockDifference
	plt.plot(x_data, y_data,marker='o', markerfacecolor='blue', markersize=5)

	plt.xlabel('#measurements')
	plt.ylabel('Difference')
	plt.title('Difference of Estimated Server Time and Local Clock')
	plt.savefig('./temp/ClockDifferenceaws-elra.png')
	plt.close()

	y_data = offset
	plt.plot(x_data, y_data,marker='o', markerfacecolor='blue', markersize=5,label='Offset')
	y_data = delay
	plt.plot(x_data, y_data,marker='o', markerfacecolor='green', markersize=5,label='Delay')
	plt.xlabel('#measurements')
	plt.ylabel('Offset and Delay')
	plt.title('Offset-Delay')
	plt.legend(loc=1)
	plt.savefig('./temp/OffsetDelayaws-elra.png')
	plt.close()


def standardDev(latencyList):
	averageLatency = sum(latencyList)/float(len(latencyList))
	standardDev = [x-averageLatency for x in latencyList]
	squaresofSD = [x**2 for x in standardDev]
	averageSD = sum(squaresofSD)/float(len(squaresofSD))
	rootavSD = averageSD ** (1/2)
	return averageLatency,rootavSD

def exportToExcel(timeframe,latencyList,mean,standardDev):
	book = xlwt.Workbook()
	sh = book.add_sheet('Test')
	for m,tup in enumerate(timeframe):
		sh.write(m,0,float(tup[0]))
		sh.write(m,1,float(tup[1]))
		sh.write(m,2,float(tup[2]))
		sh.write(m,3,float(tup[3]))

	for m, e1 in enumerate(latencyList):
	    sh.write(m, 4, e1)
	sh.write(m+1,4,mean)
	sh.write(m+1,5,standardDev)
	book.save('Local2.xls')

def calculateTmin(T3,T0,delay):
	Tmin = [(T3[x]-T0[x])/2 - delay for x in range(len(T0))]
	return Tmin

def ntpOffsetDelay(T0,T1,T2,T3):
	offsetList = [(T1[x] - T0[x] - (T3[x] - T2[x]))/2 for x in range(len(T0))]
	delayList = [T3[x]-T2[x] + T1[x]-T0[x] for x in range(len(T0))]
	#print(offsetList[0],delayList[0])
	
	return offsetList,delayList

def appendToExcel(offset,delay,clockDifference,Tn,Tmin):
	df = pd.DataFrame({'Tnew(Estimated)':Tn,'Clock Difference(T3 - Tnew)':clockDifference,'Offset(Oi)':offset,'Delay(Di)':delay,'Error Bound':Tmin})
	writer = ExcelWriter('./temp/temp.xls')
	df.to_excel(writer,'Test',index=False)
	writer.save()

def readFromExcel():
	filename = './temp/aws-elra.xls'
	df = pd.read_excel(filename)
	#print(df.columns)
	T0 = df['T0'].values
	T1 = df['T1'].values
	T2 = df['T2'].values
	T3 = df['T3'].values

	Tn = [(T1[x]+T2[x])/2 + (T3[x]-T0[x])/2 for x in range(len(T1))]

	clockDifference = [T3[x]-Tn[x] for x in range(len(T1))]

	offset,delay=ntpOffsetDelay(T0,T1,T2,T3)
	tmin = min(delay)/2
	Tmin = calculateTmin(T3,T0,tmin)
	appendToExcel(offset,delay,clockDifference,Tn,Tmin)
	plotGraph(clockDifference,offset,delay)


if __name__ == '__main__':
	
	if int(sys.argv[1]) is None:
		raise e

	timeframe = createSocketToServer(sys.argv[1])
	temp = computeLatency(timeframe)
	latencyList = [x*1000000 for x in temp]
	mean,standardDev = standardDev(latencyList)
	exportToExcel(timeframe,latencyList,mean,standardDev)
	
	#readFromExcel()

	

	
