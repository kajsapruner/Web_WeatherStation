from machine import Pin, Timer
import utime

# Pin setup
reed_pin = Pin(0, Pin.IN, Pin.PULL_DOWN)

# Variables to track the wind speed calculation
rotation_count = 0
time_last_calc = utime.ticks_ms()  # Time of last calculation
speed_readings = []  # List to store speed readings

# Constant to determine the measurement interval in milliseconds (e.g., 10 seconds)
MEASUREMENT_INTERVAL = 1000

# Trigger function when reed switch is activated
def reed_triggered(pin):
    global rotation_count
    rotation_count += 1

# Attach interrupt to the reed switch pin
reed_pin.irq(trigger=Pin.IRQ_RISING, handler=reed_triggered)

def calculate_wind_speed():
    global rotation_count, time_last_calc, speed_readings

    current_time = utime.ticks_ms()
    elapsed_time = utime.ticks_diff(current_time, time_last_calc) / 1000  # Time since last calculation in seconds

    # If enough time has passed
    if elapsed_time >= MEASUREMENT_INTERVAL / 1000:
        # Calculate rotations per second (RPS)
        rps = rotation_count / elapsed_time
        
        # Calculate wind speed using the given equation: y = 0.4226x + 0.1383
        wind_speed = 0.4226 * rps + 0.1383
        
        # Store the reading and reset rotation count
        speed_readings.append(wind_speed)
        rotation_count = 0

        # Update the last calculation time
        time_last_calc = current_time

        # Calculate average speed over the last minute (60 seconds)
        # Keep only the readings from the last minute
        while len(speed_readings) > 60:
            speed_readings.pop(0)
        
        # Calculate the average wind speed
        average_speed = sum(speed_readings) / len(speed_readings)
        
        print(f"Measured Wind Speed: {average_speed:.2f} MPH")

# Main loop
try:
    while True:
        # Calculate wind speed regularly
        calculate_wind_speed()
        # Wait before the next calculation
        utime.sleep_ms(MEASUREMENT_INTERVAL)
except KeyboardInterrupt:
    print("Stopped by user")
