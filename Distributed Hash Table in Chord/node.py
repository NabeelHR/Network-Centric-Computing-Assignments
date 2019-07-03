import socket
import time
from _thread import *
import os
import hashlib
import pickle

grand_successor = None
predecessor = None
my_port = None
file_directory = {}
host = '127.0.0.1'
finger_table = []
termination_flag = False #all threads will check on this to when the node is being terminated

def node_topology():
	global finger_table, predecessor, my_port, grand_successor
	print("Topology: ", predecessor, my_port, finger_table[0][1], "->", grand_successor)

def show(table): # printing finger table
	print("fingy table")
	node_topology()
	for element in table:
		print( "  |\t", element[0], "\t-\t", hashed_value(element[1]), " (", (element[1]), ")\t|")

def hashed_value(key):
	key = str(key)
	hash_object = hashlib.sha256(key.encode("utf-8"))
	return int(hash_object.hexdigest(), 29) % 1024


def value_in_between(a, b, c):
	a, c = hashed_value(a), hashed_value(c)
	if c <= a:
		c += 1024
	if b <= a:
		b += 1024
	if b > a and b < c:
		return True
	else:
		return False

# def is_succeeding(a, b):
# 	if a < b:
# 		a += 1024
# 	return a
def update_file_directory():
	global my_port, finger_table, file_directory
	file_directory = {key: val for key, val in file_directory.items() if value_in_between(predecessor, val, my_port)}

##########function to retrieve a specific file 
def RetrFile(conn):
	filename = conn.recv(1024).decode("utf-8")
	print("client wants to retrieve ", filename)
	path = "./database/" + filename
	if os.path.isfile(path):
		filesize = os.path.getsize(path)
		conn.send(bytes("FILE EXISTS " + str(filesize), "utf-8") )
		reply = conn.recv(1024).decode("utf-8")
		if reply[:2] == 'OK':
			f = open(path, 'rb')
			toSend = f.read(1024)
			conn.send(toSend)
			totalsend = len(toSend)
			while totalsend < filesize:
				toSend = f.read(1024)
				conn.send(toSend)
				totalsend += len(toSend)
			conn.close()
		else:
			print("your code shouldnt ever be here tbh")
	else:
		print("Error")
		conn.send(bytes("ERR file not found, this is a bug", "utf-8"))
	conn.close()
##############function to receive each specific file from predecessor
def RecvFile(s, filename):
	s.send(bytes(filename, "utf-8"))
	data = s.recv(1024).decode("utf-8")
	if data[:11] == "FILE EXISTS":
		filesize = int(data[12:])
		print ("File exists, now sending it")
		s.send(bytes("OK", "utf-8"))
		completeName = os.path.join("./database", filename)
		f = open(completeName, "wb")
		data = s.recv(1024)
		totalrecv = len(data)
		f.write(data)
		print("Downloading ", filename, "...")
		while totalrecv < filesize:
			data = s.recv(1024)
			totalrecv += len(data)
			f.write(data)
#			print ( totalrecv * 100 / filesize, "%% complete")
		print ("Download complete")
	else:
		print(data, "ERRORR file does not exist")

#fetches successor of key from given port by iteratively pinging nodes
def fetch_successor(port, entry):
	global host
	response = "_"
	while response != "YES":
		if response != "_":	
			print(port, entry, "sun luu")	
			print (response, len(response))
			port = int(response.split(" ")[2])
			s.close()
		if port == my_port:
			break
		s = socket.socket()
		s.connect((host, port))
		s.send(bytes("Do_u_hav_key?", "utf-8"))
		s.recv(1024).decode("utf-8")
		s.send(bytes(entry, "utf-8"))
		response = s.recv(1024).decode("utf-8")
	s.close()
	return port

def run_client():
	global host
	port = int(input("Enter port number you wish to connect to: "))
	choice = input("Enter name of file you wish to retrieve or Q/q to quit: ")
	while choice != "q" and choice != "Q":
		port = fetch_successor(port, str(hashed_value(choice)))

		s = socket.socket()
		s.connect((host, port))
		s.send(bytes("send_file_pls", "utf-8"))
		s.recv(1024)
		RecvFile(s, choice)
		s.close()
		choice = input("Enter name of file you wish to retrieve or Q/q to quit: ")

def stabilize_table():
	global my_port, predecessor, finger_table, host, termination_flag
	while True:
		for i, entry in enumerate(finger_table):
			print("REMINDER --->>> You can enter Quit/Q/q to remove this node from DHT")
			time.sleep(1)
			if termination_flag:
				return 
			s = socket.socket()
			try:
				s.connect((host, entry[1]))
				s.send(bytes("whoz_ur_daddy", "utf-8"))
				resp = int(s.recv(1024).decode("utf-8"))
				s.close()
				if resp == my_port:
					if value_in_between(entry[1], entry[0], my_port) and resp != entry[1]:
