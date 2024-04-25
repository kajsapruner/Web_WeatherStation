from machine import Pin
import utime

# Constants
DEBOUNCE_TIME = 200  # Debounce time in milliseconds to avoid false triggers

# Setup the GPIO pin
rain_pin = Pin(18, Pin.IN, Pin.PULL_DOWN)  # Change the pin number based on your connection

# Variables to keep track of rainfall
tips_count = 0
last_tip_time = 0

def bucket_tipped(pin):
    global tips_count, last_tip_time
    current_time = utime.ticks_ms()
    if utime.ticks_diff(current_time, last_tip_time) > DEBOUNCE_TIME:  # Debounce the sensor
        tips_count += 1
        last_tip_time = current_time
        calculate_rainfall()

def calculate_rainfall():
    # Calculate the amount of water in ml using the given equation
    water_collected_ml = 5.308 * tips_count + 1.4464
    print(f"Bucket tipped! Total Water Collected: {water_collected_ml:.2f} ml")

# Attach an interrupt to the pin
rain_pin.irq(trigger=Pin.IRQ_FALLING, handler=bucket_tipped)

try:
    while True:
        utime.sleep(1)  # Sleep to reduce CPU usage, loop keeps running to maintain the program
except KeyboardInterrupt:
    # Calculate final water collected at the end
    water_collected_ml = 5.308 * tips_count + 1.4464
    print(f"Program stopped. Total Water Collected: {water_collected_ml:.2f} ml")
