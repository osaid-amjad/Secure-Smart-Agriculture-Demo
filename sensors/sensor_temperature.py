import paho.mqtt.client as mqtt
import time
import random
import json
from datetime import datetime

# MQTT Configuration
BROKER = "localhost"
PORT = 1883
TOPIC = "agriculture/sensors/temperature"
CLIENT_ID = "temperature_sensor"

def generate_temperature():
    """Simulate realistic agricultural temperature readings (Celsius)"""
    return round(random.uniform(15.0, 45.0), 2)

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

    print(f"Starting Temperature Sensor...")
    print(f"Publishing to topic: {TOPIC}")
    print("-" * 40)

    try:
        while True:
            temperature = generate_temperature()
            payload = json.dumps({
                "sensor_id": CLIENT_ID,
                "timestamp": datetime.now().isoformat(),
                "temperature_celsius": temperature,
                "status": "cold" if temperature < 20 else "optimal" if temperature < 35 else "hot",
                "unit": "°C"
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
