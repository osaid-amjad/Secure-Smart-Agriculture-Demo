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
TOPIC = "agriculture/sensors/temperature"
CLIENT_ID = "temperature_sensor"
USERNAME = "agriconnect"
PASSWORD = "AgriSecure2026"
CA_CERT = "mqtt/certs/ca.crt"

# Event tracking variables
temp_event_offset = 0.0

def generate_temperature():
    """Simulate rapid temperature cycles with frequent drafts and glitches for short demos"""
    global temp_event_offset
    
    # --- DEMO ACTIVITY CONFIGURATION ---
    EVENT_CHANCE = 0.15   # 15% chance to trigger a draft event each loop
    GLITCH_CHANCE = 0.08  # 8% chance to trigger a single-point electrical spike
    DECAY_RATE = 1.0      # Warm back up by 1.0°C per loop (recovers in ~15-20 seconds)
    # ------------------------------------

    # 1. Base Sine Wave (3-minute cycle)
    cycle_seconds = 180 
    angle = (time.time() % cycle_seconds) / cycle_seconds * 2 * math.pi
    base_temp = 30.0
    amplitude = 10.0
    sine_value = base_temp + (amplitude * math.sin(angle))
    
    # 2. Environmental Event: Cool Breeze / Ventilation Draft
    if temp_event_offset == 0.0 and random.random() < EVENT_CHANCE:
        temp_event_offset = -random.uniform(3.0, 5.0)
    
    # Recover back to baseline
    if temp_event_offset < 0.0:
        temp_event_offset += DECAY_RATE
        if temp_event_offset > 0.0:
            temp_event_offset = 0.0
            
    # 3. Micro-jitter
    noise = random.uniform(-0.3, 0.3)
    
    # 4. Single-point Glitch (Electrical Spike)
    if random.random() < GLITCH_CHANCE:
        noise += random.choice([-2.5, 2.5])
        
    final_temp = sine_value + temp_event_offset + noise
    return round(max(15.0, min(45.0, final_temp)), 2)

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

    print(f"Starting Temperature Sensor (TLS Secured)...")
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
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    main()
