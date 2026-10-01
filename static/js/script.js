// ============================================================
// SMART ENVIRONMENTAL MONITORING + GENAI
// Real Hardware Version
//
// DHT11 → ESP8266 → Wi-Fi → Flask
//                       → Dashboard
//                       → History Chart
//                       → Ollama / Llama 3.2
// ============================================================


// ============================================================
// DOM ELEMENTS
// ============================================================

const temperatureElement =
    document.getElementById("temperature");

const humidityElement =
    document.getElementById("humidity");

const dataSourceElement =
    document.getElementById("dataSource");

const lastUpdateElement =
    document.getElementById("lastUpdate");

const environmentStatusElement =
    document.getElementById("environmentStatus");

const connectionTextElement =
    document.getElementById("connectionText");

const analyzeButton =
    document.getElementById("analyzeButton");

const aiResponseElement =
    document.getElementById("aiResponse");

const environmentChartCanvas =
    document.getElementById("environmentChart");


// ============================================================
// CHART VARIABLE
// ============================================================

let environmentChart = null;


// ============================================================
// DETERMINE ENVIRONMENTAL CONDITION
// ============================================================

function determineEnvironmentStatus(temperature, humidity) {

    if (temperature >= 35) {
        return "High Temperature";
    }

    if (humidity >= 80) {
        return "High Humidity";
    }

    if (temperature < 20) {
        return "Low Temperature";
    }

    if (humidity < 30) {
        return "Low Humidity";
    }

    return "Normal";
}


// ============================================================
// FORMAT TIMESTAMP
// ============================================================

function formatTimestamp(timestamp) {

    if (!timestamp) {
        return "--";
    }

    const date = new Date(timestamp);

    if (Number.isNaN(date.getTime())) {
        return timestamp;
    }

    return date.toLocaleTimeString();
}


// ============================================================
// FETCH LATEST REAL DHT11 SENSOR READING
// ============================================================

async function fetchSensorData() {

    try {

        const response = await fetch(
            "/api/sensor",
            {
                cache: "no-store"
            }
        );


        if (!response.ok) {

            throw new Error(
                `Server returned ${response.status}`
            );
        }


        const data = await response.json();


        // ----------------------------------------------------
        // No DHT11 data received yet
        // ----------------------------------------------------

        if (
            data.temperature === null ||
            data.humidity === null
        ) {

            temperatureElement.textContent = "--";

            humidityElement.textContent = "--";

            dataSourceElement.textContent =
                "Waiting for ESP8266";

            lastUpdateElement.textContent = "--";

            environmentStatusElement.textContent =
                "Waiting for data";

            connectionTextElement.textContent =
                "Waiting for sensor";

            return;
        }


        // ----------------------------------------------------
        // Convert DHT11 values to numbers
        // ----------------------------------------------------

        const temperature =
            Number(data.temperature);

        const humidity =
            Number(data.humidity);


        // ----------------------------------------------------
        // Update live temperature and humidity
        // ----------------------------------------------------

        temperatureElement.textContent =
            temperature.toFixed(1);

        humidityElement.textContent =
            humidity.toFixed(1);


        // ----------------------------------------------------
        // Update physical IoT source and timestamp
        // ----------------------------------------------------

        dataSourceElement.textContent =
            data.source || "DHT11 + ESP8266";

        lastUpdateElement.textContent =
            formatTimestamp(data.timestamp);


        // ----------------------------------------------------
        // Determine environmental condition
        // ----------------------------------------------------

        const status =
            determineEnvironmentStatus(
                temperature,
                humidity
            );

        environmentStatusElement.textContent =
            status;


        // ----------------------------------------------------
        // ESP8266 / Flask connection status
        // ----------------------------------------------------

        connectionTextElement.textContent =
            "Live";

    }

    catch (error) {

        console.error(
            "Unable to retrieve DHT11 sensor data:",
            error
        );

        connectionTextElement.textContent =
            "Connection Error";

        environmentStatusElement.textContent =
            "Backend unavailable";
    }
}


