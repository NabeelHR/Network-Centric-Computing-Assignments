import pickle
import socket
import turtle
import time
import random
from _thread import *

#server_ip = '10.130.18.128'
server_ip = '127.0.0.1'
server_port = 8082
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((server_ip, server_port))

delay = 0.14

window = turtle.Screen()
window.tracer(0)
snakehead = turtle.Turtle()
enemyhead = turtle.Turtle()

# apple = turtle.Turtle()
# apple_cood = ""
enemy_xy = []
you_won = False
text = turtle.Turtle()
text.speed(0)
text.ht()
window.tracer(1)
snaketail = []
checker_dualpress = True
player_num = None
turns = ""
my_turns = ""
# def randcoord():#generates a random valid coordinate within the gameboard
# 	return random.randint(-15, 15)*20
my_coods = ""
enemy_cood = ""
def createscreen():
	# global apple_cood
	# global enemy_cood
	global player_num
	window.title("PLS krlo yar kaam")
	window.bgcolor("light green")
	window.setup(width=700, height=700)
	window.tracer(0)#turns off screen updates

	grid = turtle.Turtle()
	grid.color('black')
	grid.pensize(8)
	grid.turtlesize(0.4)
	grid.pensize(12)
	grid.penup()
	grid.shape('square')
	turtle.tracer(False)
	grid.goto(-315, 315)
	grid.pendown()
	grid.setx(grid.xcor() + 630)
	grid.sety(grid.ycor() - 630)
	grid.setx(grid.xcor() - 630)
	grid.sety(grid.ycor() + 630)
	grid.pensize(1)
	for i in range(-290, 300, 20):
		grid.penup()
		grid.goto(-315, i)
		grid.pendown()
		grid.setx(grid.xcor() + 630)
	for i in range(-290, 300, 20):
		grid.penup()
		grid.goto(i, 315)
		grid.pendown()
		grid.sety(grid.ycor() - 630)

	snakehead.turtlesize(1)
	snakehead.speed(0)
	snakehead.shape("circle")
	snakehead.color("black")
	snakehead.penup()
	snakehead.pensize(2)

	enemyhead.turtlesize(1)
	enemyhead.speed(0)
	enemyhead.shape("circle")
	enemyhead.color("purple")
	enemyhead.penup()
	enemyhead.pensize(2)

	player_num = int(s.recv(1024).decode("utf-8"))
	s.send(bytes("msg_received", "utf-8"))
	print (player_num)

	snek_cood = s.recv(4096)
	snek_cood = pickle.loads(snek_cood)

	print(snek_cood)
	s.send(bytes("sneks received", "utf-8"))
	

	snakehead.goto(snek_cood[player_num], snek_cood[player_num])
	snakehead.direction = 'up'

	# enemy_cood = s.recv(1024).decode("utf-8")
	# enemy_cood = enemy_cood.split(" ")
	# print(enemy_cood)
	# if enemy_cood[0] != "enemy_cood:":
	# 	print("AINT BE HAPPENIN")
	# 	return
	# s.send(bytes("enemy received", "utf-8"))

	for i in range(player_num):
		if i != player_num:
			# print(i)
			enemyhead.goto(snek_cood[i][0], snek_cood[i][1])
			# print("bro what")

	enemyhead.direction = 'up'
	print("bro what")
	# apple.penup()
	# apple.speed(0)
	# apple.turtlesize(.85)
	# apple.shape("circle")
	# apple.color("red")
#	turtle.tracer(1)

	# apple_cood = s.recv(1024).decode("utf-8")
	# apple_cood = apple_cood.split(" ")
	# print(apple_cood)
	# if apple_cood[0] != "apple_cood:":
	# 	print("AINT BE HAPPENIN")
	# 	return
	# s.send(bytes("apple received", "utf-8"))
	

	# apple.goto(int(apple_cood[1]), int(apple_cood[2]))



def go_up():
	global my_turns
	if(snakehead.direction is not "down" and snakehead.direction is not "up"):
		snakehead.direction = "up"
		my_turns = "up"
		# s.send(bytes("going_up", "utf-8"))
		# print("datafor up down should be sent by now")
def go_down():
	global my_turns
	if(snakehead.direction is not "up" and snakehead.direction is not "down"):
		snakehead.direction = "down"
		my_turns = "down"
		print(my_turns)
		# s.send(bytes("going_down", "utf-8"))
		# print("datafor boi down should be sent by now")
def go_left():
	global my_turns
	if(snakehead.direction is not "right" and snakehead.direction is not "left"):
		snakehead.direction = "left"
		my_turns = "left"
		print(my_turns)
		# s.send(bytes("going_left", "utf-8"))
		# print("datafor left down should be sent by now")
def go_right():
	global my_turns
	if(snakehead.direction is not "left" and snakehead.direction is not "right"):
		snakehead.direction = "right"
		my_turns = "right"
		print(my_turns)
		# s.send(bytes("going_right", "utf-8"))
		# print("datafor right down should be sent by now")
qut = True
def quit():
	global qut
	qut = False
	print ("screen should exit nows")

def enemy_up(enemy_turt):
		enemy_turt.direction = "up"
