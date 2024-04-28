var temperatureHistoryDiv = document.getElementById("temperature-history");
var humidityHistoryDiv = document.getElementById("humidity-history");
var pressureHistoryDiv = document.getElementById("pressure-history");
var windSpeedHistoryDiv = document.getElementById("windSpeed-history");
var rainFallHistoryDiv = document.getElementById("rainFall-history");

var temperatureGaugeDiv = document.getElementById("temperature-gauge");
var humidityGaugeDiv = document.getElementById("humidity-gauge");
var pressureGaugeDiv = document.getElementById("pressure-gauge");
var windSpeedGaugeDiv = document.getElementById("windSpeed-gauge");
var rainFallGaugeDiv = document.getElementById("rainFall-gauge");

// History Data
var temperatureTrace = {
  x: [],
  y: [],
  name: "Temperature",
  mode: "lines+markers",
  type: "line",
};
var humidityTrace = {
  x: [],
  y: [],
  name: "Humidity",
  mode: "lines+markers",
  type: "line",
};
var pressureTrace = {
  x: [],
  y: [],
  name: "Pressure",
  mode: "lines+markers",
  type: "line",
};
var windSpeedTrace = {
  x: [],
  y: [],
  name: "Wind Speed",
  mode: "lines+markers",
  type: "line",
};
var rainFallTrace = {
  x: [],
  y: [],
  name: "Rain Fall",
  mode: "lines+markers",
  type: "line",
};

var temperatureLayout = {
  autosize: false,
  title: {
    text: "Temperature",
  },
  font: {
    size: 14,
    color: "#7f7f7f",
  },
  colorway: ["#B22222"],
  width: 450,
  height: 260,
  margin: { t: 30, b: 20, pad: 5 },
};
var humidityLayout = {
  autosize: false,
  title: {
    text: "Humidity",
  },
  font: {
    size: 14,
    color: "#7f7f7f",
  },
  colorway: ["#00008B"],
  width: 450,
  height: 260,
  margin: { t: 30, b: 20, pad: 5 },
};
var pressureLayout = {
  autosize: false,
  title: {
    text: "Pressure",
  },
  font: {
    size: 14,
    color: "#7f7f7f",
  },
  colorway: ["#FF4500"],
  width: 450,
  height: 260,
  margin: { t: 30, b: 20, pad: 5 },
};
var windSpeedLayout = {
  autosize: false,
  title: {
    text: "Wind Speed",
  },
  font: {
    size: 14,
    color: "#7f7f7f",
  },
  colorway: ["#008080"],
  width: 450,
  height: 260,
  margin: { t: 30, b: 20, pad: 5 },
};
var rainFallLayout = {
  autosize: false,
  title: {
    text: "Rain Fall",
  },
  font: {
    size: 14,
    color: "#7f7f7f",
  },
  colorway: ["#008080"],
  width: 450,
  height: 260,
  margin: { t: 30, b: 20, pad: 5 },
};

Plotly.newPlot(temperatureHistoryDiv, [temperatureTrace], temperatureLayout);
Plotly.newPlot(humidityHistoryDiv, [humidityTrace], humidityLayout);
Plotly.newPlot(pressureHistoryDiv, [pressureTrace], pressureLayout);
Plotly.newPlot(windSpeedHistoryDiv, [windSpeedTrace], windSpeedLayout);
Plotly.newPlot(rainFallHistoryDiv, [rainFallTrace], rainFallLayout);

// Gauge Data
var temperatureData = [
  {
    domain: { x: [0, 1], y: [0, 1] },
    value: 0,
    title: { text: "Temperature" },
    type: "indicator",
    mode: "gauge+number+delta",
    delta: { reference: 30 },
    gauge: {
      axis: { range: [null, 50] },
      steps: [
        { range: [0, 60], color: "lightgray" },
        { range: [60, 80], color: "gray" },
      ],
      threshold: {
        line: { color: "red", width: 4 },
        thickness: 0.75,
        value: 30,
      },
    },
  },
];

var humidityData = [
  {
    domain: { x: [0, 1], y: [0, 1] },
    value: 0,
    title: { text: "Humidity" },
    type: "indicator",
    mode: "gauge+number+delta",
    delta: { reference: 50 },
    gauge: {
      axis: { range: [null, 100] },
      steps: [
        { range: [0, 50], color: "lightgray" },
        { range: [50, 60], color: "gray" },
      ],
      threshold: {
        line: { color: "red", width: 4 },
        thickness: 0.75,
        value: 30,
      },
    },
  },
];

var pressureData = [
  {
    domain: { x: [0, 1], y: [0, 1] },
    value: 0,
    title: { text: "Pressure" },
    type: "indicator",
    mode: "gauge+number+delta",
    delta: { reference: 750 },
    gauge: {
      axis: { range: [null, 1100] },
      steps: [
        { range: [0, 900], color: "lightgray" },
        { range: [900, 1100], color: "gray" },
      ],
      threshold: {
        line: { color: "red", width: 4 },
        thickness: 0.75,
        value: 30,
      },
    },
  },
];

var windSpeedData = [
  {
    domain: { x: [0, 1], y: [0, 1] },
    value: 0,
    title: { text: "Wind Speed" },
    type: "indicator",
    mode: "gauge+number+delta",
    delta: { reference: 60 },
    gauge: {
      axis: { range: [null, 150] },
      steps: [
        { range: [0, 3], color: "lightgray" },
        { range: [3, 5], color: "gray" },
      ],
      threshold: {
        line: { color: "red", width: 4 },
        thickness: 0.75,
        value: 30,
      },
    },
  },
];

