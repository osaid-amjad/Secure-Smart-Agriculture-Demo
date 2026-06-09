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
TOPIC = "agriculture/sensors/soil_moisture"
CLIENT_ID = "soil_moisture_sensor"
USERNAME = "agriconnect"
PASSWORD = "AgriSecure2026"
CA_CERT = "mqtt/certs/ca.crt"

# Event tracking variables
moisture_event_offset = 0.0

def generate_soil_moisture():
    """Simulate soil moisture with frequent watering events and glitches for short demos"""
    global moisture_event_offset
    
    # --- DEMO ACTIVITY CONFIGURATION ---
    EVENT_CHANCE = 0.15   # 15% chance to trigger watering event
    GLITCH_CHANCE = 0.08  # 8% chance to trigger a momentary complete drop
    DECAY_RATE = 3.0      # Dries back out by 3% per loop (recovers in ~25-40 seconds)
    # ------------------------------------

    # 1. Base Sine Wave (4-minute cycle)
    cycle_seconds = 240 
    angle = (time.time() % cycle_seconds) / cycle_seconds * 2 * math.pi
    base_moisture = 50.0
    amplitude = 20.0
    sine_value = base_moisture + (amplitude * math.sin(angle))
    
    # 2. Environmental Event: Watering / Irrigation
    if moisture_event_offset == 0.0 and random.random() < EVENT_CHANCE:
        moisture_event_offset = random.uniform(15.0, 25.0)
        
    # Recover back to baseline
    if moisture_event_offset > 0.0:
        moisture_event_offset -= DECAY_RATE
        if moisture_event_offset < 0.0:
            moisture_event_offset = 0.0
            
    # 3. Micro-jitter
    noise = random.uniform(-0.5, 0.5)
    
    # 4. Single-point Glitch (Complete sensor dropout)
    if random.random() < GLITCH_CHANCE:
        noise -= random.uniform(8.0, 15.0)
        
    final_moisture = sine_value + moisture_event_offset + noise
    return round(max(20.0, min(80.0, final_moisture)), 2)

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

    print(f"Starting Soil Moisture Sensor (TLS Secured)...")
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
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    main()
