import socket
import json 
import threading
import time

from server import Server

#control module 





#server module
'''
as of now this will be its own daemon to ensure that connection is stable,
and is consistently receiving control.
'''

def daemon_serv():
	serv = Server()

	serv.init_server()
	serv.run_server()

#data module




#main loop sequence
server_thread = threading.Thread(target=daemon_serv, daemon=True)

server_thread.start()


#keeps main thread up, need a robust solution at some point
try:
	while True:
		time.sleep(1)
except KeyboardInterrupt:
	print("\nshutting down")





