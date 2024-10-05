import time
import serial
# Simulated serial connection for testing
class SimulatedSerial:
    def __init__(self, port, baudrate):
        self.port = port
        self.baudrate = baudrate
        print(f"Simulated connection established on port {port} with baudrate {baudrate}")

    def write(self, command):
        # Simulate the sending of a command to the Sabertooth
        print(f"Command sent: {command[0]} (0x{command[0]:02X})")  # Show command in hex for clarity

    def close(self):
        print("Simulated connection closed.")

# Use the simulated serial instead of real one for testing
ser = SimulatedSerial('/dev/ttyUSB0', 9600)

def send_command(command):
    ser.write(bytes([command]))  # Ensure command is sent as a single byte

# Move motor forward simulation
send_command(64 + 43)  # Simulate moving motor 1 forward at medium speed
send_command(192 + 43)  # Simulate moving motor 2 forward at medium speed
time.sleep(2)  # Simulate running for 2 seconds

# Stop motors simulation
send_command(64)  # Simulate stopping motor 1
send_command(192)  # Simulate stopping motor 2
time.sleep(1)  # Simulate pause for a second

# Move motor backward simulation
send_command(64 - 43)  # Simulate moving motor 1 backward at medium speed
send_command(192 - 43)  # Simulate moving motor 2 backward at medium speed
time.sleep(2)

# Stop motors simulation
send_command(64)  # Simulate stopping motor 1
send_command(192)  # Simulate stopping motor 2

# Close the simulated serial connection
ser.close()