// ============================================================
// CREATE REAL-TIME DHT11 HISTORY CHART
// ============================================================

function createEnvironmentChart() {

    if (!environmentChartCanvas) {

        console.error(
            "Environment chart canvas was not found."
        );

        return;
    }


    // Make sure local Chart.js loaded successfully

    if (typeof Chart === "undefined") {

        console.error(
            "Chart.js is not available."
        );

        return;
    }


    const context =
        environmentChartCanvas.getContext("2d");


    environmentChart = new Chart(
        context,
        {
            type: "line",

            data: {

                labels: [],

                datasets: [

                    {
                        label: "Temperature (°C)",

                        data: [],

                        borderColor: "#dc2626",

                        backgroundColor:
                            "rgba(220, 38, 38, 0.10)",

                        borderWidth: 3,

                        pointRadius: 3,

                        pointHoverRadius: 6,

                        tension: 0.3,

                        fill: false,

                        yAxisID: "temperatureAxis"
                    },

                    {
                        label: "Humidity (%)",

                        data: [],

                        borderColor: "#2563eb",

                        backgroundColor:
                            "rgba(37, 99, 235, 0.10)",

                        borderWidth: 3,

                        pointRadius: 3,

                        pointHoverRadius: 6,

                        tension: 0.3,

                        fill: false,

                        yAxisID: "humidityAxis"
                    }
                ]
            },


            options: {

                responsive: true,

                maintainAspectRatio: false,

                animation: {
                    duration: 300
                },


                interaction: {

                    mode: "index",

                    intersect: false
                },


                plugins: {

                    legend: {

                        position: "top",

                        labels: {

                            usePointStyle: true,

                            padding: 20,

                            font: {
                                size: 14,
                                weight: "600"
                            }
                        }
                    },


                    tooltip: {

                        enabled: true,

                        callbacks: {

                            label: function(context) {

                                const label =
                                    context.dataset.label ||
                                    "";

                                const value =
                                    Number(
                                        context.parsed.y
                                    ).toFixed(1);

                                return `${label}: ${value}`;
                            }
                        }
                    }
                },


                scales: {

                    x: {

                        title: {

                            display: true,

                            text: "Time",

                            color: "#475569",

                            font: {
                                size: 14,
                                weight: "600"
                            }
                        },


                        ticks: {

                            color: "#475569",

                            maxRotation: 45,

                            minRotation: 0,

                            autoSkip: true,

                            maxTicksLimit: 10
                        },


                        grid: {

                            color:
                                "rgba(148, 163, 184, 0.20)"
                        }
                    },


                    temperatureAxis: {

                        type: "linear",

                        position: "left",

                        title: {

                            display: true,

                            text: "Temperature (°C)",

                            color: "#475569",

                            font: {
                                size: 14,
                                weight: "600"
                            }
                        },


                        ticks: {

                            color: "#475569"
                        },


                        grid: {

                            color:
                                "rgba(148, 163, 184, 0.20)"
                        }
                    },


                    humidityAxis: {

                        type: "linear",

                        position: "right",

                        min: 0,

                        max: 100,

                        title: {

                            display: true,

                            text: "Humidity (%)",

                            color: "#475569",

                            font: {
                                size: 14,
                                weight: "600"
                            }
                        },


                        ticks: {

                            color: "#475569"
                        },


                        grid: {

                            drawOnChartArea: false
                        }
                    }
                }
            }
        }
    );
}


// ============================================================
// FETCH REAL DHT11 SENSOR HISTORY
// ============================================================

