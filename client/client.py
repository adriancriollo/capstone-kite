import socket
import threading

def handle_receive(client):
    while True:
        try:
            data = client.recv(1024).decode()
            if not data:  # Server disconnected
                print("Server disconnected")
                break
            print(f"Server: {data}")
        except:
            print("Error receiving data")
            break

def handle_send(client):
    while True:
        try:
            message = input("Enter message to send to server: ")
            client.send(message.encode())
        except:
            print("Error sending data")
            break

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 5000))  # Replace with the server's IP and port

# Start threads for sending and receiving
threading.Thread(target=handle_receive, args=(client,)).start()
threading.Thread(target=handle_send, args=(client,)).start()
