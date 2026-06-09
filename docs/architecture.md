# 🏗️ System Architecture Documentation

## Secure Smart Agriculture Demo
**Author:** Osaid Amjad  
**Diploma:** EduQual Level 3 — Cloud Cyber Security  
**Institution:** Al Nafi International College  

---

## 1. Architecture Overview

This project implements a secure end-to-end IoT pipeline for agricultural monitoring. The architecture follows a layered design where each component has a specific role, and security controls are applied at every layer.

┌─────────────────────────────────────────────┐
│           FIELD LAYER                        │
│   🌱 Soil Moisture  🌡️ Temperature  💧 Humidity │
│        Python Sensor Simulators              │
└──────────────────┬──────────────────────────┘
│ TLS 1.3 Encrypted
│ Port 8883
│ Username/Password Auth
┌──────────────────▼──────────────────────────┐
│           BROKER LAYER                       │
│         Eclipse Mosquitto 2.0                │
│      MQTT Broker — Publish/Subscribe         │
└──────────────────┬──────────────────────────┘
│ Authenticated Internal
│ Docker Network
┌──────────────────▼──────────────────────────┐
│         AUTOMATION LAYER                     │
│              Node-RED                        │
│    Flow-based Automation & Alert Engine      │
└──────────────────┬──────────────────────────┘
│
┌──────────────────▼──────────────────────────┐
│          STORAGE LAYER                       │
│            InfluxDB 2.7                      │
│        Time-Series Database                  │
└──────────────────┬──────────────────────────┘
│
┌──────────────────▼──────────────────────────┐
│       VISUALIZATION LAYER                    │
│              Grafana                         │
│     Real-Time Dashboard & Monitoring         │
└─────────────────────────────────────────────┘

---

## 2. Component Details

### 2.1 Sensor Layer (Python Simulators)

Three Python scripts simulate realistic agricultural IoT sensors using a sine wave model with environmental events and random glitches.

| Sensor | Topic | Cycle | Events |
|--------|-------|-------|--------|
| Soil Moisture | `agriculture/sensors/soil_moisture` | 4 min | Irrigation spikes |
| Temperature | `agriculture/sensors/temperature` | 3 min | Cool breeze drops |
| Humidity | `agriculture/sensors/humidity` | 5 min | Misting/ventilation |

Each sensor publishes a JSON payload every 5 seconds:

```json
{
  "sensor_id": "soil_moisture_sensor",
  "timestamp": "2026-06-08T09:13:10.971092",
  "moisture_percent": 45.23,
  "status": "optimal",
  "unit": "%"
}
```

**Security controls applied:**
- TLS 1.3 encryption via `paho-mqtt` and Python `ssl` module
- Username/password authentication on every connection
- CA certificate verification to prevent man-in-the-middle attacks
- QoS level 1 to guarantee message delivery

---

### 2.2 Broker Layer (Eclipse Mosquitto)

Mosquitto acts as the central message routing hub using the publish-subscribe model.

**Configuration highlights:**
- Listens exclusively on port 8883 (TLS) — port 1883 disabled
- `allow_anonymous false` — all connections require credentials
- Password file uses Mosquitto's built-in hashing
- TLS configured with custom CA and SAN certificate
- Full logging enabled for monitoring and auditing

**SAN Certificate covers:**
- `localhost` — for Python sensors connecting from Kali host
- `mosquitto` — for Node-RED connecting from inside Docker network

---

### 2.3 Automation Layer (Node-RED)

Node-RED subscribes to all sensor topics using the `agriculture/sensors/#` wildcard and processes incoming data through three steps:

[MQTT In] → [JSON Parser] → [InfluxDB Out]
→ [Moisture Switch] → [Dry Soil Alert] → [Debug]
→ [Temperature Switch] → [Heat Alert] → [Debug]
→ [Humidity Switch] → [High Humidity Alert] → [Debug]

**Automation rules:**
| Condition | Threshold | Alert |
|-----------|-----------|-------|
| Soil Moisture | < 30% | Irrigation required |
| Temperature | > 35°C | Heat stress risk |
| Humidity | > 80% | Fungal disease risk |

---

### 2.4 Storage Layer (InfluxDB 2.7)

InfluxDB stores all sensor data as time-series measurements in the `agriculture` bucket.

