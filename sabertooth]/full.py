import serial
import time
import pygame
import sys

# Serial port configuration
serial_port = "/dev/pts/2"  # Replace with your FTDI port
baud_rate = 9600

# Joystick input range
joystick_min = -1.0  # Range from pygame for axis is -1 to 1
joystick_max = 1.0

# Motor speed ranges for Simplified Serial protocol
motor_1_min = 0    # Motor 1 range 0-127
motor_1_max = 127
motor_1_stop = 64  # Stop position for motor 1

motor_2_min = 128  # Motor 2 range 128-255
motor_2_max = 255
motor_2_stop = 192  # Stop position for motor 2

# Interpolation factor (change rate)
interpolation_factor = 10

# Function to map joystick value to motor speed
def map_joystick_to_motor(joystick_value, motor_stop, motor_min, motor_max):
    if joystick_value == 0:
        return motor_stop  # Stop position
    elif joystick_value > 0:
        # Forward direction
        return int((joystick_value / joystick_max) * (motor_max - motor_stop) + motor_stop)
    else:
        # Reverse direction
        return int((joystick_value / joystick_min) * (motor_stop - motor_min) + motor_min)

# Function to interpolate motor speed gradually
def interpolate_motor_speed(current_speed, target_speed, interpolation_factor):
    if current_speed == target_speed:
        return target_speed
    elif target_speed > current_speed:
        return min(current_speed + interpolation_factor, target_speed)
    else:
        return max(current_speed - interpolation_factor, target_speed)

# Main loop
try:
    with serial.Serial(serial_port, baud_rate) as ser:
        current_motor_1_speed = motor_1_stop
        current_motor_2_speed = motor_2_stop

        # Initialize pygame
        pygame.init()

        # Get the number of connected joysticks
        joystick_count = pygame.joystick.get_count()

        # If there are no joysticks, exit the program
        if joystick_count == 0:
            print("No joysticks detected.")
            sys.exit()

        # Use the first joystick
        joystick = pygame.joystick.Joystick(0)
        joystick.init()

        while True:
            pygame.event.pump()  # Process the event queue

            # Get the current joystick axis values
            axis_forward_backward = joystick.get_axis(1)  # Y-axis for forward/backward
            axis_left_right = joystick.get_axis(0)        # X-axis for left/right

            # Map the joystick value for forward/backward to motor speeds
            target_motor_1_speed = map_joystick_to_motor(axis_forward_backward, motor_1_stop, motor_1_min, motor_1_max)
            target_motor_2_speed = map_joystick_to_motor(axis_forward_backward, motor_2_stop, motor_2_min, motor_2_max)

            # Adjust for left and right control
            if axis_left_right < 0:  # Turning left (reduce speed on right motor)
                target_motor_1_speed = int(target_motor_1_speed * (1 + axis_left_right))  # Reduce left motor speed
            elif axis_left_right > 0:  # Turning right (reduce speed on left motor)
                target_motor_2_speed = int(target_motor_2_speed * (1 - axis_left_right))  # Reduce right motor speed

            # Interpolate motor speeds
            interpolated_motor_1_speed = interpolate_motor_speed(current_motor_1_speed, target_motor_1_speed, interpolation_factor)
            interpolated_motor_2_speed = interpolate_motor_speed(current_motor_2_speed, target_motor_2_speed, interpolation_factor)

            # Print the target and interpolated speeds
            print(f"Target Motor 1: {target_motor_1_speed}, Interpolated Motor 1: {interpolated_motor_1_speed}")
            print(f"Target Motor 2: {target_motor_2_speed}, Interpolated Motor 2: {interpolated_motor_2_speed}")

            # Send interpolated speed to the motor controller
            ser.write(bytes([int(interpolated_motor_1_speed)]))
            ser.write(bytes([int(interpolated_motor_2_speed)]))

            # Update current speeds
            current_motor_1_speed = interpolated_motor_1_speed
            current_motor_2_speed = interpolated_motor_2_speed

            time.sleep(0.01)  # Adjust delay as needed

except KeyboardInterrupt:
    print("Exiting...")