#						print("time to update fingy table")
						finger_table[i][1] = resp
				elif value_in_between(my_port, entry[0] ,resp):
#					print("time to update fingy table")
					finger_table[i][1] = resp
			except:
				print("Node", entry[1], " at value ", entry[0], " has been terminated")
				finger_table[i][1] = finger_table[(i+2)%10][1]
				try:
					s.connect((host, finger_table[(i+2)%10][1]))
					s.send(bytes("ping", "utf-8"))
					s.recv(1024)
					s.close()
				except:
					finger_table[i][1] = finger_table[(i+7)%10][1]

		node_topology()
		print ("** ** ** ** ** ** **")
		print(file_directory)
		show(finger_table)
		time.sleep(10)

def ping_successor():
	global grand_successor, finger_table, host, my_port
	time.sleep(4)
	while termination_flag == False:
		time.sleep(1)
		try:
#			print("_________%$%#^#$^&&&___________", host, finger_table[0][1])
#			show(finger_table)
			s = socket.socket()
			s.connect((host, finger_table[0][1]))
			# print("________________connection made to successor")
			s.send(bytes("ping " + str(my_port), "utf-8"))
			grand_successor = int(s.recv(1024).decode("utf-8"))
			# print("_________grand successor updateddd____")
			s.close()
		except:
			print("_ _ _ _ _ _UPDATINGG  G G G successor to grand successor _ _ ___ _")
			finger_table[0][1] = grand_successor

def node_termination():
	global my_port, host, file_directory, predecessor, finger_table, termination_flag
	print("you entered: ", input("Press any key to exit node"), "\nSetting flag to true so thread terminating")
	termination_flag = True
	
	if my_port == predecessor and my_port == finger_table[0][1]:
		print("dude exit already")
		os._exit(1)

	s = socket.socket()
	s.connect((host, finger_table[0][1]))
	s.send(bytes("exiting, update predecessor " + str(predecessor) + " " + str(my_port), "utf-8"))
	toSend = []
	for key, _ in file_directory.items():
		toSend.append(key)
	toSend = pickle.dumps(toSend)
	s.recv(1024)
	s.send(toSend)
	s.close()

	s = socket.socket()
	s.connect((host, predecessor))
	s.send(bytes("exiting, update successor " + str(finger_table[0][1]), "utf-8"))
	s.recv(1024)
	s.close()

	print("......... exiting ... in 10 seconds")
	time.sleep(5)
	print("......... exiting ... in 5 seconds")
	time.sleep(2)
	print("......... exiting ... in 3 seconds")
	time.sleep(1)
	print("......... exiting ... in 2 seconds")
	time.sleep(1)
	print("......... exiting ... in 1 second")
	time.sleep(1)
	os._exit(1)

def threaded_client(conn):
	global predecessor, my_port, file_directory, finger_table
	role = conn.recv(1024).decode("utf-8").split(" ")
	# node_topology()
	if role[0] == "new_node":
		print("new node connected with ID: ", role[1])
		new_node = int(role[1])
		print (hashed_value(predecessor), hashed_value(new_node), hashed_value(my_port))
		if value_in_between(predecessor, hashed_value(new_node), my_port) == True:
			toSend = []
			for key, value in file_directory.items():
				if value_in_between(predecessor, value, new_node):
					toSend.append(key)

			conn.send(bytes("I_will_be_your_successor", "utf-8"))
			conn.recv(1024).decode("utf-8")
			conn.send(bytes(str(predecessor), "utf-8"))
			predecessor = int(role[1])
			conn.recv(1024)
			toSend = pickle.dumps(toSend)
			conn.send(toSend)
		else:
			conn.send(bytes("I_aint_your_mama, lookup " + str(finger_table[0][1]), "utf-8"))
		conn.close()
	elif role[0] == "hello_im_your_new_successor":
		finger_table[0][1] = int(role[1]) #updating successor
		conn.close()
	elif role[0] == "send_file_pls":
		conn.send(bytes("coolbro_ok", "utf-8"))
		RetrFile(conn)
	elif role[0] == "Do_u_hav_key?":
		conn.send(bytes("send_keyvalue_pls", "utf-8"))
		key = int(conn.recv(1024).decode("utf-8"))
		if value_in_between(predecessor, key, my_port):
			conn.send(bytes("YES", "utf-8"))
		elif value_in_between(my_port, key, finger_table[0][1]):
			print("line 190: ", hashed_value(predecessor), " ", hashed_value(key), " ", hashed_value(my_port))
			toSend = "Nope, lookup " + str(finger_table[0][1])
			conn.send(bytes(toSend, "utf-8"))
		else:
			print("NOPE Me don't have le key, forwarding through a chord in O(log n)")
			for entry in reversed(finger_table):
				if value_in_between(entry[1], key, my_port):
					conn.send(bytes("Nope, lookup " + str(entry[1]), "utf-8"))
					break
		conn.close()
	elif role[0] == "whoz_ur_daddy":
		conn.send(bytes(str(predecessor), "utf-8"))
		conn.close()
	elif role[0] == "exiting,":
		if role[2] == "successor":
			finger_table[0][1] = int(role[3])
			conn.send(bytes("coolio I gotcha", "utf-8"))
			conn.close()
		else: #update predecessor instead
			conn.send(bytes("coolio but send files", "utf-8"))
		
			filenames = conn.recv(4096)
			filenames = pickle.loads(filenames)
			print ("files received from deleted node: ")
			print (filenames)

			conn.close()
			for file in filenames:
				s = socket.socket()
				s.connect((host, int(role[4])))
				s.send(bytes("send_file_pls", "utf-8"))
				s.recv(1024)
				RecvFile(s, file)
				s.close()

			predecessor = int(role[3])
			for filename in filenames:
				file_directory[filename] = hashed_value(filename)

	elif role[0] == "ping":
		if len(role) > 1:
			predecessor = int(role[1])
		conn.send(bytes(str(finger_table[0][1]), "utf-8"))
		conn.close()
	else:
		print("WEIRD REQUEST bro u shouldn't be here!! wat are you even saying?")
		print(role)
