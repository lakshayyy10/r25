import pygame
import socket
import math
import time

# UDP socket setup to send commands
UDP_IP = "192.168.68.23"  # Rover laptop IP
UDP_PORT = 5005
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

pygame.init()
pygame.joystick.init()

# Check if a joystick is connected
if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print(f"Joystick {joystick.get_name()} initialized")
else:
    print("No joystick connected!")
    exit()

def joystick_to_motor_power(x, y, max_motor_power=100, max_joystick=1.0):
    theta = math.atan2(y, x)
    magnitude = math.sqrt(x**2 + y**2)
    magnitude = min(magnitude, 1.0)

    x_cartesian = magnitude * math.cos(theta)
    y_cartesian = magnitude * math.sin(theta)

    x_scaled = (max_motor_power * x_cartesian) / max_joystick
    y_scaled = (max_motor_power * y_cartesian) / max_joystick

    right_motor_power = y_scaled - x_scaled
    left_motor_power = x_scaled + y_scaled

    return left_motor_power, right_motor_power

def control_motors(y_axis, x_axis):
    y_axis = -y_axis
    x_axis = -x_axis
    left_power, right_power = joystick_to_motor_power(x_axis, y_axis)

    if abs(y_axis) > 0.1 or abs(x_axis) > 0.1:
        left_speed = int(left_power * 63 / 100)
        right_speed = int(right_power * 63 / 100)
        
        left_command = 64 + left_speed if left_power >= 0 else 64 - abs(left_speed)
        right_command = 192 + right_speed if right_power >= 0 else 192 - abs(right_speed)
        
        # Send the motor command as a tuple (motor1, motor2)
        command = f"{left_command},{right_command}"
        sock.sendto(command.encode('utf-8'), (UDP_IP, UDP_PORT))
        
        # Print the sent command
        print(f"Sent command: Motor 1 = {left_command}, Motor 2 = {right_command}")
    else:
        # Send stop command
        command = "64,192"
        sock.sendto(command.encode('utf-8'), (UDP_IP, UDP_PORT))
        
        # Print the stop command
        print("Sent command: Stop (Motor 1 = 64, Motor 2 = 192)")

# Main loop to read joystick input
try:
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Get joystick axis values (e.g., left stick axes)
        x_axis = joystick.get_axis(0)
        y_axis = joystick.get_axis(1)

        control_motors(y_axis, x_axis)

        time.sleep(0.1)

except KeyboardInterrupt:
    print("Program interrupted.")
finally:
    pygame.quit()

