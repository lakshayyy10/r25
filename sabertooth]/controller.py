import serial
import time
import pygame

# Initialize Pygame and the joystick module
pygame.init()
pygame.joystick.init()

# Attempt to create a serial connection
try:
    ser = serial.Serial('/dev/pts/2', 9600, timeout=1)  # Adjust as needed
    print(f"Connected to {ser.portstr}")  # Confirm connection
except serial.SerialException as e:
    print(f"Error: {e}")
    exit(1)

def send_command(command):
    """Send a command to the motor driver, ensuring it's within 0-255."""
    try:
        command = max(0, min(255, command))  # Clamp the value to range 0-255
        command_byte = bytes([command])
        ser.write(command_byte)
        print(f"Command sent: {command} (0x{command:02X})")
    except Exception as e:
        print(f"Failed to send command: {e}")

def map_speed(value, min_input, max_input, min_output, max_output):
    """Map joystick value to motor speed using linear interpolation."""
    return min_output + (max_output - min_output) * ((value - min_input) / (max_input - min_input))

def control_motors():
    """Control the motors using a game controller with speed interpolation."""
    print("Control the motors using the game controller:")

    # Check if a joystick is connected
    if pygame.joystick.get_count() < 1:
        print("No joystick detected.")
        return

    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    try:
        while True:
            pygame.event.pump()  # Process Pygame events
            
            # Get joystick axes (for left stick)
            axis_y = joystick.get_axis(1)  # Y-axis for forward/backward
            axis_x = joystick.get_axis(0)  # X-axis for left/right

            # Map joystick axis values (-1.0 to 1.0) to motor speed (0 to 255)
            # Forward (255), Backward (127 for motor 1, others can be adjusted similarly)
            if axis_y > 0:  # Moving backward
                motor1_speed = map_speed(axis_y, 0, 1.0, 127, 255)  # Motor 1 slower for backward
                motor2_speed = map_speed(axis_y, 0, 1.0, 127, 255)  # Motor 2 slower for backward
            elif axis_y < 0:  # Moving forward
                motor1_speed = map_speed(-axis_y, 0, 1.0, 128, 255)  # Forward movement for both motors
                motor2_speed = map_speed(-axis_y, 0, 1.0, 128, 255)
            else:  # Stopping
                motor1_speed = motor2_speed = 0

            # Send motor commands for forward/backward
            send_command(64 + int(motor1_speed))  # Motor 1 speed
            send_command(192 + int(motor2_speed))  # Motor 2 speed

            # Left/right turning (you can adjust this to rotate motors differently)
            if axis_x < -0.5:  # Turn left
                send_command(64 + int(128))  # Example turning speed for left
            elif axis_x > 0.5:  # Turn right
                send_command(192 + int(128))  # Example turning speed for right

            time.sleep(0.1)  # Short delay to reduce CPU usage

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

