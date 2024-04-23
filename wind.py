from machine import Pin, Timer
import utime

# Pin setup
reed_pin = Pin(0, Pin.IN, Pin.PULL_DOWN)

# Variables to track the wind speed calculation
last_activation = 0
rotation_count = 0

def reed_triggered(pin):
    global last_activation, rotation_count
    current_time = utime.ticks_ms()
   
    # Debounce the switch by ensuring at least 1 second between activations
    if utime.ticks_diff(current_time, last_activation) > 1000:
        rotation_count += 1
        last_activation = current_time
        print("Rotation detected!")

# Attach interrupt to the reed switch pin
reed_pin.irq(trigger=Pin.IRQ_RISING, handler=reed_triggered)

def calculate_wind_speed():
    global rotation_count
    # Calculate speed: Assuming 1 rotation per second equals 2 MPH (this is an example, adjust as needed)
    wind_speed = rotation_count * 2
    rotation_count = 0  # reset count after reading
    
    return wind_speed

# Main loop
try:
    while True:
        utime.sleep(1)  # calculate speed every minute
        speed = calculate_wind_speed()
        print(f"Measured Wind Speed: {speed} MPH")
except KeyboardInterrupt:
    print("Stopped by user")