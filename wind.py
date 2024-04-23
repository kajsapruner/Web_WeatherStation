from machine import Pin
import time

# Define the pin connected to the reed switch
reed_switch = Pin(0, Pin.IN, Pin.PULL_DOWN)

# Variables to keep track of the wind speed calculation
last_time = time.ticks_ms()
rotations = 0

# Callback function to handle the interrupt
def wind_speed_isr(pin):
    global last_time, rotations
    current_time = time.ticks_ms()
    # Calculate time difference to debounce the sensor
    if time.ticks_diff(current_time, last_time) > 1000:  # Debounce threshold 1000 ms
        rotations += 1
        last_time = current_time

# Attach the interrupt to the pin
reed_switch.irq(trigger=Pin.IRQ_RISING, handler=wind_speed_isr)

# Function to calculate wind speed
def calculate_wind_speed():
    global rotations
    # Convert rotations to wind speed (Example: 1 rotation per second = 1 MPH)
    # This conversion factor needs calibration
    speed = rotations * (60 / 3600)  # Convert rotations per hour to rotations per minute
    rotations = 0  # Reset rotation count
    return speed

# Main loop to calculate wind speed every minute
try:
    while True:
        time.sleep(60)  # Delay for 1 minute
        wind_speed = calculate_wind_speed()
        print(f"Current Wind Speed: {wind_speed:.2f} MPH")
except KeyboardInterrupt:
    print("Program stopped.")