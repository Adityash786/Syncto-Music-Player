import socket
import pygame
import time

host="172.16.12.64"
port=12345

def recieve(serverSocket,size = 100):
	size = int(size)
	data = ""
	while size > 0:
		r = serverSocket.recv(size)
		data += r
		size -= len(r)
		print "Left = ",size
	return data


def changeLength(data,size):
	data = str(data)
	print "size = ",size," data ",data
	data = '0'*(size-len(data)) + data
	return data


def copyFile(client,name):
	size = recieve(client,10)
	print"File size = ",size,'name = ',name
	size = int(size)
	f = open(name,'wb')
	data = recieve(client,size)
	f.write(data)
	f.flush()
	f.close()

offset = 0
base = 0
def sync(client):
	global base,offset
	# waiting for sync permission
	#print "Waiting for sync"
	val = recieve(client,1)
	#print "Starting sync"
	timeStamp = time.time()
	#print "Sending time ",repr(timeStamp)
	#print "length  = ",len(repr(timeStamp))
	client.sendall(changeLength(len(repr(timeStamp)),3))
	client.sendall(repr(timeStamp))
	#print "Recieving time"
	size = recieve(client,3)
	val = recieve(client,int(size))
	#print "Recieved = ",repr(val)
	timeStamp2 = time.time()
	#print "Recieved at",repr(timeStamp2)
	base = timeStamp2
	rtt = timeStamp2 - timeStamp
	
	print "rtt = ",rtt
	
	offset = float(val) + rtt/2
	print "offset = ",repr(offset)

def getTime():
	global base,offset
	return time.time()-base + offset


def play(name,client):
	print "Copying file"
	copyFile(client,name)
	print "Copied file"

	# waiting for begining sync
	sync(client)
	print "Server Time = ",repr(getTime())


	print repr(getTime())
	size = recieve(client,3)
	command = recieve(client,int(size))
	print command
	if command.split(' ')[0] == 'Play':
		tm = command.split(' ')[1]
		print "Will play at",tm
		tm = float(tm)
		print "Waiting"
		while(getTime() < tm):
			pass
		#print"time = ",repr(getTime()), "currTime = ",repr(time.time())
		#print "playing"
		pygame.mixer.music.load(name)
		pygame.mixer.music.play(0)
	else:
		print 'Invalid command ',command



pygame.init()


serverSocket=socket.socket()



serverSocket.bind((host,port))
serverSocket.listen(5)

print 'Shubh naam ?'
hostName = raw_input()

size = changeLength(len(hostName),3)
print "name size = ",size
client,addr=serverSocket.accept()

client.sendall(size)
client.sendall(hostName)	
print 'Accepted connection from',addr

#print "Synching"
#sync(client)
#print getTime()



while True:
	size = recieve(client,3)
	print "recieved size ",size
	data = recieve(client,size)
	print "received ",data

	if data.split(' ')[0]=="play":
		play(data.split(' ')[1],client)  
	elif data.split(' ')[0]=="stop":
		pygame.mixer.music.stop()	
            
	elif data.split(' ')[0]=="pause":
		pygame.mixer.music.pause()
   	
	elif data.split(' ')[0]=="unpause":
		pygame.mixer.music.unpause()           
	
	elif data.split(' ')[0]=="exit":
		print "Hero gone, bye bye"
		break
