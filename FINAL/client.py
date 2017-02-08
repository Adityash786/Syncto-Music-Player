import socket
import os
import threading
import time

def recieve(sock,size = 100):
	size = int(size)
	data = ""
	while size > 0:
		#print "data = ",data
		r = sock.recv(size)
		data += r
		size -= len(r)
	return data

def changeLength(data,size):
	data = str(data)
	print "size = ",size," data ",data
	data = '0'*(size-len(data)) + data
	return data

def getPeerList():
	return ['127.0.0.1','172.16.14.208']

def findPeers():
	peers = []
	peerList = getPeerList()
	for host in peerList:
		s=socket.socket()
		port=12345
		names = []
		s.connect((host,port))

		size = recieve(s,3)
		print'size = ',size
		name = recieve(s,size)
		print 'name = ',name	

		peers.append((s,name))
	return peers


def sendToPeer(peerSocket,name,command,data):
	size = len(command)
	size = changeLength(size,3)
	print"Sending command to ",name
	peerSocket.sendall(size)
	peerSocket.sendall(command)
	size = os.path.getsize(command.split(' ')[1])
	print 'file size = ',size
	size = changeLength(size,10)
	print "size = ",size
	peerSocket.sendall(size)
	print'send size = ',len(data)
	peerSocket.sendall(data)

def sync(s):
	print "recieving time"
	s.sendall('F')
	size = recieve(s,3)

	val = recieve(s,int(size))
	print "Recieved ",val
	tm = time.time()
	print "sending ",repr(tm)
	s.sendall(changeLength(len(repr(tm)),3))
	s.sendall(repr(tm))


def connect():
	peers = findPeers()
	return peers
def control(command,peers):
	threadList = []
	s,n = peers[0]
	print s,n
	size = changeLength(len(command),3)
	if command.split(' ')[0] == 'play':
		print command
		print command.split(' ')[1]
		f = open(command.split(' ')[1],'rb')
		data = f.read()
		for s,n in peers:
			th = threading.Thread(target = sendToPeer,args = [s,n,command,data])
			th.start()
			threadList.append(th)
		print "Sending file to peers"
		for th in threadList:
			th.join()
		print "File sent"

		#synching all peers
		print "Synching clocks"
		for s,n in peers:
			#print "Syncing with ",n
			sync(s)
			#print "Sync done"
		print time.time()
		print "All done ! Playing after 3 seconds"


		playTime = time.time() + 5
		print "Play Time = ",repr(playTime)
		command = 'Play '+repr(playTime)
		#print "Command = ",command
		for s,n in peers:
			s.sendall(changeLength(len(command),3))
			s.sendall(command)

		print"curr Time = ",repr(time.time()), "Play Time = ",repr(playTime)

	elif command.split(' ')[0] == 'pause':
		for s,n in peers:
			s.sendall(size)
			s.sendall('pause')
	elif command.split(' ')[0] == 'unpause':
		for s,n in peers:
			s.sendall(size)
			s.sendall('unpause')
	elif command.split(' ')[0] == 'stop':
		for s,n in peers:
			s.sendall(size)
			s.sendall('stop')
	elif command.split(' ')[0] == 'exit':
		for s,n in peers:
			s.sendall(size)
			s.sendall("exit")
			s.close()
	else:
		print "Invalid Command"		



