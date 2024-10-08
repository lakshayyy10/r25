import tkinter as tk
from tkinter import ttk
import serial
import time

# Attempt to create a serial connection
try:
    ser = serial.Serial('/dev/pts/3', 9600, timeout=1)  # Adjust as needed
    print(f"Connected to {ser.portstr}")  # Confirm connection
except serial.SerialException as e:
    print(f"Error: {e}")
    exit(1)

def send_command(command):
    """Send a command to the Sabertooth motor controller."""
    try:
        command_byte = bytes([command])
        ser.write(command_byte)
        print(f"Command sent: {command} (0x{command:02X})")
    except Exception as e:
        print(f"Failed to send command: {e}")

def update_speed_label(val):
    speed_label.config(text=f"Speed: {int(val)}")  # Update speed label dynamically

def move_forward():
    speed = speed_slider.get()
    send_command(64 + speed)
    send_command(192 + speed)

def move_backward():
    speed = speed_slider.get()
    send_command(64 - speed)
    send_command(192 - speed)

def move_left():
    speed = speed_slider.get()
    send_command(64 + speed)
    send_command(192 - speed)

def move_right():
    speed = speed_slider.get()
    send_command(64 - speed)
    send_command(192 + speed)

def stop_motors():
    send_command(64)  # Stop motor 1
    send_command(192)  # Stop motor 2

def quit_program():
    stop_motors()
    ser.close()  # Close the serial connection
    root.destroy()  # Close the Tkinter window

# Create the main window
root = tk.Tk()
root.title("Motor Control")

# Create control buttons
forward_button = tk.Button(root, text="Forward (W)", width=15, height=2, command=move_forward)
backward_button = tk.Button(root, text="Backward (S)", width=15, height=2, command=move_backward)
left_button = tk.Button(root, text="Left (A)", width=15, height=2, command=move_left)
right_button = tk.Button(root, text="Right (D)", width=15, height=2, command=move_right)
stop_button = tk.Button(root, text="Stop", width=15, height=2, command=stop_motors)
quit_button = tk.Button(root, text="Quit", width=15, height=2, command=quit_program)

# Arrange buttons in grid layout
forward_button.grid(row=0, column=1, padx=10, pady=10)
backward_button.grid(row=2, column=1, padx=10, pady=10)
left_button.grid(row=1, column=0, padx=10, pady=10)
right_button.grid(row=1, column=2, padx=10, pady=10)
stop_button.grid(row=1, column=1, padx=10, pady=10)
quit_button.grid(row=3, column=1, padx=10, pady=10)

# Create a slider for speed control
speed_label = tk.Label(root, text="Speed: 20")
speed_label.grid(row=4, column=0, columnspan=3)

speed_slider = ttk.Scale(root, from_=0, to=127, orient="horizontal", command=update_speed_label)
speed_slider.set(20)  # Default speed value
speed_slider.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

# Start the Tkinter event loop
root.mainloop()

# Stop motors and close the serial connection when exiting
stop_motors()
ser.close()
print("Serial connection closed.")

