import numpy as np
import matplotlib.pyplot as plt

# PID gains
Kp = 1.5  # Proportional gain
Ki = 0.1  # Integral gain
Kd = 0.05  # Derivative gain

# Desired setpoint (target angle in degrees)
setpoint = 90.0  

# Simulation parameters
dt = 0.01  # Time step
time = np.arange(0, 10, dt)  # Total simulation time
n = len(time)

# Initial conditions
current_angle = 0.0
error_sum = 0.0
previous_error = 0.0
current_error = 0.0
angle_history = []
corrected_angle_history = []

# Gaussian noise parameters
mu = 0.0  # Mean
sigma = 0.5  # Standard deviation (for error simulation)

# PID control loop
for t in time:
    # Calculate the error
    current_error = setpoint - current_angle
    
    # Simulate Gaussian noise to mimic system errors/disturbances
    gaussian_error = np.random.normal(mu, sigma)
    
    # Noisy angle calculation
    noisy_angle = current_angle + gaussian_error
    
    # PID controller calculations
    P = Kp * current_error
    I = Ki * error_sum
    D = Kd * (current_error - previous_error) / dt
    
    # Update control signal (angle adjustment)
    control_signal = P + I + D
    
    # Update the corrected angle (system response)
    current_angle += control_signal * dt
    
    # Store histories for plotting
    angle_history.append(noisy_angle)
    corrected_angle_history.append(current_angle)
    
    # Update error sum and previous error for the next iteration
    error_sum += current_error * dt
    previous_error = current_error

# Plot the results
plt.figure(figsize=(12, 6))
plt.plot(time, angle_history, label="Noisy Angle", alpha=0.5)
plt.plot(time, corrected_angle_history, label="Corrected Angle", color='orange')
plt.axhline(y=setpoint, color='r', linestyle='--', label="Setpoint (90°)")
plt.xlabel("Time (s)")
plt.ylabel("Angle (°)")
plt.title("PID Control of Servo Motor: Noisy vs Corrected Angle")
plt.legend()
plt.grid(True)

# Save the plot as a PNG file in the current working directory
plt.savefig('pid_noisy_corrected_angles.png')

plt.close()

