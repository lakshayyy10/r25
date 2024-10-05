import socket

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect(('192.168.137.23', 9999))

while True:
    # Client sends data to the server
    message = input("Enter message to server: ")
    client_socket.send(message.encode())
    
    # Receive a response from the server
    data = client_socket.recv(1024).decode()
    if not data:
        break
    print("Server:", data)

# Close the socket
client_socket.close()

