# Smart Environmental Monitoring and GenAI Assistant Using IoT

## Real DHT11 + ESP8266 Hardware Version

This project is a **Smart Environmental Monitoring and GenAI Assistant**
that combines **Internet of Things (IoT)**, real-time Web technologies,
and **Generative AI**.

A physical **DHT11 sensor** measures temperature and humidity. The
sensor is connected to an **ESP8266** board programmed with
**MicroPython**. The ESP8266 sends the measurements over Wi-Fi to a
**Flask REST backend**, where they are displayed on a real-time Web
dashboard.

The application also integrates **Ollama and Llama 3.2**, running
locally, to interpret the current environmental measurements and
generate a natural-language environmental condition, analysis, and
recommendation.

------------------------------------------------------------------------

# 1. System Flow

``` text
Real Environment
      │
      ▼
DHT11 Sensor
      │
      │ Temperature + Humidity
      ▼
ESP8266 + MicroPython
      │
      │ Wi-Fi
      │ HTTP POST / JSON
      ▼
Flask Backend + REST API
      │
      ├──────────────► Live Sensor Data
      │
      ├──────────────► Last 30 Readings
      │
      └──────────────► Ollama / Llama 3.2
                              │
                              ▼
                    GenAI Environmental Analysis
      │
      ▼
HTML + CSS + JavaScript
      │
      ▼
Chart.js Real-Time Visualization
      │
      ▼
Web Dashboard
```

The complete data flow can therefore be summarized as:

**DHT11 → ESP8266 → Wi-Fi → HTTP/JSON → Flask REST API → Web Dashboard →
Chart.js → Ollama/Llama 3.2**

------------------------------------------------------------------------

# 2. Main Features

The application provides:

-   Real DHT11 temperature measurements
-   Real DHT11 humidity measurements
-   ESP8266 Wi-Fi communication
-   MicroPython-based sensor acquisition
-   HTTP/JSON communication between the ESP8266 and Flask
-   Flask REST API
-   Live temperature display
-   Live humidity display
-   Current environmental status
-   Physical IoT data-source identification
-   Latest-reading timestamp
-   Rolling history of the latest 30 sensor readings
-   Real-time temperature and humidity chart
-   Local Chart.js integration
-   Local Ollama integration
-   Llama 3.2 environmental analysis
-   Environmental Condition generation
-   Environmental Analysis
-   Practical Recommendation
-   Responsive Web dashboard

------------------------------------------------------------------------

# Application Screenshots

The following screenshots show the three main sections of the running
application using real DHT11 sensor data transmitted through the
ESP8266.

## Live Environmental Monitoring

The main dashboard displays the latest temperature and humidity
measurements received from the physical DHT11 sensor, together with the
current environmental status, data source, and latest-reading time.

![Live Environmental
Monitoring](docs/screenshots/dashboard-live-monitoring.jpg)

## Temperature and Humidity History

The real-time history section visualizes the latest 30 temperature and
humidity measurements collected from the DHT11 sensor through the
ESP8266.

![Temperature and Humidity
History](docs/screenshots/temperature-humidity-history.jpg)

## GenAI Environmental Analysis

The GenAI Environmental Assistant sends the latest environmental
measurements to the locally running Llama 3.2 model through Ollama and
displays the generated environmental condition, analysis, and
recommendation.

![GenAI Environmental
Analysis](docs/screenshots/genai-environmental-analysis.jpg)

------------------------------------------------------------------------

# 3. Hardware Requirements

The real-hardware version requires:

-   ESP8266 development board
-   DHT11 temperature and humidity sensor
-   Dupont jumper wires
-   USB cable for connecting/programming the ESP8266
-   Laptop or desktop computer
-   Wi-Fi network or mobile-phone hotspot

The DHT11 data pin used by the current MicroPython program is:

``` text
GPIO4
```

On many NodeMCU ESP8266 boards:

