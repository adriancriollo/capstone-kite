import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 5000))

try:
    while True:
        message = input("Enter message to send to the server: ")
        client.send(message.encode())
        response = client.recv(1024).decode()
        print(f"Server says: {response}")
        if message.lower() == "exit":
            break
finally:
    client.close()