import socket
import threading

# Client configuration
SERVER_IP = '25.11.189.28'  # Replace with your server's IP address
SERVER_PORT = 12345        # Same port as the server

# Function to handle receiving messages from the server
def receive_messages(sock):
    while True:
        try:
            message = sock.recv(1024).decode('utf-8')
            if not message:
                break
            print(f"\nReceived: {message}")
        except ConnectionResetError:
            break

# Main function for sending messages
def start_client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((SERVER_IP, SERVER_PORT))
        print("Connected to the server.")

        # Start a thread to handle incoming messages
        receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
        receive_thread.start()

        # Main loop to send messages
        while True:
            message = input("You: ")
            if message.lower() == "exit":
                break
            client_socket.sendall(message.encode('utf-8'))

        print("Disconnected from the server.")

if __name__ == "__main__":
    start_client()

