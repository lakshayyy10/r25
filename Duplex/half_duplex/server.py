import socket

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to an address and port
server_socket.bind(('0.0.0.0', 9999))

# Listen for incoming connections
server_socket.listen(1)
print("Server is listening...")

# Accept a client connection
client_socket, addr = server_socket.accept()
print(f"Connected to {addr}")

while True:
    # Receive data from the client (half-duplex mode)
    data = client_socket.recv(1024).decode()
    if not data:
        break
    print("Client:", data)
    
    # Server sends a response after receiving data
    response = input("Enter response to client: ")
    client_socket.send(response.encode())

# Close the sockets
client_socket.close()
server_socket.close()

