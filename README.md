# 🌱 Secure Smart Agriculture Demo

A Docker-based demonstration of a secure smart agriculture monitoring system using MQTT, Node-RED, InfluxDB, and Grafana — built on Kali Linux as part of an EduQual Level 3 Diploma in Cloud Cyber Security.

---

## 📋 Overview

This project simulates a secure IoT pipeline for agricultural monitoring. Three Python-based sensor simulators publish realistic environmental data over a TLS-secured MQTT broker. The data flows through Node-RED for automation and alerting, gets stored in InfluxDB, and is visualized in real-time on a Grafana dashboard.

---

## 🏗️ System Architecture

IoT Sensors (Python)
↓ TLS Encrypted (Port 8883)
MQTT Broker (Mosquitto)
↓ Authenticated
Node-RED (Automation Engine)
↓
InfluxDB (Time-Series Database)
↓
Grafana (Live Dashboard)

---

## 🔧 Technologies Used

| Component | Technology | Version |
|-----------|------------|---------|
| MQTT Broker | Eclipse Mosquitto | 2.0 |
| Automation | Node-RED | Latest |
| Database | InfluxDB | 2.7 |
| Visualization | Grafana | Latest |
| Sensors | Python + paho-mqtt | 3.13 / 2.1.0 |
| Containers | Docker + Compose | 29.5.3 / v5.1.4 |

---

## 🔐 Security Features

- **TLS Encryption** — All MQTT communication encrypted in transit on port 8883
- **Custom CA & SAN Certificate** — Self-signed CA with Subject Alternative Names covering both `localhost` and `mosquitto`
- **Username/Password Authentication** — Broker requires credentials for all connections
- **Anonymous Access Blocked** — `allow_anonymous false` enforced in Mosquitto
- **Role-Based Access Control** — Grafana restricts dashboard access by user role
- **Sensitive File Protection** — Private keys, passwords, and certificates excluded from version control via `.gitignore`
- **Data Persistence** — Docker named volumes ensure data survives container restarts

---

## 📁 Project Structure

Secure-Smart-Agriculture-Demo/
├── docs/
│   └── architecture.md         # Detailed architecture documentation
├── grafana/
│   └── dashboards/             # Grafana dashboard configs
├── mqtt/
│   ├── certs/
│   │   ├── ca.crt              # Certificate Authority (generated locally)
│   │   ├── san.cnf             # SAN config for certificate generation
│   │   └── server.crt          # Server certificate (generated locally)
│   └── mosquitto.conf          # Broker configuration
├── node-red/
│   └── flows.json              # Node-RED automation flows
├── sensors/
│   ├── sensor_humidity.py      # Humidity simulator
│   ├── sensor_soil_moisture.py # Soil moisture simulator
│   └── sensor_temperature.py   # Temperature simulator
├── docker-compose.yml          # Docker services configuration
├── LICENSE                     # MIT Licence
└── README.md                   # Project documentation

---

## 🚀 Getting Started

### Prerequisites

- Docker and Docker Compose
- Python 3.x and pip
- OpenSSL

### 1. Clone the Repository

```bash
git clone https://github.com/osaid-amjad/Secure-Smart-Agriculture-Demo.git
cd Secure-Smart-Agriculture-Demo
```

### 2. Generate TLS Certificates

```bash
cd mqtt/certs
openssl genrsa -out ca.key 2048
openssl req -new -x509 -days 365 -key ca.key -out ca.crt \
  -subj "/C=PK/O=AgriSecure/CN=AgriSecure-CA"
openssl genrsa -out server.key 2048
openssl req -new -key server.key -out server.csr -config san.cnf
openssl x509 -req -days 365 -in server.csr -CA ca.crt -CAkey ca.key \
  -CAcreateserial -out server.crt -extensions v3_req -extfile san.cnf
cd ../..
```

### 3. Generate MQTT Password File

```bash
docker run --rm -it \
  -v $(pwd)/mqtt:/mosquitto/config \
  eclipse-mosquitto:2.0 \
  mosquitto_passwd -c /mosquitto/config/passwd agriconnect
```

Enter your chosen password when prompted.

### 4. Start the Docker Stack

```bash
docker compose up -d
```

Verify all containers are running:

```bash
docker compose ps
```

### 5. Set Up Python Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install paho-mqtt
```

### 6. Run the Sensors

Open three terminal tabs and run one sensor in each:

```bash
# Terminal 1 - Soil Moisture
python3 sensors/sensor_soil_moisture.py

# Terminal 2 - Temperature
python3 sensors/sensor_temperature.py

# Terminal 3 - Humidity
python3 sensors/sensor_humidity.py
```

Each sensor will confirm a secure TLS connection:

✓ Connected to MQTT Broker securely via TLS

---

## 🌐 Service Interfaces

| Service | URL | Default Credentials |
|---------|-----|-------------------|
| Node-RED | http://localhost:1880 | None required |
| InfluxDB | http://localhost:8086 | admin / AgriSecure2026 |
| Grafana | http://localhost:3000 | admin / AgriSecure2026 |

---

## 📊 Sensor Simulation Model

Each sensor uses a realistic sine wave model with environmental events and random glitches to simulate real agricultural conditions:

| Sensor | Cycle | Environmental Event | Glitch Type | Range |
|--------|-------|-------------------|-------------|-------|
| 🌱 Soil Moisture | 4 min | Irrigation (moisture spike) | Sensor dropout | 20–80% |
| 🌡️ Temperature | 3 min | Cool breeze (temp drop) | Electrical spike | 15–45°C |
| 💧 Humidity | 5 min | Misting or exhaust fan | Electrical spike | 30–90% |

---

## 📜 Licence

MIT Licence — see [LICENSE](LICENSE) for details.

---

## 👤 Author

**Osaid Amjad**
EduQual Level 3 Diploma in Cloud Cyber Security
Al Nafi International College
