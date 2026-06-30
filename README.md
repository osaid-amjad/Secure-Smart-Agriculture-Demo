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

```text
Secure-Smart-Agriculture-Demo/
├── docs/
│   └── architecture.md         # Detailed architecture documentation
├── grafana/
│   └── dashboards/
│       └── dashboard.json      # Grafana dashboard export
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
├── README.md                   # Project documentation
├── requirements.txt            # Python dependencies
└── SECURITY.md                 # Security policy and recommendations
```
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

Enter your chosen password when prompted. The default password used throughout this project (and in the sensor scripts below) is `AgriSecure2026`.

> **Important:** If you choose a different password here instead of the default `AgriSecure2026`, you must also update the `PASSWORD` field in **all three** sensor simulator files before running them:
> - `sensors/sensor_soil_moisture.py`
> - `sensors/sensor_temperature.py`
> - `sensors/sensor_humidity.py`

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
pip install -r requirements.txt
```

This installs all required Python dependencies automatically from `requirements.txt`.

### 6. Run the Sensors

Open three terminal tabs. In **each** tab, activate the virtual environment first, then run one sensor:

```bash
# Terminal 1 - Soil Moisture
source venv/bin/activate
python3 sensors/sensor_soil_moisture.py

# Terminal 2 - Temperature
source venv/bin/activate
python3 sensors/sensor_temperature.py

# Terminal 3 - Humidity
source venv/bin/activate
python3 sensors/sensor_humidity.py
```

> **Note:** `source venv/bin/activate` must be run in every new terminal tab/window before running a sensor script, since the virtual environment is not active by default in a new shell session.

Each sensor will confirm a secure TLS connection:

✓ Connected to MQTT Broker securely via TLS

---

## ⚙️ Post-Setup Configuration

This stack does not fully auto-provision on first run — a handful of one-time manual steps are required after `docker compose up -d`, because credentials/tokens (InfluxDB token, MQTT TLS cert upload) cannot be safely stored in version control. Follow these steps **in order**, in a fresh setup.

### A. Import the Node-RED Flow

1. Open Node-RED at `http://localhost:1880`
2. Click the **hamburger menu (☰)** in the top-right corner → **Import**
3. In the import dialog, click **"select a file to import"**
4. Navigate to and select `Secure-Smart-Agriculture-Demo/node-red/flows.json`
5. Click the red **Import** button → choose **import copy**
6. Click on the **Flow 1** tab at the top to open the imported flow

### B. Install the InfluxDB Node-RED Plugin

1. Click the **hamburger menu (☰)** → **Manage palette**
2. Go to the **Install** tab
3. Search for `influxdb`
4. Install **node-red-contrib-influxdb**
5. Click **Install**, then **Close** once finished

### C. Configure the MQTT Broker Connection (TLS)

1. Find the **"All Agriculture Sensors"** node, double-click it
2. Click the **pencil icon** next to **Server** ("Mosquitto Broker")
3. Go to the **Security** tab:
   - **Username:** `agriconnect`
   - **Password:** the password you set in Step 3 of Getting Started (default: `AgriSecure2026`)
4. Go to the **Connection** tab:
   - Change **Port** from `1883` to `8883`
   - Check **Use TLS**
   - Click the **+** icon next to the TLS pencil icon to add a new TLS configuration
   - Scroll down to **CA Certificate**, click **Upload**, and select `Secure-Smart-Agriculture-Demo/mqtt/certs/ca.crt`
   - **Uncheck** "Verify server certificate"
5. Click **Add** (top right) → **Update** → **Done**

The MQTT node should now show **"connected"** underneath it once deployed. ✅

### D. Get Your InfluxDB Token

1. Open a new tab and go to `http://localhost:8086`
2. Log in: username `admin`, password `AgriSecure2026`
3. Go to **Load Data** (left sidebar) → **API Tokens**
4. Find **admin's Token**, click the small **settings icon** next to it (beside Delete)
5. Click **Clone**
6. Copy the newly generated token to your clipboard

### E. Connect Node-RED to InfluxDB

1. Back in the Node-RED tab, double-click the **"Write to InfluxDB"** node
2. In **Server**, select **[v2.0] Write to InfluxDB**
3. Click the **pencil icon** next to it
4. Under **Properties → URL**, paste your copied token into the **Token** field
5. Click **Update** → **Done**
6. Click **Deploy** (top-right corner) to save and activate the entire flow

### F. Connect Grafana to InfluxDB

1. Open a new tab and go to `http://localhost:3000`
2. Log in: username `admin`, password `AgriSecure2026`
3. Click the **Main Menu (☰)** (top-left) → **Connections** → **Data sources**
4. Click **Add data source**, scroll down, and select **InfluxDB**
5. Set **Query language** to **Flux**
6. Set **URL** to `http://influxdb:8086`
7. Scroll to **Auth**:
   - Uncheck **Basic auth**
   - Check **Skip TLS Verify**
8. Scroll to **InfluxDB Details**:
   - **Organization:** `AgriSecure`
   - **Token:** paste the same token you copied in Step D
   - **Bucket:** `agriculture`
9. Click **Save & Test**

### G. Import the Grafana Dashboard

1. Scroll up and click **Build a dashboard** (top-right)
2. Click the **+** button (top-right) → **Import dashboard**
3. Click the upload area and select `Secure-Smart-Agriculture-Demo/grafana/dashboards/dashboard.json`
4. Click **Import**

### H. Fix the Time Range and Refresh Rate

1. Near the top of the dashboard, change the time range from **"Last 6 hours"** to **"Last 5 minutes"**
2. Click the dropdown arrow next to the **Refresh** button (just right of the time range) and select **Auto**

### I. Re-link Each Panel to the Datasource

For each panel/visualization on the dashboard:

1. Click the **three dots (⋮)** in the top-right corner of the panel
2. Click **Edit**
3. Click **Save** (top right) without making any changes
4. Click **Back to dashboard**

Repeat this for every panel on the dashboard. This step re-binds each panel's query to the newly imported datasource UID.

---

Once all steps (A–I) are complete, live sensor data should be flowing end-to-end: **Sensors → MQTT (TLS) → Node-RED → InfluxDB → Grafana**, fully visualized in real time.

> **Why are these manual steps needed?** The InfluxDB API token and the MQTT TLS certificate are security-sensitive and are regenerated fresh on every new setup — they cannot be safely committed to version control. As a result, the datasource token, the broker's TLS certificate, and each dashboard panel's datasource binding must be configured once per fresh installation.

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