``` text
GPIO4 = D2
```

------------------------------------------------------------------------

# 4. Software Requirements

The project uses:

-   Python 3
-   Flask
-   Ollama
-   Llama 3.2
-   MicroPython
-   HTML
-   CSS
-   JavaScript
-   Chart.js 4.5.1
-   Visual Studio Code
-   Thonny or another MicroPython-compatible development environment

A Conda environment can also be used for the Python/Flask backend.

------------------------------------------------------------------------

# 5. Project Structure

``` text
Smart_Environment_IoT_GenAI_Real_DHT11_ESP8266/
│
├── README.md
│
├── .vscode/
│   └── settings.json
│
├── backend/
│   └── app.py
│
├── docs/
│   └── screenshots/
│       ├── dashboard-live-monitoring.jpg
│       ├── temperature-humidity-history.jpg
│       └── genai-environmental-analysis.jpg
│
├── esp8266/
│   └── main.py
│
├── static/
│   ├── css/
│   │   └── style.css
│   │
│   └── js/
│       ├── chart.umd.min.js
│       └── script.js
│
└── templates/
    └── index.html
```

`chart.umd.min.js` is stored locally so the dashboard does not depend on
the Chart.js CDN during normal operation.

------------------------------------------------------------------------

# 6. ESP8266 Configuration

The ESP8266 program is located at:

``` text
esp8266/main.py
```

Before running the real hardware, configure the Wi-Fi connection.

Open:

``` text
esp8266/main.py
```

Find:

``` python
WIFI_SSID = "WIFI_SSID"
WIFI_PASSWORD = "WIFI_PASSWORD"
```

Replace these placeholders locally with the Wi-Fi network or
mobile-hotspot credentials:

``` python
WIFI_SSID = "YOUR_WIFI_NAME"
WIFI_PASSWORD = "YOUR_WIFI_PASSWORD"
```

Do not commit real Wi-Fi credentials to a public GitHub repository.

------------------------------------------------------------------------

# 7. Flask Server Address Configuration

The ESP8266 must know the IP address of the laptop running the Flask
backend.

The GitHub version contains:

``` python
SERVER_URL = "http://YOUR_LAPTOP_IP:5000/api/sensor"
```

On Windows, open Command Prompt and run:

``` text
ipconfig
```

Find the IPv4 address of the network adapter connected to the same Wi-Fi
network or hotspot as the ESP8266.

For example, if the laptop IPv4 address were:

``` text
192.168.1.10
```

the local ESP8266 configuration would become:

``` python
SERVER_URL = "http://192.168.1.10:5000/api/sensor"
```

The ESP8266 and the computer running Flask must be able to communicate
over the same local network.

Do not replace `YOUR_LAPTOP_IP` in the public GitHub version with a
personal network address unless necessary.

------------------------------------------------------------------------

# 8. DHT11 Configuration

The current MicroPython code uses:

``` python
DHT_PIN = 4
```

The DHT11 is therefore read through:

``` text
GPIO4
```

On many NodeMCU ESP8266 development boards, GPIO4 corresponds to:

``` text
D2
```

The DHT11 sensor object is initialized in MicroPython and periodically
measures:

-   Temperature in degrees Celsius
-   Humidity in percent

------------------------------------------------------------------------

# 9. Sensor Reading Interval

After initialization, the ESP8266 continuously reads the physical DHT11
sensor.

The current program waits:

``` python
time.sleep(5)
```

between iterations.

Therefore, a new environmental reading is obtained approximately every
**5 seconds**.

------------------------------------------------------------------------

# 10. Communication Between ESP8266 and Flask

The ESP8266 sends the sensor measurements to the Flask backend using an
HTTP POST request.

The JSON data has the following structure:

``` json
{
    "temperature": 30,
    "humidity": 60,
    "source": "DHT11 + ESP8266"
}
```

The request is sent to:

``` text
POST /api/sensor
```

