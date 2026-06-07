import paho.mqtt.client as mqtt
import time
import random
import json
from datetime import datetime

# MQTT Configuration
BROKER = "localhost"
PORT = 1883
TOPIC = "agriculture/sensors/soil_moisture"
CLIENT_ID = "soil_moisture_sensor"

def generate_soil_moisture():
    """Simulate realistic soil moisture readings (0-100%)"""
    return round(random.uniform(20.0, 80.0), 2)

def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("✓ Connected to MQTT Broker successfully")
    else:
        print(f"✗ Connection failed with code {rc}")

def main():
    # Create MQTT client
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, CLIENT_ID)
    client.on_connect = on_connect

    # Connect to broker
    client.connect(BROKER, PORT, 60)
    client.loop_start()

    print(f"Starting Soil Moisture Sensor...")
    print(f"Publishing to topic: {TOPIC}")
    print("-" * 40)

    try:
        while True:
            moisture = generate_soil_moisture()
            payload = json.dumps({
                "sensor_id": CLIENT_ID,
                "timestamp": datetime.now().isoformat(),
                "moisture_percent": moisture,
                "status": "dry" if moisture < 30 else "optimal" if moisture < 60 else "wet",
                "unit": "%"
            })

            client.publish(TOPIC, payload, qos=1)
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Published: {payload}")

            time.sleep(5)

    except KeyboardInterrupt:
        print("\nSensor stopped by user")
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    main()

