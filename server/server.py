import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 5000))
server.listen(1)

print("Waiting for a connection...")
client, addr = server.accept()
print(f"Connected to {addr}")

try:
    while True:
        data = client.recv(1024).decode()
        if not data:
            print("Client disconnected")
            break
        print(f"Received: {data}")
        client.send("Acknowledged".encode())
finally:
    client.close()
    server.close()