The Flask backend receives and validates the physical sensor
measurements.

------------------------------------------------------------------------

# 11. Flask REST API

The Flask backend is located at:

``` text
backend/app.py
```

The application provides the following main endpoints.

## POST /api/sensor

Receives physical temperature and humidity measurements from the
ESP8266.

## GET /api/sensor

Returns the latest available DHT11 sensor reading.

## GET /api/history

Returns the rolling history of the latest 30 DHT11 measurements.

## POST /api/analyze

Sends the latest physical environmental measurements to the locally
running Llama 3.2 model through Ollama and returns the generated
environmental analysis.

------------------------------------------------------------------------

# 12. Sensor Data Validation

The Flask backend validates incoming DHT11 measurements before storing
them.

The expected ranges used by the current application are:

``` text
Temperature: 0 °C to 50 °C
Humidity:    20 % to 90 %
```

Invalid or non-numeric values are rejected by the REST API.

------------------------------------------------------------------------

# 13. Sensor History

The Flask backend stores a rolling history of the latest:

``` text
30 readings
```

When the history exceeds 30 measurements, the oldest measurement is
removed.

This rolling history is used by the Web dashboard to display the
real-time environmental chart.

------------------------------------------------------------------------

# 14. Install the Python Environment

A dedicated Conda environment can be created for the Flask and GenAI
components.

Open Anaconda Prompt:

``` text
conda create -n iot_genai_env python=3.12 -y
```

Activate it:

``` text
conda activate iot_genai_env
```

Install the required packages:

``` text
pip install flask ollama
```

Verify the installation:

``` text
python -c "import flask, ollama; print('Project environment ready')"
```

Expected output:

``` text
Project environment ready
```

------------------------------------------------------------------------

# 15. Install Ollama

The Generative AI component requires Ollama to be installed on the
computer.

After installing Ollama, verify the installation:

``` text
ollama --version
```

------------------------------------------------------------------------

# 16. Install Llama 3.2

The project uses the Llama 3.2 model locally through Ollama.

Download the model:

``` text
ollama pull llama3.2
```

Verify the installed models:

``` text
ollama list
```

The list should contain:

``` text
llama3.2
```

The model can also be tested directly:

``` text
ollama run llama3.2
```

Exit the interactive session with:

``` text
/bye
```

Ollama and Llama 3.2 must already be installed before using the GenAI
Environmental Assistant.

------------------------------------------------------------------------

# 17. Run the Flask Backend

Open the project root folder in Visual Studio Code.

Activate the Python environment:

``` text
conda activate iot_genai_env
```

From the project root, run:

``` text
python backend\app.py
```

The Flask development server uses:

``` text
Host: 0.0.0.0
Port: 5000
```

The `0.0.0.0` binding allows compatible devices on the local network,
including the ESP8266, to reach the Flask application through the
computer's network IP address.

Keep the Flask terminal running.

------------------------------------------------------------------------

# 18. Prepare the ESP8266

Install MicroPython on the ESP8266 if it is not already installed.

Open the ESP8266 program:

``` text
esp8266/main.py
```

Before transferring/running the program, configure locally:

``` python
WIFI_SSID = "YOUR_WIFI_NAME"
WIFI_PASSWORD = "YOUR_WIFI_PASSWORD"

SERVER_URL = "http://YOUR_LAPTOP_IP:5000/api/sensor"
```

The Wi-Fi network/hotspot used by the ESP8266 must allow it to
communicate with the laptop running Flask.

------------------------------------------------------------------------

# 19. Run the ESP8266 Program

Using Thonny or another compatible MicroPython environment:

1.  Connect the ESP8266 to the computer using a USB cable.
2.  Select the appropriate MicroPython interpreter and serial port.
3.  Open `esp8266/main.py`.
4.  Configure the Wi-Fi credentials and Flask server IP locally.
5.  Run or transfer the program to the ESP8266.

