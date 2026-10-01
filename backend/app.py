# ============================================================
# SMART ENVIRONMENTAL MONITORING + GENAI
# Real Hardware Version
#
# DHT11 → ESP8266 → Wi-Fi → Flask
#                       → Dashboard
#                       → History Chart
#                       → Ollama / Llama 3.2
# ============================================================

import ollama

from flask import Flask, jsonify, request, render_template
from datetime import datetime


# ============================================================
# FLASK APPLICATION CONFIGURATION
# ============================================================

app = Flask(
    __name__,
    template_folder="../templates",
    static_folder="../static"
)


# ============================================================
# LATEST REAL DHT11 SENSOR READING
# ============================================================

latest_sensor_data = {
    "temperature": None,
    "humidity": None,
    "timestamp": None,
    "source": None
}


# ============================================================
# SENSOR HISTORY
# Keep the latest 30 physical DHT11 readings
# ============================================================

sensor_history = []

MAX_HISTORY = 30


# ============================================================
# HOME ROUTE
# ============================================================

@app.route("/")
def home():

    return render_template("index.html")


# ============================================================
# POST /api/sensor
#
# Receive real DHT11 sensor data from ESP8266
# over Wi-Fi using HTTP POST.
# ============================================================

@app.route("/api/sensor", methods=["POST"])
def receive_sensor_data():

    data = request.get_json(silent=True)


    # --------------------------------------------------------
    # Validate JSON request
    # --------------------------------------------------------

    if not data:

        return jsonify({
            "error": "No JSON data received"
        }), 400


    if (
        "temperature" not in data or
        "humidity" not in data
    ):

        return jsonify({
            "error":
                "temperature and humidity are required"
        }), 400


    # --------------------------------------------------------
    # Convert sensor values to numbers
    # --------------------------------------------------------

    try:

        temperature = float(data["temperature"])
        humidity = float(data["humidity"])

    except (TypeError, ValueError):

        return jsonify({
            "error":
                "temperature and humidity must be numeric"
        }), 400


    # --------------------------------------------------------
    # Validate expected DHT11 measurement range
    # --------------------------------------------------------

    if temperature < 0 or temperature > 50:

        return jsonify({
            "error":
                "Temperature is outside the expected DHT11 range"
        }), 400


    if humidity < 20 or humidity > 90:

        return jsonify({
            "error":
                "Humidity is outside the expected DHT11 range"
        }), 400


    # --------------------------------------------------------
    # Update latest physical sensor reading
    # --------------------------------------------------------

    latest_sensor_data["temperature"] = temperature

    latest_sensor_data["humidity"] = humidity

    latest_sensor_data["timestamp"] = (
        datetime.now().isoformat(
            timespec="seconds"
        )
    )


    # --------------------------------------------------------
    # Identify physical IoT data source
    # --------------------------------------------------------

    latest_sensor_data["source"] = data.get(
        "source",
        "DHT11 + ESP8266"
    )


    # --------------------------------------------------------
    # Add reading to sensor history
    # --------------------------------------------------------

    sensor_history.append(
        latest_sensor_data.copy()
    )


    # --------------------------------------------------------
    # Keep only the latest 30 readings
    # --------------------------------------------------------

    if len(sensor_history) > MAX_HISTORY:

        sensor_history.pop(0)


    # --------------------------------------------------------
    # Display received data in Flask terminal
    # --------------------------------------------------------

    print("\nReal DHT11 sensor data received:")

    print(latest_sensor_data)

    print(
        f"Sensor history: "
        f"{len(sensor_history)}/"
        f"{MAX_HISTORY} readings"
    )


    # --------------------------------------------------------
    # Send confirmation back to ESP8266
    # --------------------------------------------------------

    return jsonify({

        "message":
            "DHT11 sensor data received successfully",

        "data":
            latest_sensor_data

    }), 200


# ============================================================
# GET /api/sensor
#
# Return latest real DHT11 sensor reading
# ============================================================

@app.route("/api/sensor", methods=["GET"])
def get_sensor_data():

    return jsonify(
        latest_sensor_data
    ), 200


# ============================================================
# GET /api/history
#
# Return latest 30 DHT11 readings for
# real-time temperature and humidity chart
# ============================================================

@app.route("/api/history", methods=["GET"])
def get_sensor_history():

    return jsonify({

        "count":
            len(sensor_history),

        "max_history":
            MAX_HISTORY,

        "readings":
            sensor_history

    }), 200


# ============================================================
# POST /api/analyze
#
# Analyze latest physical DHT11 reading
# using local Ollama + Llama 3.2
# ============================================================

@app.route("/api/analyze", methods=["POST"])
def analyze_environment():

    temperature = latest_sensor_data["temperature"]
    humidity = latest_sensor_data["humidity"]


    # --------------------------------------------------------
    # Real DHT11 data must exist before GenAI analysis
    # --------------------------------------------------------

    if (
        temperature is None or
        humidity is None
    ):

        return jsonify({
            "error":
                "No DHT11 sensor data available for analysis"
        }), 400


    # --------------------------------------------------------
    # Prompt sent to local Llama 3.2
    # --------------------------------------------------------

    prompt = f"""
You are an intelligent environmental monitoring assistant
integrated with a real IoT environmental monitoring system.

The following values were measured by a physical DHT11 sensor
connected to an ESP8266 microcontroller.

Current DHT11 sensor readings:

Temperature: {temperature:.1f} °C
Humidity: {humidity:.1f} %

Analyze the current environmental conditions.

Provide a concise response with exactly these sections:

Environmental Condition:
Give a short description of the overall condition.

Analysis:
Briefly explain what the measured temperature and humidity
indicate.

Recommendation:
Give one practical recommendation based on the readings.

Keep the response concise, clear, and suitable for display
on a smart environmental monitoring dashboard.
"""


    try:

        # ----------------------------------------------------
        # Send real environmental data to local Llama 3.2
        # ----------------------------------------------------

        response = ollama.chat(

            model="llama3.2",

            messages=[

                {
                    "role": "system",

                    "content":
                        "You are an IoT environmental "
                        "monitoring assistant."
                },

                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )


        # ----------------------------------------------------
        # Extract Llama 3.2 response
        # ----------------------------------------------------

        analysis = (
            response["message"]["content"].strip()
        )


        # ----------------------------------------------------
        # Display GenAI status in Flask terminal
        # ----------------------------------------------------

        print(
            "\nGenAI environmental analysis generated "
            "from real DHT11 data."
        )

        print(
            f"Temperature: {temperature:.1f} °C | "
            f"Humidity: {humidity:.1f} %"
        )


        # ----------------------------------------------------
        # Return analysis to dashboard
        # ----------------------------------------------------

        return jsonify({

            "temperature":
                temperature,

            "humidity":
                humidity,

            "source":
                latest_sensor_data["source"],

            "model":
                "llama3.2",

            "analysis":
                analysis

        }), 200


    except Exception as error:

        print(
            f"\nOllama error: {error}"
        )

        return jsonify({

            "error":
                "Unable to generate AI analysis. "
                "Make sure Ollama and Llama 3.2 "
                "are available."

        }), 500


# ============================================================
# START FLASK DEVELOPMENT SERVER
#
# 0.0.0.0 allows the ESP8266 and other devices connected
# to the same phone hotspot / local network to reach Flask.
# ============================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )