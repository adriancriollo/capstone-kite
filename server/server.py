import socket
import threading

def handle_receive(client):
    while True:
        try:
            data = client.recv(1024).decode()
            if not data:  # Client disconnected
                print("Client disconnected")
                break
            print(f"Client: {data}")
        except:
            print("Error receiving data")
            break

def handle_send(client):
    while True:
        try:
            message = input("Enter message to send to client: ")
            client.send(message.encode())
        except:
            print("Error sending data")
            break

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 5000)) 
server.listen(1)

print("Waiting for a connection...")
client, addr = server.accept()
print(f"Connected to {addr}")

threading.Thread(target=handle_receive, args=(client,)).start()
threading.Thread(target=handle_send, args=(client,)).start()