async function fetchSensorHistory() {

    try {

        const response = await fetch(
            "/api/history",
            {
                cache: "no-store"
            }
        );


        if (!response.ok) {

            throw new Error(
                `Server returned ${response.status}`
            );
        }


        const data =
            await response.json();


        if (
            !Array.isArray(data.readings) ||
            data.readings.length === 0
        ) {

            return;
        }


        // ----------------------------------------------------
        // Prepare chart timestamps
        // ----------------------------------------------------

        const labels =
            data.readings.map(
                reading =>
                    formatTimestamp(
                        reading.timestamp
                    )
            );


        // ----------------------------------------------------
        // Prepare DHT11 temperature values
        // ----------------------------------------------------

        const temperatures =
            data.readings.map(
                reading =>
                    Number(
                        reading.temperature
                    )
            );


        // ----------------------------------------------------
        // Prepare DHT11 humidity values
        // ----------------------------------------------------

        const humidities =
            data.readings.map(
                reading =>
                    Number(
                        reading.humidity
                    )
            );


        // ----------------------------------------------------
        // Update real-time chart
        // ----------------------------------------------------

        if (environmentChart) {

            environmentChart.data.labels =
                labels;

            environmentChart
                .data
                .datasets[0]
                .data =
                temperatures;

            environmentChart
                .data
                .datasets[1]
                .data =
                humidities;

            environmentChart.update();
        }

    }

    catch (error) {

        console.error(
            "Unable to retrieve DHT11 sensor history:",
            error
        );
    }
}


// ============================================================
// FORMAT GENAI RESPONSE
// ============================================================

function formatAIResponse(text) {

    if (!text) {

        return "No AI analysis was returned.";
    }


    /*
       Convert the small amount of Markdown returned by
       Llama 3.2 into HTML for dashboard presentation.

       Example:

       **Environmental Condition:**

       becomes:

       <strong>Environmental Condition:</strong>
    */


    return text
        .replace(
            /\*\*(.*?)\*\*/g,
            "<strong>$1</strong>"
        )
        .replace(
            /\n/g,
            "<br>"
        );
}


// ============================================================
// GENAI ENVIRONMENTAL ANALYSIS
// ============================================================

async function analyzeEnvironment() {

    if (!analyzeButton || !aiResponseElement) {

        console.error(
            "GenAI dashboard elements were not found."
        );

        return;
    }


    // --------------------------------------------------------
    // Show loading state
    // --------------------------------------------------------

    analyzeButton.disabled = true;

    analyzeButton.textContent =
        "Analyzing with Llama 3.2...";

    aiResponseElement.textContent =
        "Generating environmental analysis...";


    try {

        // ----------------------------------------------------
        // Request AI analysis from Flask
        // ----------------------------------------------------

        const response = await fetch(
            "/api/analyze",
            {
                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                }
            }
        );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.error ||
                "AI analysis failed"
            );
        }


        // ----------------------------------------------------
        // Format local Llama 3.2 response
        // ----------------------------------------------------

        const formattedAnalysis =
            formatAIResponse(
                data.analysis
            );


        // ----------------------------------------------------
        // Display formatted Llama 3.2 response
        // ----------------------------------------------------

        aiResponseElement.innerHTML =
            formattedAnalysis;

    }

    catch (error) {

        console.error(
            "GenAI error:",
            error
        );


        aiResponseElement.textContent =
            "Unable to generate AI analysis. " +
            "Please make sure Ollama and " +
            "Llama 3.2 are running.";
    }

    finally {

        analyzeButton.disabled = false;

        analyzeButton.textContent =
            "Analyze Current Environment";
    }
}


// ============================================================
// INITIALIZE REAL-HARDWARE DASHBOARD
// ============================================================

// Create empty history chart
createEnvironmentChart();

// Load latest DHT11 reading immediately
fetchSensorData();

// Load available DHT11 history immediately
fetchSensorHistory();


// ============================================================
// AUTOMATIC LIVE UPDATES
// ============================================================

// Refresh latest DHT11 sensor reading every 2 seconds
setInterval(
    fetchSensorData,
    2000
);


// Refresh DHT11 history chart every 2 seconds
setInterval(
    fetchSensorHistory,
    2000
);


// ============================================================
// GENAI BUTTON EVENT
// ============================================================

if (analyzeButton) {

    analyzeButton.addEventListener(
        "click",
        analyzeEnvironment
    );
}