def enemy_down(enemy_turt):
		enemy_turt.direction = "down"
def enemy_left(enemy_turt):
		enemy_turt.direction = "left"
def enemy_right(enemy_turt):
		enemy_turt.direction = "right"


def move(turt):
	if turt.direction == 'up':
		turt.sety(turt.ycor() + 20)
	elif turt.direction == 'down':
		turt.sety(turt.ycor() - 20)
	elif turt.direction == 'right':
		turt.setx(turt.xcor() + 20)
	elif turt.direction == 'left':
		turt.setx(turt.xcor() - 20)

def create_segment():
	window.tracer(0)
	new_segment = turtle.Turtle()
	new_segment.turtlesize(0.7)
	new_segment.speed(0)
	new_segment.penup()
	new_segment.shape("square")
	new_segment.color("grey")
	window.tracer(1)
	return new_segment
def checkCollision():
	if (snakehead.xcor()<-300 or snakehead.xcor()>300 or snakehead.ycor()>300 or snakehead.ycor()<-300):
		return True
	for seg in snaketail:
		if seg.distance(snakehead) < 20:
			return True
	if snakehead.distance(enemyhead) <10:
		return True
	return False
# bool debugg = True
text.clear()
text.write("Waiting for server to connect all clients", move=False, align="center", font=("Arial", 14, "bold"))

createscreen()
#keyboard bindings
window.listen()
window.onkeypress(go_up, "w")
window.onkeypress(go_left, "a")
window.onkeypress(go_down, "s")
window.onkeypress(go_right, "d")
window.onkeypress(quit, "q")

#Ainwein ka shugal
text.penup()
text.goto(0, 325)
text.write("starting game in 3 seconds", move=False, align="center", font=("Arial", 14, "bold"))
time.sleep(delay*8)
text.clear()
text.write("starting game in 2 seconds", move=False, align="center", font=("Arial", 14, "bold"))
time.sleep(delay*8)
text.clear()
text.write("starting game in 1 second", move=False, align="center", font=("Arial", 14, "bold"))
time.sleep(delay*8)
text.clear()
def check_enemy_moves():
	global you_won
	global turns
	global enemy_xy
	global enemyhead
	print (turns)
	if turns != "":
		enemyhead.goto(int(enemy_xy[0]), int(enemy_xy[1]) )
		# enemyhead.sety(int(enemy_xy[1]))
		if turns == "up":
			enemy_up(enemyhead)
		elif turns == "down":
			enemy_down(enemyhead)
		elif turns == "left":
			enemy_left(enemyhead)
		elif turns == "right":
			enemy_right(enemyhead)
		elif turns == "terminate":
			enemyhead.goto(10000, 10000)
			you_won = True

		turns = ""

def await_outbox(s):
	global my_turns
	# global
	while True:
		time.sleep(0.08)
		if my_turns != "":
			s.send(bytes(my_turns + " " + my_coods, "utf-8"))
			print ("data sent for sgoing ", my_turns)
			my_turns = ""

def await_msg(s):
	global you_won
	# global apple
	# global apple_cood
	global enemy_xy
	global turns
	while True:
		if my_turns == "terminate" or you_won == True:
			break
		msg_from_server = s.recv(1024).decode("utf-8")
		msg_from_server = msg_from_server.split(" ")
		print (msg_from_server)

		if msg_from_server[0] == "Player":
			print("coolio")
			if msg_from_server[1] != player_num:
				turns = msg_from_server[2]
				print ("enemy turninnnng ", turns)
				enemy_xy = [msg_from_server[3], msg_from_server[4]]
#		elif


score = 0
#snaketail.append(create_segment())
text.clear()
text.write("Score is " + str(score), move=False, align="center", font=("Arial", 14, "bold"))
start_new_thread(await_msg, (s,))
#start_new_thread(await_outbox, (s,))
#main game loop
while True:
	time.sleep(delay)
	if checkCollision() is True:
		text.clear()
		text.write("LOSER, exitin game", move=False, align="center", font=("Arial", 14, "bold"))
		my_turns = "terminate"
		s.send(bytes(my_turns + " " + my_coods, "utf-8"))
		time.sleep(3)
		# s.shutdown(socket.SHUT_WR)
		# s.close()
		break
	elif you_won == True:
		text.clear()
		text.write("YOU won, game exiting", move=False, align="center", font=("Arial", 14, "bold"))
		time.sleep(3)
		break


	for i in range(len(snaketail)-1, 0, -1):
		x = snaketail[i-1].xcor()
		y = snaketail[i-1].ycor()
		snaketail[i].goto(x, y)

	if (len(snaketail) > 0):
		x = snakehead.xcor()
		y = snakehead.ycor()
		snaketail[0].goto(x, y)


	move(snakehead)
	my_coods = str(snakehead.xcor()) + " " + str(snakehead.ycor())
	if my_turns != "":
		s.send(bytes(my_turns + " " + my_coods, "utf-8"))
		print ("data sent for sgoing ", my_turns)
		my_turns = ""

	check_enemy_moves()
	move(enemyhead)


# text.clear()
# text.write("Enter q to quit", move=False, align="center", font=("Arial", 14, "bold"))

# while qut == True:
# 	1
