import paho.mqtt.client as mqtt
import time
import random
import json
from datetime import datetime

# MQTT Configuration
BROKER = "localhost"
PORT = 1883
TOPIC = "agriculture/sensors/humidity"
CLIENT_ID = "humidity_sensor"

def generate_humidity():
    """Simulate realistic agricultural humidity readings (0-100%)"""
    return round(random.uniform(30.0, 90.0), 2)

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

    print(f"Starting Humidity Sensor...")
    print(f"Publishing to topic: {TOPIC}")
    print("-" * 40)

    try:
        while True:
            humidity = generate_humidity()
            payload = json.dumps({
                "sensor_id": CLIENT_ID,
                "timestamp": datetime.now().isoformat(),
                "humidity_percent": humidity,
                "status": "low" if humidity < 40 else "optimal" if humidity < 70 else "high",
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
