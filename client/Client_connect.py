"""
This file will be for connecting the raspberry pi to the laptop over
a TCP socket connection
"""

import socket
import json
from pynput import keyboard
import time
import threading

SERVER_IP = "172.20.10.4"  # Replace with Raspberry Pi's IP
PORT = 8080
WINCH_SPEED = 20  # Adjust this value to control how fast the winch moves

# Create TCP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, PORT))
print(f"Connected to server at {SERVER_IP}:{PORT}")
print("Press a to pull left, d to pull right.")
print("Press 's' to stop the winch, and 'q' to quit.")


#state of the key commands
current_command = None
lock = threading.Lock()

#functions for running commands
def send_command(command):
    """Sends a JSON command to the server only if it has changed."""
    global current_command
    with lock:
        if current_command != command:  # Avoid sending duplicate commands
            client_socket.sendall(json.dumps(command).encode("utf-8"))
            current_command = command

def on_press(key):
    """Handles key press events."""
    try:
        if key == keyboard.Key.left:
            send_command({"winch_speed": -WINCH_SPEED})  # Pull left
        elif key == keyboard.Key.right:
            send_command({"winch_speed": WINCH_SPEED})   # Pull right
        elif key.char == "s":
            send_command({"stop": True})  # Stop winch
        elif key.char == "q":
            print("Closing connection...")
            client_socket.close()
            return False  # Stop the listener
    except AttributeError:
        pass  # Ignore unsupported keys

def on_release(key):
    """Stops winch movement when keys are released."""
    try:
        if key == keyboard.Key.left or key == keyboard.Key.right:
            send_command({"stop": True})  # Stop when arrow key is released
    except AttributeError:
        pass

# Start listening for keyboard input in a separate thread
listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()

# Main loop (keeps connection alive)
try:
    while listener.running:
        time.sleep(0.1)  # Prevent CPU overuse, adjust for responsiveness
except KeyboardInterrupt:
    print("Closing connection...")
    client_socket.close()