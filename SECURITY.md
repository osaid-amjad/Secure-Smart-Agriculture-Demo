# 🔐 Security Policy

## Important Notice

This project is a **demonstration environment** built for educational purposes as part of an EduQual Level 3 Diploma in Cloud Cyber Security. It is not intended for production deployment without significant security hardening.

---

## ⚠️ Default Credentials

This demo uses default credentials that **must** be changed before any production use:

| Service | Default Username | Default Password |
|---------|-----------------|-----------------|
| Grafana | admin | AgriSecure2026 |
| InfluxDB | admin | AgriSecure2026 |
| MQTT Broker | agriconnect | (set during setup) |

---

## 🔒 Security Controls Implemented

- **TLS 1.3 Encryption** — All MQTT communication encrypted in transit
- **Self-Signed Certificates** — Custom CA with SAN certificate
- **Authentication** — Username/password required for all connections
- **Anonymous Access Blocked** — `allow_anonymous false` enforced
- **Sensitive Files Excluded** — Private keys and passwords excluded via `.gitignore`
- **Role-Based Access** — Grafana user sign-up disabled

---

## ⚡ Production Recommendations

Before deploying in any real environment:

1. **Replace self-signed certificates** with certificates from a trusted CA
2. **Change all default passwords** to strong unique passwords
3. **Store credentials** in environment variables or a secrets manager — never hardcode them
4. **Enable HTTPS** on Grafana and InfluxDB interfaces
5. **Restrict network access** — expose only necessary ports
6. **Enable audit logging** across all services
7. **Implement certificate rotation** policy
8. **Add intrusion detection** monitoring

---

## 📋 Reporting Issues

This is an educational project. If you find security issues relevant to the concepts demonstrated, feel free to open a GitHub issue.

---

## 📜 Disclaimer

This demo environment is provided as-is for educational purposes. The author accepts no responsibility for any use of this project outside its intended educational context.
