import socket
import signal
import sys
import json
import time

from motor_ctrl import StepperMotor

class Server:

	#a msg will be stored here for the handler to read
	msg_buf = None
	server_socket = None

	def store_msg(msg):
		msg_buf = msg

	def read_msg(self):
		return self.msg_buf

	def init_server(self):

		#server config
		HOST = "0.0.0.0"
		PORT = 8080

		#creating socket here
		self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		print("\nSocket created")

		#binding the socket to the port
		self.server_socket.bind((HOST, PORT))


	#to handle shutdown
#	def shutdown_server(sig, frame):
#		server_socket.close()
#		sys.exit(0)

	def run_server(self):


		#setting signal interrupt in order shutdown the server
#		signal.signal(signal.SIGINT, self.shutdown_server)


		#Listen for 1 client
		print("\nlistening for connection")
		self.server_socket.listen(1)

		motor = StepperMotor()


		while True:
			#poll for client
			print("\npolling for client")
			client_socket, client_address = self.server_socket.accept()
			while True:
				#recieve from client
				data = client_socket.recv(1024).decode("utf-8")

				if not data:
					print("Client Disconnected")

				print(f"Recieved: {data}")

				try:
					command = json.loads(data) #parse json

					#handle winch command
					if "winch_speed" in command:
						winch_speed = command["winch_speed"]
						motor.set_dir(winch_speed > 0)
						motor.step(200, 0.0002)
						print(f"Setting winch speed: {winch_speed}")
						#todo  make modular

					elif "stop" in command:
						motor.stop_step()
						print("stopping motor")

					client_socket.sendall("OK".encode("utf-8"))

				except json.JSONDecodeError:
					client_socket.sendall("Invalid JSON".encode("utf-8"))



				client_socket.sendall("Message recieved".encode("utf-8"))

			#if client disconnects, close socket
			client_socket.close()