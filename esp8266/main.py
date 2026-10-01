# ============================================================
# Smart Environmental Monitoring and GenAI Assistant Using IoT
# REAL HARDWARE VERSION
#
# DHT11 → ESP8266 → Wi-Fi → Flask → Dashboard
#                              → Chart
#                              → Ollama / Llama 3.2
#
# Board  : ESP8266
# Sensor : DHT11
# Language: MicroPython
# ============================================================

import machine
import dht
import network
import time
import urequests


# ============================================================
# 1. WI-FI CONFIGURATION
# ============================================================

# Replace these two values with YOUR phone hotspot details.

WIFI_SSID = "WIFI_SSID"
WIFI_PASSWORD = "WIFI_PASSWORD"


# ============================================================
# 2. FLASK SERVER CONFIGURATION
# ============================================================

# Current laptop IPv4 address on the phone hotspot.
#
# IMPORTANT:
# If the laptop receives a different IPv4 address later,
# run "ipconfig" again and update this URL.

SERVER_URL = "http://YOUR_LAPTOP_IP:5000/api/sensor"


# ============================================================
# 3. DHT11 CONFIGURATION
# ============================================================

# DHT11 DATA pin connected to ESP8266 GPIO4.
#
# On many NodeMCU boards:
# GPIO4 = D2

DHT_PIN = 4

dht_sensor = dht.DHT11(
    machine.Pin(DHT_PIN)
)


# ============================================================
# 4. CONNECT ESP8266 TO WI-FI
# ============================================================

def connect_wifi():

    wlan = network.WLAN(network.STA_IF)

    # Enable station mode
    wlan.active(True)

    # Check whether ESP8266 is already connected
    if wlan.isconnected():

        print("Wi-Fi already connected.")
        print("ESP8266 IP:", wlan.ifconfig()[0])

        return wlan

    print()
    print("Connecting ESP8266 to Wi-Fi...")
    print("SSID:", WIFI_SSID)

    wlan.connect(
        WIFI_SSID,
        WIFI_PASSWORD
    )

    # Wait for connection
    timeout = 20

    while not wlan.isconnected() and timeout > 0:

        print("Connecting...")
        time.sleep(1)

        timeout -= 1

    # Check connection result
    if wlan.isconnected():

        print()
        print("Wi-Fi connected successfully.")

        network_info = wlan.ifconfig()

        print("ESP8266 IP:", network_info[0])
        print("Subnet Mask:", network_info[1])
        print("Gateway:", network_info[2])

    else:

        print()
        print("Wi-Fi connection failed.")

    return wlan


# ============================================================
# 5. SEND SENSOR DATA TO FLASK
# ============================================================

def send_sensor_data(temperature, humidity):

    # JSON data expected by Flask /api/sensor
    sensor_data = {
        "temperature": temperature,
        "humidity": humidity,
        "source": "DHT11 + ESP8266"
    }

    response = None

    try:

        print()
        print("Sending data to Flask...")

        response = urequests.post(
            SERVER_URL,
            json=sensor_data
        )

        print(
            "HTTP Status:",
            response.status_code
        )

        # Flask normally returns JSON confirming
        # that the reading was received.
        print(
            "Flask Response:",
            response.text
        )

        if response.status_code == 200:

            print(
                "Sensor data sent successfully."
            )

        else:

            print(
                "Flask returned an error."
            )

    except Exception as error:

        print()
        print(
            "Failed to send data to Flask:"
        )

        print(error)

    finally:

        # Always close the HTTP response
        # to release ESP8266 memory.
        if response is not None:

            response.close()


# ============================================================
# 6. START WI-FI CONNECTION
# ============================================================

wifi = connect_wifi()


# ============================================================
# 7. START DHT11 MONITORING
# ============================================================

print()
print("============================================")
print("DHT11 + ESP8266 Environmental Monitoring")
print("============================================")

print("DHT11 Pin: GPIO4")
print("Flask Server:", SERVER_URL)

print("============================================")


reading = 1


# ============================================================
# 8. MAIN LOOP
# ============================================================

while True:

    try:

        # ----------------------------------------------------
        # Reconnect Wi-Fi if connection was lost
        # ----------------------------------------------------

        if not wifi.isconnected():

            print()
            print("Wi-Fi connection lost.")

            wifi = connect_wifi()

        # ----------------------------------------------------
        # Read DHT11 sensor
        # ----------------------------------------------------

        dht_sensor.measure()

        temperature = dht_sensor.temperature()
        humidity = dht_sensor.humidity()

        # ----------------------------------------------------
        # Display reading in Thonny Shell
        # ----------------------------------------------------

        print()
        print("--------------------------------------------")

        print(
            "Reading",
            reading
        )

        print(
            "Temperature:",
            temperature,
            "°C"
        )

        print(
            "Humidity:",
            humidity,
            "%"
        )

        # ----------------------------------------------------
        # Send reading to Flask
        # ----------------------------------------------------

        if wifi.isconnected():

            send_sensor_data(
                temperature,
                humidity
            )

        else:

            print(
                "No Wi-Fi connection. "
                "Reading not sent."
            )

        reading += 1


    except OSError as error:

        print()
        print(
            "Failed to read DHT11 sensor:"
        )

        print(error)


    except Exception as error:

        print()
        print(
            "Unexpected error:"
        )

        print(error)


    # --------------------------------------------------------
    # Wait before next reading
    # --------------------------------------------------------

    time.sleep(5)