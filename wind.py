from machine import Pin, Timer
import utime

reed_pin = Pin(0, Pin.IN, Pin.PULL_DOWN)

rotation_count = 0
time_last_calc = utime.ticks_ms()  
speed_readings = []  

MEASUREMENT_INTERVAL = 1000

def reed_triggered(pin):
    global rotation_count
    rotation_count += 1

reed_pin.irq(trigger=Pin.IRQ_RISING, handler=reed_triggered)

def calculate_wind_speed():
    global rotation_count, time_last_calc, speed_readings

    current_time = utime.ticks_ms()
    elapsed_time = utime.ticks_diff(current_time, time_last_calc) / 1000 

    if elapsed_time >= MEASUREMENT_INTERVAL / 1000:
        rps = rotation_count / elapsed_time
        
        wind_speed = 0.4226 * rps + 0.1383
        
        speed_readings.append(wind_speed)
        rotation_count = 0

        time_last_calc = current_time

        while len(speed_readings) > 60:
            speed_readings.pop(0)
        
        average_speed = sum(speed_readings) / len(speed_readings)
        
        print(f"Measured Wind Speed: {average_speed:.2f} MPH")

# Main loop
try:
    while True:
        calculate_wind_speed()
        utime.sleep_ms(MEASUREMENT_INTERVAL)
except KeyboardInterrupt:
    print("Stopped by user")
