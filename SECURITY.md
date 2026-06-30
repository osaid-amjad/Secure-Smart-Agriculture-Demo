# 🔐 Security Policy

## ⚠️ EDUCATIONAL DEMO ONLY — NOT FOR PRODUCTION USE

> **This project is strictly a learning and demonstration environment.**
> It was built as part of an EduQual Level 3 Diploma in Cloud Cyber Security to demonstrate secure architecture *concepts* for an IoT-based smart agriculture system.
>
> **It is NOT production-ready, NOT hardened for real deployment, and MUST NOT be used to handle real sensor data, real biotechnology research data, or any data of actual value.**
>
> Default credentials, self-signed certificates, and locally-stored tokens are used throughout this project **intentionally and only** for demonstration purposes. Deploying this project as-is in any real-world, production, or internet-facing environment would be insecure.

---

## 📋 Overview

This repository demonstrates how a secure IoT-to-dashboard pipeline *can* be architected — covering encryption in transit, authentication, access control, and data integrity concepts — using MQTT, Node-RED, InfluxDB, and Grafana. The goal is to illustrate security **principles and design decisions**, not to provide a deployable, hardened product.

---

## 🔒 Security Controls Implemented (For Demonstration)

### Network & Transport Security
- **TLS 1.2/1.3 Encryption** — All MQTT communication between sensors and the broker is encrypted in transit on port 8883
- **Custom CA & SAN Certificate** — A self-signed Certificate Authority issues a server certificate with Subject Alternative Names covering both `localhost` and `mosquitto`
- **Trust Boundary Enforcement** — The architecture separates an unsecured Field/Edge Zone from a secured Cloud Zone, with TLS enforced at the boundary

### Authentication & Access Control
- **Username/Password Authentication** — The MQTT broker requires credentials for every client connection
- **Anonymous Access Blocked** — `allow_anonymous false` is enforced in the Mosquitto configuration
- **Role-Based Access Control (RBAC)** — Grafana restricts dashboard and data source access by user role
- **Grafana Sign-Up Disabled** — Public self-registration is disabled (`GF_USERS_ALLOW_SIGN_UP=false`)

### Data Integrity & Confidentiality
- **Data Integrity Verification (Conceptual)** — The architecture demonstrates hash-based verification of data as it moves from sensor to broker to database
- **Read-Only Audit Principles** — The design illustrates how logs and stored sensor data should be treated as read-only / tamper-evident in a real system

### Operational Hygiene
- **Sensitive File Exclusion** — Private keys, passwords, and certificates are excluded from version control via `.gitignore`
- **Documented Manual Setup** — Tokens and certificates are intentionally excluded from the repository and must be generated/entered manually per installation (see `README.md`), rather than committed or hardcoded

---

## ⚠️ Default Credentials (Demo Only)

This demo intentionally uses hardcoded default credentials for ease of setup and grading/demonstration purposes. **These must never be reused, exposed publicly, or carried into any real deployment:**

| Service | Default Username | Default Password |
|---------|-----------------|-----------------|
| Grafana | admin | AgriSecure2026 |
| InfluxDB | admin | AgriSecure2026 |
| MQTT Broker | agriconnect | (set during setup) |

---

## 🚫 What This Project Does NOT Provide

To be explicit, this project does **not** include or guarantee any of the following, all of which would be required before any real-world use:

- Certificates issued by a trusted, publicly-recognized Certificate Authority
- Secrets management (all tokens/passwords here are stored in plaintext config for demo simplicity)
- Network hardening, firewalling, or restricted port exposure
- Intrusion detection or anomaly monitoring
- Horizontal scaling, redundancy, or high-availability configuration
- Penetration testing or formal security auditing
- Compliance certification of any kind (ISO/IEC 27001, NIST, FAO, OECD, etc. are referenced conceptually in project documentation, not implemented or certified here)

---

## ⚡ If You Wanted to Adapt This for Real Use (Not Recommended Without Major Changes)

This list is provided purely for educational completeness — to illustrate the *gap* between a demo and a production system, not as a guarantee that following it makes the project production-safe:

1. Replace all self-signed certificates with certificates from a trusted CA
2. Replace every default password with strong, unique, randomly-generated secrets
3. Store all credentials in a proper secrets manager or environment variables — never in version control or plaintext config
4. Enable HTTPS on Grafana and InfluxDB web interfaces
5. Restrict network access — expose only the minimum necessary ports, behind a firewall/VPN
6. Enable full audit logging across all services
7. Implement a certificate rotation policy
8. Add intrusion detection and anomaly monitoring
9. Conduct formal security review and penetration testing before going anywhere near real data

---

## 📋 Reporting Issues

This is an educational project, not a maintained security product. If you notice an issue relevant to the security concepts being demonstrated, feel free to open a GitHub issue for discussion.

---

## 📜 Disclaimer

This repository is provided **as-is, for educational demonstration purposes only**, as part of a diploma coursework submission. It is explicitly **not intended, designed, audited, or warranted for production, commercial, or real-world deployment of any kind**. The author accepts no responsibility for any use of this project outside its intended educational context.
