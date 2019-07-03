import pickle
import socket
import random
from _thread import *


#HOST = '10.130.18.128'
HOST = '127.0.0.1'
PORT = 8082

def randcoord():#generates a random valid coordinate within the gameboard
	return random.randint(-15, -5)*20

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT)) #assigning a particular port rather than a random one
no_players = 2 	
s.listen(no_players)

connection_list = []


# snakes = 	[
# 				[str(randcoord()), str(randcoord() )],
# 				[str(randcoord()), str(randcoord() )]
# 			]
snakes = [[randcoord() for _ in range(2)] for _ in range(no_players)]
print (snakes)

def threaded_client(conn, p_index):
	global connection_list	
	enemy_ID = 1
	if p_index == 1:
		enemy_ID = 0

	conn.send(bytes(str(p_index), "utf-8"))
	conn.recv(1024)

	toSend = pickle.dumps(snakes)
	conn.send(toSend)
	conn.recv(1024)
	
	# toSend = str(p_index) + " " + snakes[p_index][0] + " " + snakes[p_index][1]
	# conn.send(bytes(toSend, "utf-8"))
	# conn.recv(1024)

	while True:
		if len(connection_list) == 2:
			break

	# toSend = "enemy_cood: " + snakes[enemy_ID][0] + " " + snakes[enemy_ID][1]
	# conn.send(bytes(toSend, "utf-8"))
	# conn.recv(1024)

	while True:
		request = conn.recv(1024).decode("utf-8")
		if len(request) == 0:
			break
		# elif request == "msg_received":
		# 	continue
		# conn.send(bytes("msg_received", "utf-8"))

		print("request: " + request)
		player = "Player " + str(p_index)
		toSend = player + " " + request #untabbed

		print("sending:", toSend)
		for i in range(len(connection_list)):
			connection_list[i].send(bytes(toSend, "utf-8"))
			# connection_list[i].recv(1024)


i=0
while True:
	conn,address = s.accept()
	print('Connected to: ', address)
	connection_list.append(conn)

	start_new_thread(threaded_client, (conn, i,))
	print("only once")
	i += 1
	# if (lem(connection_list) == 2):
	# 	start_new_thread(threaded_client, (connection_list[0], 0,))
	# 	start_new_thread(threaded_client, (connection_list[1], 1,))


