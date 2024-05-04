# Import necessary modules
from machine import Pin, Timer, ADC
from time import sleep
import utime
import bme280_float as bme280
import ujson
import ure as re
import usocket as socket
import network
import requests

# Wind Speed
reed_pin = Pin(0, Pin.IN, Pin.PULL_DOWN)
rotation_count = 0
time_last_calc = utime.ticks_ms()  
speed_readings = []  
MEASUREMENT_INTERVAL = 1000

# Rain Fall
rain_pin = Pin(18, Pin.IN, Pin.PULL_DOWN)  
DEBOUNCE_TIME = 200  
tips_count = 0
last_tip_time = 0

# Wind Direction
pot_pin = 26  
adc = ADC(Pin(pot_pin))
v_ref = 3.3
north_voltage = 1.1
east_voltage = 0.3
south_voltage = 2.8
west_voltage = 2.0
tolerance = 0.1 

# BME280
i2c = machine.I2C(0, sda=machine.Pin(16), scl=machine.Pin(17))
bme = bme280.BME280(i2c=i2c)

url = "http://10.251.64.151:5000/sensor-data"

# Wi-Fi credentials
WIFI_SSID = "Reagan Computer"
WIFI_PASSWORD = "V05h14(3"

# Connect to Wi-Fi
def connect_to_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connecting to Wi-Fi...")
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        while not wlan.isconnected():
            pass
    print("Wi-Fi connected:", wlan.ifconfig())

# Rain Fuctions
def bucket_tipped(pin):
    global tips_count, last_tip_time
    current_time = utime.ticks_ms()
    if utime.ticks_diff(current_time, last_tip_time) > DEBOUNCE_TIME:
        tips_count += 1
        last_tip_time = current_time
        calculate_rainfall()

def calculate_rainfall():
    water_collected_ml = 5.308 * tips_count 
    return water_collected_ml

rain_pin.irq(trigger=Pin.IRQ_FALLING, handler=bucket_tipped)

# Wind Speed Function
def reed_triggered(pin):
    global rotation_count
    rotation_count += 1

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
        
        return average_speed

reed_pin.irq(trigger=Pin.IRQ_RISING, handler=reed_triggered)


# Wind Direction Function
def determine_direction(voltage):
    print(f"Determining direction for voltage: {voltage}")
    if abs(voltage - north_voltage) <= tolerance:
        return "N"
    elif abs(voltage - east_voltage) <= tolerance:
        return "E"
    elif abs(voltage - south_voltage) <= tolerance:
        return "S"
    elif abs(voltage - west_voltage) <= tolerance:
        return "W"
    elif voltage > west_voltage and voltage < south_voltage:
        return "SW"
    elif voltage > north_voltage and voltage < west_voltage:
        return "NW"
    elif voltage > east_voltage and voltage < north_voltage:
        return "NE"
    else:
        return "SE"

def update_wind_direction():
    adc_value = adc.read_u16()
    
    voltage = adc_value / 65535 * v_ref
    
    direction = determine_direction(voltage)
    
    return direction

# Send Data Function
def send_data():
    data = bme.read_compensated_data()
    temperature = (data[0] * 1.8) + 32
    pressure = data[1] /100
    humidity = data[2]
    wind = calculate_wind_speed()
    direction = update_wind_direction()
    rain = calculate_rainfall()

    jsonData = {
        "temperature": temperature,
        "pressure": pressure,
        "humidity": humidity,
        "wind": wind,
        "direction": direction,
        "rain": rain
    }
    
    print(jsonData)
    
    response = requests.post(url, json=jsonData)
    
    print("Server response:" + response.text)
    
    sleep(10)
    send_data()

# Main function
def main():
    connect_to_wifi()
    send_data()

if __name__ == "__main__":
    main()
