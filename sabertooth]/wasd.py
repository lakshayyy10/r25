import serial
import time
import keyboard  # Import the keyboard library

# Attempt to create a serial connection
try:
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)  # Adjust as needed
    print(f"Connected to {ser.portstr}")  # Confirm connection
except serial.SerialException as e:
    print(f"Error: {e}")
    exit(1)

def send_command(command):
    try:
        # Ensure command is sent as a single byte
        command_byte = bytes([command])
        ser.write(command_byte)
        print(f"Command sent: {command} (0x{command:02X})")  # Show command in hex for clarity
    except Exception as e:
        print(f"Failed to send command: {e}")

# Function to control motors with WASD keys
def control_motors():
    print("Control the motors using W and S keys:")
    print("W: Forward, S: Backward, Q: Stop, E: Exit")

    try:
        while True:
            if keyboard.is_pressed('w'):  # Move forward
                send_command(64 + 43)  # Motor 1 forward
                send_command(192 + 43)  # Motor 2 forward
            elif keyboard.is_pressed('s'):  # Move backward
                send_command(64 - 43)  # Motor 1 backward
                send_command(192 - 43)  # Motor 2 backward
            elif keyboard.is_pressed('q'):  # Stop all motors
                send_command(64)  # Stop motor 1
                send_command(192)  # Stop motor 2
            elif keyboard.is_pressed('e'):  # Exit the program
                break
            
            time.sleep(0.1)  # Add a short delay to reduce CPU usage

    except KeyboardInterrupt:
        print("Program interrupted.")
    
    # Stop all motors on exit
    send_command(64)  # Stop motor 1
    send_command(192)  # Stop motor 2

# Start controlling the motors
control_motors()

# Close the serial connection
ser.close()
print("Serial connection closed.")

