from machine import Pin
import utime

DEBOUNCE_TIME = 200  
rain_pin = Pin(18, Pin.IN, Pin.PULL_DOWN)  

tips_count = 0
last_tip_time = 0

def bucket_tipped(pin):
    global tips_count, last_tip_time
    current_time = utime.ticks_ms()
    if utime.ticks_diff(current_time, last_tip_time) > DEBOUNCE_TIME:  
        tips_count += 1
        last_tip_time = current_time
        calculate_rainfall()

def calculate_rainfall():
    water_collected_ml = 5.308 * tips_count + 1.4464
    print(f"Bucket tipped! Total Water Collected: {water_collected_ml:.2f} ml")

rain_pin.irq(trigger=Pin.IRQ_FALLING, handler=bucket_tipped)

try:
    while True:
        utime.sleep(1)  
except KeyboardInterrupt:
    water_collected_ml = 5.308 * tips_count + 1.4464
    print(f"Program stopped. Total Water Collected: {water_collected_ml:.2f} ml")
