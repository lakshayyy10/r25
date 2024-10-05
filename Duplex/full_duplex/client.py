import socket
import threading

# Server configuration
HOST = '127.0.0.1'  # Server IP address (use actual server IP in production)
PORT = 12345        # Same port as the server

# Function to receive messages from the server
def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                print("Connection closed by the server.")
                break
            print(f"{message}")
        except ConnectionResetError:
            print("Connection lost.")
            break

# Function to send messages to the server
def send_messages(client_socket):
    while True:
        message = input("You: ")
        if message.lower() == 'exit':
            print("Closing connection...")
            client_socket.close()
            break
        client_socket.sendall(message.encode('utf-8'))

# Main client function
def start_client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        try:
            client_socket.connect((HOST, PORT))
            print(f"Connected to the server at {HOST}:{PORT}")
            
            # Start threads for sending and receiving messages
            receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
            send_thread = threading.Thread(target=send_messages, args=(client_socket,))
            
            receive_thread.start()
            send_thread.start()
            
            # Wait for both threads to finish
            receive_thread.join()
            send_thread.join()
        except ConnectionRefusedError:
            print(f"Unable to connect to the server at {HOST}:{PORT}")

# Start the client
if __name__ == "__main__":
    start_client()

