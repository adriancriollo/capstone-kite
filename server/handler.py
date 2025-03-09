import socket
import json 
import threading
import time

from server import Server
import sensors2


#server module
'''
as of now this will be its own daemon to ensure that connection is stable,
and is consistently receiving control. The server is also directly controlling
the motor. 
'''

def daemon_serv():
	serv = Server()

	serv.init_server()
	serv.run_server()

#data module

#spawns a thread to run the sensor main. Will need better integration
def daemon_data():
	sensors2.main()


#main loop sequence
server_thread = threading.Thread(target=daemon_serv, daemon=True)

server_thread.start()

data_thread = threading.Thread(target=daemon_data, daemon=True)

data_thread.start()


#keeps main thread up, need a robust solution at some point
try:
	while True:
		time.sleep(1)
except KeyboardInterrupt:
	print("\nshutting down")





