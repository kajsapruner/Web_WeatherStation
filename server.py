from flask import Flask, jsonify, send_file, request

app = Flask(__name__)
json_data = None

@app.route('/')
def index():
    return send_file('index.html')

@app.route('/sensor-data', methods=['POST'])
def sensor_data():
    global json_data
    data = request.get_json()
    json_data = jsonify(data)
    return "Sensor Data recieved"

@app.route('/get-sensor-data')
def get_sensor_data():
    return json_data

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)