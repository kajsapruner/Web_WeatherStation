# Import necessary modules
from machine import Pin
from time import sleep
import bme280_float as bme280
import ujson
import ure as re
import usocket as socket
import network

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

# Initialize BME280 sensor
i2c = machine.I2C(0, sda=machine.Pin(16), scl=machine.Pin(17))
bme = bme280.BME280(i2c=i2c)

# Function to handle HTTP requests
def handle_request(client_socket):
    data = bme.read_compensated_data()
    temperature = data[0]
    pressure = data[1]
    humidity = data[2]

    response = {
        "temperature": temperature,
        "pressure": pressure,
        "humidity": humidity
    }

    client_socket.send("HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n" + ujson.dumps(response))
    client_socket.close()

# Start socket server
def start_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 80))
    s.listen(5)

    while True:
        client_socket, addr = s.accept()
        req = client_socket.recv(4096)
        client_socket.settimeout(1)
        if req:
            client_socket.settimeout(None)
            handle_request(client_socket)

# Main function
def main():
    connect_to_wifi()
    start_server()

if __name__ == "__main__":
    main()
