import time
import pygame
import serial

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

# Initialize pygame for GUI
pygame.init()
screen = pygame.display.set_mode((400, 400))  # Create a window
pygame.display.set_caption("Motor Control with Speed")

# Define colors
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Define button properties
button_width = 80
button_height = 80
button_margin = 20

# Create rectangles for buttons
w_button = pygame.Rect(150, 40, button_width, button_height)
a_button = pygame.Rect(80, 110, button_width, button_height)
s_button = pygame.Rect(150, 110, button_width, button_height)
d_button = pygame.Rect(220, 110, button_width, button_height)

# Define the slider for speed
slider_rect = pygame.Rect(100, 300, 200, 20)
slider_handle_rect = pygame.Rect(190, 290, 20, 40)  # The slider handle
slider_min, slider_max = 0, 100  # Slider range for speed control
current_speed = 50  # Start with 50% speed

# Motor state to track the current direction
motor_state = None

def update_speed(pos_x):
    """Update the speed based on the slider position and send to motors."""
    global current_speed
    if slider_rect.left <= pos_x <= slider_rect.right:
        # Calculate speed as a percentage of the slider position
        current_speed = int(((pos_x - slider_rect.left) / slider_rect.width) * 100)
        slider_handle_rect.x = pos_x - (slider_handle_rect.width // 2)  # Move the handle
        print(f"Speed set to {current_speed}%")

        # Send the updated speed command to the motors
        if motor_state == 'forward':
            send_command(64 + int(43 * current_speed / 100))  # Motor 1 forward
            send_command(192 + int(43 * current_speed / 100))  # Motor 2 forward
        elif motor_state == 'backward':
            send_command(64 - int(43 * current_speed / 100))  # Motor 1 backward
            send_command(192 - int(43 * current_speed / 100))  # Motor 2 backward
        elif motor_state == 'left':
            send_command(64 + int(43 * current_speed / 100))  # Motor 1 forward
            send_command(192 - int(43 * current_speed / 100))  # Motor 2 backward
        elif motor_state == 'right':
            send_command(64 - int(43 * current_speed / 100))  # Motor 1 backward
            send_command(192 + int(43 * current_speed / 100))  # Motor 2 forward

# Main loop for GUI
running = True
try:
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Get mouse position
                pos = pygame.mouse.get_pos()

                # Check if buttons were clicked
                if w_button.collidepoint(pos):
                    motor_state = 'forward'
                    send_command(64 + int(43 * current_speed / 100))  # Motor 1 forward
                    send_command(192 + int(43 * current_speed / 100))  # Motor 2 forward
                elif s_button.collidepoint(pos):
                    motor_state = 'backward'
                    send_command(64 - int(43 * current_speed / 100))  # Motor 1 backward
                    send_command(192 - int(43 * current_speed / 100))  # Motor 2 backward
                elif a_button.collidepoint(pos):
                    motor_state = 'left'
                    send_command(64 + int(43 * current_speed / 100))  # Motor 1 forward
                    send_command(192 - int(43 * current_speed / 100))  # Motor 2 backward
                elif d_button.collidepoint(pos):
                    motor_state = 'right'
                    send_command(64 - int(43 * current_speed / 100))  # Motor 1 backward
                    send_command(192 + int(43 * current_speed / 100))  # Motor 2 forward

                # Check if slider was clicked
                if slider_rect.collidepoint(pos):
                    update_speed(pos[0])

            if event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[0]:
                # Update speed if the mouse is dragging the slider
                if slider_rect.collidepoint(event.pos):
                    update_speed(event.pos[0])

        # Draw buttons
        screen.fill(WHITE)  # Fill background with white
        pygame.draw.rect(screen, GRAY, w_button)
        pygame.draw.rect(screen, GRAY, a_button)
        pygame.draw.rect(screen, GRAY, s_button)
        pygame.draw.rect(screen, GRAY, d_button)

        # Add text labels
        font = pygame.font.Font(None, 36)
        text_w = font.render('W', True, RED)
        text_a = font.render('A', True, RED)
        text_s = font.render('S', True, RED)
        text_d = font.render('D', True, RED)

        screen.blit(text_w, (w_button.centerx - 10, w_button.centery - 20))
        screen.blit(text_a, (a_button.centerx - 10, a_button.centery - 20))
        screen.blit(text_s, (s_button.centerx - 10, s_button.centery - 20))
        screen.blit(text_d, (d_button.centerx - 10, d_button.centery - 20))

        # Draw the speed slider
        pygame.draw.rect(screen, GRAY, slider_rect)  # Slider track
        pygame.draw.rect(screen, BLUE, slider_handle_rect)  # Slider handle
        text_speed = font.render(f"Speed: {current_speed}%", True, RED)
        screen.blit(text_speed, (slider_rect.centerx - 50, slider_rect.bottom + 10))

        pygame.display.flip()  # Update the display
        time.sleep(0.1)  # Small delay to reduce CPU usage

except KeyboardInterrupt:
    print("Keyboard interrupt detected.")
finally:
    # Stop motors and close the serial connection
    send_command(64)  # Stop motor 1
    send_command(192)  # Stop motor 2
    ser.close()
    print("Serial connection closed.")
    pygame.quit()
