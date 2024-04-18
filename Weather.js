// Get the canvas element and its context
var canvas = document.getElementById('canvas');
var ctx = canvas.getContext('2d');

// Function to update the canvas with weather data
function updateWeather(temperature, humidity, pressure, altitude) {
    // Clear the canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Draw temperature box
    ctx.fillStyle = 'lightblue';
    ctx.fillRect(20, 20, 100, 50);
    ctx.fillStyle = 'white';
    ctx.fillText("Temperature: " + temperature + "°C", 30, 50);

    // Draw humidity box
    ctx.fillStyle = 'lightblue';
    ctx.fillRect(140, 20, 100, 50);
    ctx.fillStyle = 'white';
    ctx.fillText("Humidity: " + humidity + "%", 150, 50);

    // Draw pressure box
    ctx.fillStyle = 'lightblue';
    ctx.fillRect(20, 100, 100, 50);
    ctx.fillStyle = 'white';
    ctx.fillText("Pressure: " + pressure + " hPa", 30, 130);

    // Draw altitude box
    ctx.fillStyle = 'lightblue';
    ctx.fillRect(140, 100, 100, 50);
    ctx.fillStyle = 'white';
    ctx.fillText("Altitude: " + altitude + " meters", 150, 130);
}
