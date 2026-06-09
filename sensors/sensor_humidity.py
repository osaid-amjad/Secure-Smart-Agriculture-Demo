import paho.mqtt.client as mqtt
import time
import random
import json
import ssl
import math
from datetime import datetime

# MQTT Configuration
BROKER = "localhost"
PORT = 8883
TOPIC = "agriculture/sensors/humidity"
CLIENT_ID = "humidity_sensor"
USERNAME = "agriconnect"
PASSWORD = "AgriSecure2026"
CA_CERT = "mqtt/certs/ca.crt"

# Event tracking variables
humidity_event_offset = 0.0

def generate_humidity():
    """Simulate humidity with frequent misting/ventilation changes and glitches for short demos"""
    global humidity_event_offset
    
    # --- DEMO ACTIVITY CONFIGURATION ---
    EVENT_CHANCE = 0.15   # 15% chance to trigger ventilation/misting
    GLITCH_CHANCE = 0.08  # 8% chance to trigger a sharp single-point spike
    DECAY_RATE = 2.0      # Normalizes by 2% per loop (recovers in ~20-30 seconds)
    # ------------------------------------

    # 1. Base Sine Wave (5-minute cycle)
    cycle_seconds = 300 
    angle = (time.time() % cycle_seconds) / cycle_seconds * 2 * math.pi
    base_humidity = 60.0
    amplitude = 25.0
    sine_value = base_humidity + (amplitude * math.sin(angle))
    
    # 2. Environmental Event: Ventilation or Misting
    if humidity_event_offset == 0.0 and random.random() < EVENT_CHANCE:
        if random.random() < 0.5:
            humidity_event_offset = -random.uniform(10.0, 15.0)  # Exhaust Fan
        else:
            humidity_event_offset = random.uniform(10.0, 15.0)   # Misting
            
    # Recover back to baseline
    if humidity_event_offset > 0.0:
        humidity_event_offset -= DECAY_RATE
        if humidity_event_offset < 0.0:
            humidity_event_offset = 0.0
    elif humidity_event_offset < 0.0:
        humidity_event_offset += DECAY_RATE
        if humidity_event_offset > 0.0:
            humidity_event_offset = 0.0
            
    # 3. Micro-jitter
    noise = random.uniform(-0.4, 0.4)
    
    # 4. Single-point Glitch (Electrical spike)
    if random.random() < GLITCH_CHANCE:
        noise += random.choice([-5.0, 5.0])
        
    final_humidity = sine_value + humidity_event_offset + noise
    return round(max(30.0, min(90.0, final_humidity)), 2)

def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("✓ Connected to MQTT Broker securely via TLS")
    else:
        print(f"✗ Connection failed with code {rc}")

def main():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, CLIENT_ID)
    client.on_connect = on_connect
    client.tls_set(ca_certs=CA_CERT, tls_version=ssl.PROTOCOL_TLSv1_2)
    client.username_pw_set(USERNAME, PASSWORD)
    client.connect(BROKER, PORT, 60)
    client.loop_start()

    print(f"Starting Humidity Sensor (TLS Secured)...")
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
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    main()