var rainFallData = [
  {
    domain: { x: [0, 1], y: [0, 1] },
    value: 0,
    title: { text: "Rain Fall" },
    type: "indicator",
    mode: "gauge+number+delta",
    delta: { reference: 60 },
    gauge: {
      axis: { range: [null, 150] },
      steps: [
        { range: [0, 10], color: "lightgray" },
        { range: [10, 20], color: "gray" },
      ],
      threshold: {
        line: { color: "red", width: 4 },
        thickness: 0.75,
        value: 30,
      },
    },
  },
];

var layout = { width: 300, height: 250, margin: { t: 0, b: 0, l: 0, r: 0 } };

Plotly.newPlot(temperatureGaugeDiv, temperatureData, layout);
Plotly.newPlot(humidityGaugeDiv, humidityData, layout);
Plotly.newPlot(pressureGaugeDiv, pressureData, layout);
Plotly.newPlot(windSpeedGaugeDiv, windSpeedData, layout);
Plotly.newPlot(rainFallGaugeDiv, rainFallData, layout);

// Will hold the arrays we receive from our BME280 sensor
// Temperature
let newTempXArray = [];
let newTempYArray = [];
// Humidity
let newHumidityXArray = [];
let newHumidityYArray = [];
// Pressure
let newPressureXArray = [];
let newPressureYArray = [];
// windSpeed
let newWindSpeedXArray = [];
let newWindSpeedYArray = [];
// rainFall
let newRainFallXArray = [];
let newRainFallYArray = [];
// The maximum number of data points displayed on our scatter/line graph
let MAX_GRAPH_POINTS = 12;
let ctr = 0;

// Callback function that will retrieve our latest sensor readings and redraw our Gauge with the latest readings
function updateSensorReadings() {
  fetch(`/get-sensor-data`)
    .then((response) => response.json())
    .then((jsonResponse) => {
      console.log(jsonResponse);
      let temperature = jsonResponse.temperature.toFixed(2);
      let humidity = jsonResponse.humidity.toFixed(2);
      let pressure = jsonResponse.pressure.toFixed(2);
      let windSpeed = jsonResponse.wind.toFixed(2);
      let windDirection = jsonResponse.direction; 
      let rainFall = jsonResponse.rain.toFixed(2);

      updateBoxes(temperature, humidity, pressure, windSpeed, windDirection, rainFall);

      updateGauge(temperature, humidity, pressure, windSpeed, rainFall);

      // Update Temperature Line Chart
      updateCharts(
        temperatureHistoryDiv,
        newTempXArray,
        newTempYArray,
        temperature
      );
      // Update Humidity Line Chart
      updateCharts(
        humidityHistoryDiv,
        newHumidityXArray,
        newHumidityYArray,
        humidity
      );
      // Update Pressure Line Chart
      updateCharts(
        pressureHistoryDiv,
        newPressureXArray,
        newPressureYArray,
        pressure
      );

      // Update windSpeed Line Chart
      updateCharts(
        windSpeedHistoryDiv,
        newWindSpeedXArray,
        newWindSpeedYArray,
        windSpeed
      );

      // Update rainFall Line Chart
      updateCharts(
        rainFallHistoryDiv,
        newrainFallXArray,
        newrainFallYArray,
        rainFall
      );
    });
}

function updateBoxes(temperature, humidity, pressure, windSpeed, windDirection, rainFall) {
  let temperatureDiv = document.getElementById("temperature");
  let humidityDiv = document.getElementById("humidity");
  let pressureDiv = document.getElementById("pressure");
  let windSpeedDiv = document.getElementById("windSpeed");
  let rainFallDiv = document.getElementById("rainFall");

  temperatureDiv.innerHTML = temperature + " F";
  humidityDiv.innerHTML = humidity + " %";
  pressureDiv.innerHTML = pressure + " Pa";
  windSpeedDiv.innerHTML = windSpeed + " MPH " + windDirection;
  rainFallDiv.innerHTML = rainFall + " mL";
}

function updateGauge(temperature, humidity, pressure, windSpeed, rainFall) {
  var temperature_update = {
    value: temperature,
  };
  var humidity_update = {
    value: humidity,
  };
  var pressure_update = {
    value: pressure,
  };
  var windSpeed_update = {
    value: windSpeed,
  };
  var rainFall_update = {
    value: rainFall,
  };
  Plotly.update(temperatureGaugeDiv, temperature_update);
  Plotly.update(humidityGaugeDiv, humidity_update);
  Plotly.update(pressureGaugeDiv, pressure_update);
  Plotly.update(windSpeedGaugeDiv, windSpeed_update);
  Plotly.update(rainFallGaugeDiv, rainFall_update);

}

function updateCharts(lineChartDiv, xArray, yArray, sensorRead) {
  if (xArray.length >= MAX_GRAPH_POINTS) {
    xArray.shift();
  }
  if (yArray.length >= MAX_GRAPH_POINTS) {
    yArray.shift();
  }
  xArray.push(ctr++);
  yArray.push(sensorRead);

  var data_update = {
    x: [xArray],
    y: [yArray],
  };

  Plotly.update(lineChartDiv, data_update);
}

// Continuos loop that runs evry 3 seconds to update our web page with the latest sensor readings
(function loop() {
  setTimeout(() => {
    updateSensorReadings();
    loop();
  }, 3000);
})();