#	print("after processing query")
	# node_topology()
		
def connect_to_DHT(my_port):
	global predecessor, host, finger_table
	# host = '127.0.0.1'
	s = socket.socket()
	connection, peer_port = None, None

	while connection != True:
		try:
			peer_port = int(input('Enter port number of peer you wish to connect to: '))
			s.connect((host, peer_port))
			connection = 1
		except:
			print("Port invalid, re enter pls")

	toSend = "new_node " + str(my_port)
	s.send(bytes(toSend, "utf-8"))
	response = s.recv(1024).decode("utf-8")
	print ("check 3")
	while response != "I_will_be_your_successor": ##repeat until someoene allows you to fix in
		print(response)
		response = response.split(" ")
		peer_port = int(response[2])
		s.close()
		s = socket.socket()
		s.connect((host, peer_port))
		s.send(bytes(toSend, "utf-8"))
		response = s.recv(1024).decode("utf-8")

	s.send(bytes("Okay, pls send my predecessor", "utf-8"))
	finger_table[0][1] = peer_port
	predecessor = int(s.recv(1024).decode("utf-8"))


	s.send(bytes("Pls send me my file names", "utf-8"))
	filenames = s.recv(4096)
	filenames = pickle.loads(filenames)
	print ("files received: ")
	print (filenames)
	s.close()
	############# notifying predecessor
	s = socket.socket()
	s.connect((host, predecessor))
	s.send(bytes("hello_im_your_new_successor " + str(my_port), "utf-8"))
	s.close()
	###receiving files
	for file in filenames:
		s = socket.socket()
		s.connect((host, finger_table[0][1]))
		s.send(bytes("send_file_pls", "utf-8"))
		s.recv(1024)
		RecvFile(s, file)
		s.close()

	############# updating finger table
	# port  = successor
	for i, entry in enumerate(finger_table):
		ans = fetch_successor(finger_table[0][1], str(entry[0]))
#		print(ans)
		finger_table[i][1] = ans

def Main():
	global predecessor, host, my_port, file_directory, finger_table


	my_port = int(input("Enter port number that you wish to use: "))
	print("This is node ", my_port, " with hashed_value of ", hashed_value(my_port) )
	for i in range(10): # initializing finger table
		finger_table.append([ (hashed_value(my_port) + 2 ** i) % 1024 , my_port])

	show(finger_table)
	predecessor = my_port

	if os.path.isdir('./database') == False:
		os.mkdir('./database')
		print("Database initialized!")

	choice = input('Press 1 to connect as a client, press 2 to join DHT, or enter anything else to initialize DHT ')
	if choice == "1":
		run_client()
		return
	elif choice == "2":
		print ("connecting...\n")
		connect_to_DHT(my_port)

	show(finger_table)

	for _, _, files in os.walk("./database"):
		for filename in files:
			file_directory[filename] = hashed_value(filename)
	print(file_directory)

	s = socket.socket()
	s.bind((host, my_port))
	s.listen(5)
	print("Server listening yo")

	start_new_thread(stabilize_table, ())
	start_new_thread(ping_successor, ())
	start_new_thread(node_termination, ())
	while True:
		update_file_directory()
		c, addr = s.accept()
		print ("client connects! with IP ", str(addr))
		start_new_thread(threaded_client, (c,))


	s.close()


if __name__ == '__main__':
	Main()







