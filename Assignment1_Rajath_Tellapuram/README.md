How to run Client?
python3 udpTimestampClient.py [port number]

Functions:
createSocketToServer(PORT) - 
This creates a socket to the server using the socket API in Python.

getServerTime(sock, server_address) -
we use the sendto() UDP function to send data on the given IP and Port number. We try to improve the reliablility of the system by keeping a timeout of 5 seconds. This means, if the server doesn't respond to the client, the client resends the packet again after waiting for 5 seconds.
Time Format = We use a standard time so that we can communicate through the internet. We use utcnow() API, which takes our datetime value and normalizes it to a epoch value.
From the server we get the values of T2 and T1 with a comma seperated message.
We have now T0,T1,T2,T3 values.
We use these to calculate the following:
1. Latency
2. Standard Deviation
3. Offset
4. Delay
5. Error Bounds
6. Tnew - Estimated Server Time

How to run Server?
python3 udpTimestampServer.py [port number]
The value is send back to client using its address, the value is T1 and T2 in a comma seperated format. The server responds whenever it recives a data from the client.
It's always lisiting to the clients message.

