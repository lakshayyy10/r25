import socket
import threading

# Server configuration
HOST = '0.0.0.0'  # Accept connections on all available interfaces
PORT = 12345       # Arbitrary port to use

clients = []

# Function to handle receiving and broadcasting messages
def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    clients.append(conn)
    
    with conn:
        while True:
            try:
                # Receive messages from client
                data = conn.recv(1024).decode('utf-8')
                if not data:
                    break
                print(f"[{addr}] {data}")
                broadcast(f"[{addr}] {data}", conn)
            except ConnectionResetError:
                break
    
    # Remove client after disconnecting
    print(f"[DISCONNECT] {addr} disconnected.")
    clients.remove(conn)

# Function to broadcast messages to other clients
def broadcast(message, sender_conn=None):
    for client in clients:
        if client != sender_conn:  # Don't send the message back to the sender
            try:
                client.sendall(message.encode('utf-8'))
            except BrokenPipeError:
                pass

# Function for server to send its own messages
def server_send():
    while True:
        message = input("Server: ")
        broadcast(f"Server: {message}")  # Broadcast server messages to all clients

# Main server loop
def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print(f"[LISTENING] Server is listening on {HOST}:{PORT}")
        
        # Start a thread for server-side messaging
        server_thread = threading.Thread(target=server_send)
        server_thread.start()
        
        while True:
            conn, addr = server_socket.accept()
            client_thread = threading.Thread(target=handle_client, args=(conn, addr))
            client_thread.start()

# Start the server
if __name__ == "__main__":
    print("[STARTING] Server is starting...")
    start_server()