When the connection succeeds, the terminal should report the Wi-Fi
connection and the ESP8266 network information.

The program then begins reading the DHT11 sensor and sending
measurements to Flask.

------------------------------------------------------------------------

# 20. Open the Web Dashboard

After the Flask backend is running, open a modern Web browser.

On the computer running Flask, open:

``` text
http://127.0.0.1:5000
```

The dashboard displays:

-   Connection status
-   Current temperature
-   Current humidity
-   Environmental status
-   Data source
-   Latest-reading time
-   Temperature and humidity history
-   Latest 30 readings
-   GenAI Environmental Assistant

The frontend automatically requests the latest information from the
Flask backend, so the dashboard can update without manually refreshing
the page.

------------------------------------------------------------------------

# 21. Real-Time Chart

The application uses **Chart.js 4.5.1**.

The library is stored locally at:

``` text
static/js/chart.umd.min.js
```

The chart displays the historical DHT11 measurements collected by the
backend.

It contains:

``` text
X-axis       → Time
Left Y-axis  → Temperature (°C)
Right Y-axis → Humidity (%)
```

The chart maintains a rolling visualization of the latest 30
measurements.

------------------------------------------------------------------------

# 22. GenAI Environmental Assistant

The dashboard contains a:

``` text
GenAI Environmental Assistant
```

When the user clicks:

``` text
Analyze Current Environment
```

the frontend requests an analysis from:

``` text
POST /api/analyze
```

The Flask backend retrieves the latest physical DHT11 values and sends
them to:

``` text
Ollama
   ↓
Llama 3.2
```

The model generates three sections:

``` text
Environmental Condition

Analysis

Recommendation
```

The response is then displayed on the Web dashboard.

------------------------------------------------------------------------

# 23. Local Generative AI

Llama 3.2 is executed locally through Ollama.

The environmental sensor measurements therefore do not need to be sent
to a cloud-based LLM for the GenAI analysis implemented in this project.

The architecture is:

``` text
DHT11 Reading
      │
      ▼
Flask Backend
      │
      ▼
Ollama
      │
      ▼
Llama 3.2
      │
      ▼
Environmental Condition
Analysis
Recommendation
```

------------------------------------------------------------------------

# 24. Normal Startup Procedure

Each time the complete real-hardware project is used, follow this
general order.

## Step 1 --- Connect the Hardware

Connect:

``` text
DHT11
  ↓
ESP8266
  ↓
USB / Power
```

Make sure the ESP8266 and Flask computer can use the required local
network.

## Step 2 --- Start Flask

``` text
conda activate iot_genai_env
python backend\app.py
```

## Step 3 --- Start the ESP8266 Program

Run:

``` text
esp8266/main.py
```

using the MicroPython environment on the ESP8266.

## Step 4 --- Open the Dashboard

``` text
http://127.0.0.1:5000
```

## Step 5 --- Observe Real-Time Measurements

Verify that:

-   Temperature updates
-   Humidity updates
-   Data source shows DHT11 + ESP8266
-   Last-reading time changes
-   History chart receives new measurements

## Step 6 --- Run GenAI Analysis

Click:

``` text
Analyze Current Environment
```

The latest physical sensor values will be analyzed locally by Llama 3.2
through Ollama.

------------------------------------------------------------------------

# 25. Application Architecture

``` text
                    REAL ENVIRONMENT
                           │
                           ▼
                    ┌────────────┐
                    │   DHT11    │
                    │   Sensor   │
                    └─────┬──────┘
                          │
                          │ Temperature
                          │ Humidity
                          ▼
                    ┌────────────┐
                    │  ESP8266   │
                    │ MicroPython│
                    └─────┬──────┘
                          │
                          │ Wi-Fi
                          │ HTTP POST + JSON
                          ▼
                    ┌────────────┐
                    │   Flask    │
                    │ REST API   │
                    └─────┬──────┘
                          │
              ┌───────────┼────────────┐
              │           │            │
              ▼           ▼            ▼
         /api/sensor  /api/history  /api/analyze
              │           │            │
              ▼           ▼            ▼
         Latest Data  Last 30      Ollama
                      Readings          │
                          │             ▼
                          │         Llama 3.2
                          │             │
                          └──────┬──────┘
                                 ▼
                        Web Application
                                 │
                   ┌─────────────┼─────────────┐
                   ▼             ▼             ▼
              Live Values     Chart.js      GenAI
                                            Analysis
```

