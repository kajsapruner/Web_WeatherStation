from flask import Flask, jsonify, send_file
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return send_file('station.html')

@app.route('/sensor-data')
def sensor_data():
    response = requests.get('http://172.20.10.3')  # Replace with the IP of your MicroPython device
    data = response.json()
    return jsonify(data)

@app.route('/weather.js')
def weather_js():
    return send_file('weather.js')

if __name__ == '__main__':
    app.run(debug=True)