**Configuration:**
- Organisation: `AgriSecure`
- Bucket: `agriculture`
- Retention: 1 week
- Authentication: API token required for all read/write operations

**Data structure:**

Measurement: sensor_data
Fields: moisture_percent, temperature_celsius, humidity_percent, status, unit
Tags: sensor_id, timestamp

---

### 2.5 Visualization Layer (Grafana)

Grafana connects to InfluxDB using the Flux query language and displays four panels:

| Panel | Type | Query Field |
|-------|------|-------------|
| Soil Moisture | Time Series | `moisture_percent` |
| Temperature | Arc Gauge | `temperature_celsius` |
| Humidity | Time Series | `humidity_percent` |
| Live Sensor Status | State Timeline | `status` |

**Security controls:**
- Admin authentication required
- User sign-up disabled (`GF_USERS_ALLOW_SIGN_UP=false`)
- Role-based access control enforced

---

## 3. Network Architecture

All services run inside a Docker bridge network (`secure-smart-agriculture-demo_default`). Container-to-container communication uses Docker DNS resolution — containers reference each other by name (e.g., `mosquitto`, `influxdb`, `grafana`).

┌─────────────────────────────────────────────────┐
│           Docker Bridge Network                  │
│                                                  │
│  ┌──────────┐    ┌──────────┐    ┌───────────┐  │
│  │ Mosquitto│    │ Node-RED │    │  InfluxDB │  │
│  │ :8883    │◄───│ :1880    │───►│  :8086    │  │
│  └──────────┘    └──────────┘    └─────┬─────┘  │
│                                        │         │
│                                  ┌─────▼─────┐  │
│                                  │  Grafana  │  │
│                                  │  :3000    │  │
│                                  └───────────┘  │
└─────────────────────────────────────────────────┘
▲
│ TLS 8883
│
┌───────┴──────────────────────────────────────────┐
│              Kali Linux Host                      │
│   sensor_soil_moisture.py                        │
│   sensor_temperature.py                          │
│   sensor_humidity.py                             │
└──────────────────────────────────────────────────┘

---

## 4. Security Architecture

### 4.1 Defence in Depth

Security is applied at every layer — no single point of failure:

| Layer | Control | Implementation |
|-------|---------|----------------|
| Transport | TLS Encryption | Mosquitto + OpenSSL |
| Authentication | Username/Password | Mosquitto passwd file |
| Certificate | CA Verification | Custom CA + SAN cert |
| Access Control | RBAC | Grafana user roles |
| Data | API Token Auth | InfluxDB tokens |
| Network | Isolation | Docker bridge network |
| Storage | Persistence | Named Docker volumes |

### 4.2 CIA Triad Mapping

| Principle | Implementation |
|-----------|---------------|
| **Confidentiality** | TLS encryption prevents data interception in transit |
| **Integrity** | QoS 1 guarantees delivery; anomaly detection flags invalid readings |
| **Availability** | `restart: unless-stopped` ensures services recover automatically |

### 4.3 Certificate Infrastructure

AgriSecure-CA (ca.crt / ca.key)
│
└── Signs ──► mqtt_broker (server.crt / server.key)
SAN: localhost, mosquitto, 127.0.0.1

---

## 5. Data Flow

1. Python sensor generates reading every 5 seconds
2. Payload serialized as JSON
3. Published to MQTT topic over TLS on port 8883
4. Mosquitto broker receives, authenticates, and routes message
5. Node-RED receives via wildcard subscription agriculture/sensors/#
6. JSON parser deserializes payload
7. Threshold switch checks values against alert rules
8. Alert triggered if threshold breached → debug output
9. Data written to InfluxDB agriculture bucket
10. Grafana queries InfluxDB every 5 seconds via Flux
11. Dashboard panels update with latest readings

---

## 6. Alignment with Global Standards

| Standard | Application in This Project |
|----------|-----------------------------|
| **ISO/IEC 27001** | Information security controls applied at every layer |
| **NIST CSF** | Identify → Protect → Detect → Respond → Recover mapped to architecture |
| **FAO Digital Agriculture** | Secure digital technology use in agricultural context |
| **OECD Biotechnology Principles** | Protection of agricultural research and sensor data |