------------------------------------------------------------------------

# 26. Frontend Technologies

The Web interface uses:

``` text
HTML
CSS
JavaScript
Chart.js
```

The HTML template is located at:

``` text
templates/index.html
```

The CSS stylesheet is located at:

``` text
static/css/style.css
```

The application JavaScript is located at:

``` text
static/js/script.js
```

Chart.js is located at:

``` text
static/js/chart.umd.min.js
```

------------------------------------------------------------------------

# 27. Backend Technologies

The backend uses:

``` text
Python
Flask
Ollama Python package
```

The main backend file is:

``` text
backend/app.py
```

Flask handles:

-   Web page rendering
-   Sensor-data reception
-   Sensor-data validation
-   Latest-reading storage
-   Sensor history
-   REST API responses
-   Communication with Ollama
-   Llama 3.2 environmental analysis

------------------------------------------------------------------------

# 28. IoT Technologies

The physical IoT component uses:

``` text
DHT11
ESP8266
MicroPython
Wi-Fi
HTTP
JSON
```

The DHT11 measures the physical environment.

The ESP8266 retrieves the measurements and sends them over Wi-Fi to the
Flask REST API using HTTP and JSON.

------------------------------------------------------------------------

# 29. Security and GitHub Configuration

Do not commit actual Wi-Fi credentials to GitHub.

The public repository should keep:

``` python
WIFI_SSID = "WIFI_SSID"
WIFI_PASSWORD = "WIFI_PASSWORD"
```

The Flask server address should also remain generic:

``` python
SERVER_URL = "http://YOUR_LAPTOP_IP:5000/api/sensor"
```

Each user should replace these values locally before running the
physical ESP8266.

------------------------------------------------------------------------

# 30. Development Server Notice

The Flask server included in this project is configured as a development
server.

The current configuration is suitable for:

-   Local development
-   Laboratory demonstration
-   Classroom presentation
-   Local-network IoT experimentation

It should not be treated as a production Internet-facing deployment
without additional production configuration and security measures.

------------------------------------------------------------------------

# 31. Project Purpose

This project demonstrates the integration of three main areas:

### Internet of Things

Physical environmental measurements are collected using a DHT11 sensor
and ESP8266.

### Web Technologies

Flask, HTML, CSS, JavaScript, REST APIs, JSON, and Chart.js are used to
process and visualize the sensor data.

### Generative Artificial Intelligence

Ollama and Llama 3.2 interpret the physical sensor measurements and
generate natural-language environmental analysis and recommendations.

The project therefore demonstrates an end-to-end architecture:

``` text
Physical Sensor
      ↓
IoT Microcontroller
      ↓
Wireless Communication
      ↓
REST Backend
      ↓
Real-Time Web Visualization
      ↓
Local Generative AI Analysis
```

------------------------------------------------------------------------

# 32. Summary

The **Smart Environmental Monitoring and GenAI Assistant Using IoT**
combines real physical sensing with Web technologies and locally
executed Generative AI.

The DHT11 measures temperature and humidity, the ESP8266 collects and
transmits the measurements through Wi-Fi, Flask receives and manages the
sensor data, JavaScript and Chart.js provide real-time visualization,
and Llama 3.2 running locally through Ollama interprets the current
environmental conditions.

This demonstrates how **IoT and Generative AI can be integrated into a
single real-time environmental monitoring system**.
