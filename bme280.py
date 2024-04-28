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

# Pin setup
reed_pin = Pin(0, Pin.IN, Pin.PULL_DOWN)

# Variables to track the wind speed calculation
rotation_count = 0
time_last_calc = utime.ticks_ms()  # Time of last calculation
speed_readings = []  # List to store speed readings

# Constant to determine the measurement interval in milliseconds (e.g., 10 seconds)
MEASUREMENT_INTERVAL = 1000

# Constants
DEBOUNCE_TIME = 200  # Debounce time in milliseconds to avoid false triggers

# Setup the GPIO pin
rain_pin = Pin(18, Pin.IN, Pin.PULL_DOWN)  # Change the pin number based on your connection

# Variables to keep track of rainfall
tips_count = 0
last_tip_time = 0

# Set up the ADC on the GPIO pin connected to the potentiometer
pot_pin = 26  # GPIO pin number
adc = ADC(Pin(pot_pin))

# Reference voltage (3.3V)
v_ref = 3.3

# Define the threshold values for each direction
north_voltage = 1.1
east_voltage = 0.3
south_voltage = 2.8
west_voltage = 2.0

# Define the tolerance for voltage comparisons
tolerance = 0.1  # You can adjust this value as needed

# Read the ADC value (0 to 65535)
adc_value = adc.read_u16()
    
# Convert the ADC value to voltage
voltage = adc_value / 65535 * v_ref

# Initialize BME280 sensor
i2c = machine.I2C(0, sda=machine.Pin(16), scl=machine.Pin(17))
bme = bme280.BME280(i2c=i2c)

url = "http://192.168.3.101:5000/sensor-data"

# Wi-Fi credentials
#WIFI_SSID = "Reagan Computer"
#WIFI_PASSWORD = "V05h14(3"

# Wi-Fi credentials
WIFI_SSID = "Perspective Guest"
WIFI_PASSWORD = "worshipgrowserve"

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
    return water_collected_ml
    #print(f"Bucket tipped! Total Water Collected: {water_collected_ml:.2f} ml")

# Attach an interrupt to the pin
rain_pin.irq(trigger=Pin.IRQ_FALLING, handler=bucket_tipped)

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
        
        #print(f"Measured Wind Speed: {average_speed:.2f} MPH")
        return average_speed

def determine_direction(voltage):
    """Determine the direction based on the input voltage."""
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

# Function to handle HTTP requests
def send_data():
    data = bme.read_compensated_data()
    temperature = (data[0] * 1.8) + 32
    pressure = data[1] /100
    humidity = data[2]
    wind = calculate_wind_speed()
    direction = determine_direction(voltage)
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
    
    sleep(50)
    send_data()

# Main function
def main():
    connect_to_wifi()
    send_data()

if __name__ == "__main__":
    main()
