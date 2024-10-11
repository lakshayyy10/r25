import socket
import serial

# Set up serial connection to Sabertooth motor controller
ser = serial.Serial('/dev/ttyUSB0', 9600)  # Adjust the port as necessary

# Set up UDP socket to receive commands
UDP_IP = "0.0.0.0"  # Listening on all available interfaces
UDP_PORT = 5005
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print("Waiting for commands...")

def send_command_to_sabertooth(motor_1_value, motor_2_value):
    ser.write(bytes([motor_1_value]))
    ser.write(bytes([motor_2_value]))

try:
    while True:
        data, addr = sock.recvfrom(1024)  # Receive command
        motor_commands = data.decode('utf-8').split(',')

        if len(motor_commands) == 2:
            motor_1_value = int(motor_commands[0])
            motor_2_value = int(motor_commands[1])

            send_command_to_sabertooth(motor_1_value, motor_2_value)
            print(f"Received command: Motor 1 = {motor_1_value}, Motor 2 = {motor_2_value}")

except KeyboardInterrupt:
    print("Closing connection.")
finally:
    ser.close()
    sock.close()

