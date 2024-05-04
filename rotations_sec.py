from machine import Pin, Timer
import utime

# Pin setup
reed_pin = Pin(0, Pin.IN, Pin.PULL_DOWN)

# Variables to track the wind speed calculation
last_activation = 0
rotation_count = 0
start_time = utime.ticks_ms()  # Start time of the measurement period

def reed_triggered(pin):
    global last_activation, rotation_count
    current_time = utime.ticks_ms()
   
    # Calculate time since last activation in seconds
    if last_activation != 0:
        time_diff = utime.ticks_diff(current_time, last_activation) / 1000
    
    # Increment rotation count
    rotation_count += 1
    
    # Update last activation time
    last_activation = current_time

# Attach interrupt to the reed switch pin
reed_pin.irq(trigger=Pin.IRQ_RISING, handler=reed_triggered)

def calculate_average_rps():
    global rotation_count, start_time
    current_time = utime.ticks_ms()
    elapsed_time = utime.ticks_diff(current_time, start_time) / 1000  # Time elapsed in seconds

    # Calculate average rotations per second
    if elapsed_time > 0:
        average_rps = rotation_count / elapsed_time
    else:
        average_rps = 0
    
    # Print the average rotations per second
    print(f"Average Rotations per Second (1 min): {average_rps:.2f}")

    # Reset rotation count and start time for the next minute
    rotation_count = 0
    start_time = current_time

# Main loop
try:
    while True:
        # Calculate average RPS every minute (60 seconds)
        utime.sleep(60)
        calculate_average_rps()
except KeyboardInterrupt:
    print("Stopped by user")
