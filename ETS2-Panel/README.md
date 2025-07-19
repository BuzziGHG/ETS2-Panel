# ETS2 Server Panel - Complete Installation Package | Vollständiges Installationspaket

[🇺🇸 English](#english) | [🇩🇪 Deutsch](#deutsch)

---

## English

A modern, web-based administration panel for Euro Truck Simulator 2 Dedicated Servers, inspired by Pterodactyl Panel.

### 🚛 Overview

This package contains everything you need to install and operate a professional ETS2 Server Panel:

- **Automatic Installation Script** for one-click setup
- **Complete Backend** (Python/Flask) with REST API
- **Modern Frontend** (React/Tailwind CSS) with responsive design and **multilingual support**
- **HTTPS Support** with Let's Encrypt Integration
- **Comprehensive Documentation** with Troubleshooting Guide

### 🌐 Language Support

The panel now supports multiple languages:
- **German (Deutsch)** - Original language
- **English** - Full translation available
- **Language Selector** - Switch between languages in the interface

### 📁 Package Contents

#### Installation Scripts
- `install-ets2-panel.sh` - Main installation script (automatic)
- `deploy-panel.sh` - Deployment script for updates
- `setup-https.sh` - HTTPS/SSL configuration

#### Backend (Python/Flask)
- `ets2-panel-backend/` - Complete Backend with API
  - User Authentication (JWT)
  - Server Management API
  - WebSocket for real-time updates
  - SQLite Database

#### Frontend (React)
- `ets2-panel-frontend/` - Modern React Application
  - Responsive Design
  - Dashboard with Real-time Monitoring
  - Server Management
  - User Management
  - **Multilingual Interface** (German/English)

#### Documentation
- `ETS2_Server_Panel_Guide_en.md` - Complete Guide in English (50+ pages)
- `ETS2_Server_Panel_Anleitung.md` - Complete Guide in German (50+ pages)
- `README.md` - This bilingual overview file

### 🚀 Quick Start

To install the ETS2 Server Panel, first clone the repository and then run the installation script:

```bash
git clone https://github.com/BuzziGHG/ETS2-Panel.git
cd ETS2-Panel
sudo bash install-ets2-panel.sh --panel-host yourdomain.com --enable-https y --le-email your-email@example.com --admin-username admin --admin-password your_secure_password --admin-email admin@yourdomain.com
```

**Note:** If you are using an IP address for `--panel-host`, set `--enable-https n` as HTTPS is not possible with IP addresses.

The script guides you through the configuration and automatically installs:
- All dependencies (Python, Node.js, Nginx)
- SteamCMD for ETS2 Server Management
- Backend and Frontend
- SSL Certificates (optional)
- Systemd Services

#### After Installation

1. **Access Panel:** `https://your-domain.com` or `http://your-server-ip`
2. **Login:** Default login is `admin` / `admin123`
3. **Change Password:** Immediately after the first login
4. **Select Language:** Use the language selector in the top navigation
5. **Create First Server:** Via the Dashboard

### 🔧 System Requirements

#### Minimal
- **OS:** Ubuntu 20.04+ or Debian 11+
- **RAM:** 2 GB
- **CPU:** 2 Cores
- **Storage:** 10 GB
- **Network:** Stable Internet Connection

#### Recommended
- **OS:** Ubuntu 22.04 LTS
- **RAM:** 4 GB or more
- **CPU:** 4 Cores or more
- **Storage:** 50 GB SSD
- **Network:** 100 Mbit/s or more

### 🌟 Features

#### Panel Features
- ✅ **Modern Dashboard** with Real-time Updates
- ✅ **Multi-Server Management** - Unlimited ETS2 Servers
- ✅ **User Management** with Role System
- ✅ **HTTPS Support** with Let's Encrypt
- ✅ **Responsive Design** for Desktop and Mobile
- ✅ **WebSocket Integration** for Live Updates
- ✅ **REST API** for Integrations
- ✅ **Multilingual Support** (German/English)

#### Server Management
- ✅ **One-Click Server Creation**
- ✅ **Start/Stop/Restart Control**
- ✅ **Real-time Monitoring**
- ✅ **Log Viewer**
- ✅ **Automatic Updates** via SteamCMD
- ✅ **Configuration Management**

#### Security
- ✅ **JWT Authentication**
- ✅ **bcrypt Password Hashing**
- ✅ **HTTPS Encryption**
- ✅ **CORS Protection**
- ✅ **Input Validation**
- ✅ **Firewall Integration**

### 📖 Documentation

The complete documentation is available in both languages:

**English:**
- `ETS2_Server_Panel_Guide_en.md` - Complete installation and operation guide

**German:**
- `ETS2_Server_Panel_Anleitung.md` - Vollständige Installations- und Bedienungsanleitung

Both guides contain:
1. **Detailed Installation Guide**
2. **System Requirements and Compatibility**
3. **Step-by-Step Configuration**
4. **HTTPS Setup with Let's Encrypt**
5. **Panel Operation and Features**
6. **Server Management Guide**
7. **Troubleshooting and FAQ**
8. **API Documentation**
9. **Development and Customization**

### 🔧 Manual Installation

For advanced setups or customizations, see the detailed guide in your preferred language.

### 🆘 Support and Troubleshooting

#### Common Issues
- **Installation fails:** Check root privileges and internet connection
- **Panel does not load:** Check service status and firewall
- **Servers do not start:** Check permissions and ports

#### Collect Debug Information
```bash
# Check service status
sudo systemctl status ets2-panel-backend
sudo systemctl status nginx

# View logs
sudo journalctl -u ets2-panel-backend -f
sudo tail -f /var/log/nginx/error.log
```

#### Community Support
- **GitHub Issues:** For bug reports and feature requests
- **Documentation:** Complete guide with FAQ in both languages
- **Discord/Forum:** Community discussions (Links in the documentation)

### 🔄 Updates and Maintenance

#### Update Panel
```bash
# Download latest version
git pull origin main

# Execute deployment script
./deploy-panel.sh
```

#### Create Backups
```bash
# Automatic backups are enabled by default
# Manual backups:
sudo tar -czf ets2-panel-backup-$(date +%Y%m%d).tar.gz /opt/ets2-panel /opt/ets2-servers
```

### 📄 License

MIT License - Free to use for private and commercial purposes.

### 🤝 Contribute

Contributions are welcome! See CONTRIBUTING.md for details.

### 📞 Contact
- **Author:** Simon Dialler
- **Version:** 1.0
- **Date:** July 2025

---

**Note:** This panel is an independent project and not officially supported by SCS Software.

---

## Deutsch

Ein modernes, webbasiertes Verwaltungspanel für Euro Truck Simulator 2 Dedicated Server, inspiriert von Pterodactyl Panel.

### 🚛 Überblick

Dieses Paket enthält alles, was Sie für die Installation und den Betrieb eines professionellen ETS2 Server Panels benötigen:

- **Automatisches Installationsskript** für One-Click-Setup
- **Vollständiges Backend** (Python/Flask) mit REST API
- **Modernes Frontend** (React/Tailwind CSS) mit responsivem Design und **mehrsprachiger Unterstützung**
- **HTTPS-Unterstützung** mit Let's Encrypt Integration
- **Umfassende Dokumentation** mit Troubleshooting-Guide

### 🌐 Sprachunterstützung

Das Panel unterstützt jetzt mehrere Sprachen:
- **Deutsch** - Originalsprache
- **English** - Vollständige Übersetzung verfügbar
- **Sprachauswahl** - Wechseln Sie zwischen Sprachen in der Benutzeroberfläche

### 📁 Paket-Inhalt

#### Installationsskripte
- `install-ets2-panel.sh` - Hauptinstallationsskript (automatisch)
- `deploy-panel.sh` - Deployment-Skript für Updates
- `setup-https.sh` - HTTPS/SSL-Konfiguration

#### Backend (Python/Flask)
- `ets2-panel-backend/` - Vollständiges Backend mit API
  - Benutzer-Authentifizierung (JWT)
  - Server-Management-API
  - WebSocket für Echtzeit-Updates
  - SQLite-Datenbank

#### Frontend (React)
- `ets2-panel-frontend/` - Moderne React-Anwendung
  - Responsive Design
  - Dashboard mit Echtzeit-Monitoring
  - Server-Verwaltung
  - Benutzer-Management
  - **Mehrsprachige Benutzeroberfläche** (Deutsch/English)

#### Dokumentation
- `ETS2_Server_Panel_Guide_en.md` - Vollständige Anleitung auf Englisch (50+ Seiten)
- `ETS2_Server_Panel_Anleitung.md` - Vollständige Anleitung auf Deutsch (50+ Seiten)
- `README.md` - Diese zweisprachige Übersichtsdatei

### 🚀 Schnellstart

Um das ETS2 Server Panel zu installieren, klonen Sie zuerst das Repository und führen Sie dann das Installationsskript aus:

```bash
git clone https://github.com/BuzziGHG/ETS2-Panel.git
cd ETS2-Panel
sudo bash install-ets2-panel.sh --panel-host ihre-domain.com --enable-https y --le-email ihre-email@example.com --admin-username admin --admin-password ihr_sicheres_passwort --admin-email admin@ihre-domain.com
```

**Hinweis:** Wenn Sie eine IP-Adresse für `--panel-host` verwenden, setzen Sie `--enable-https n`, da HTTPS mit IP-Adressen nicht möglich ist.

Das Skript führt Sie durch die Konfiguration und installiert automatisch:
- Alle Abhängigkeiten (Python, Node.js, Nginx)
- SteamCMD für ETS2 Server-Management
- Backend und Frontend
- SSL-Zertifikate (optional)
- Systemd-Services

#### Nach der Installation

1. **Panel aufrufen:** `https://ihre-domain.com` oder `http://ihre-server-ip`
2. **Anmelden:** Standard-Login ist `admin` / `admin123`
3. **Passwort ändern:** Sofort nach der ersten Anmeldung
4. **Sprache wählen:** Verwenden Sie die Sprachauswahl in der oberen Navigation
5. **Ersten Server erstellen:** Über das Dashboard

### 🔧 Systemanforderungen

#### Minimal
- **OS:** Ubuntu 20.04+ oder Debian 11+
- **RAM:** 2 GB
- **CPU:** 2 Kerne
- **Speicher:** 10 GB
- **Netzwerk:** Stabile Internetverbindung

#### Empfohlen
- **OS:** Ubuntu 22.04 LTS
- **RAM:** 4 GB oder mehr
- **CPU:** 4 Kerne oder mehr
- **Speicher:** 50 GB SSD
- **Netzwerk:** 100 Mbit/s oder mehr

### 🌟 Features

#### Panel-Features
- ✅ **Modernes Dashboard** mit Echtzeit-Updates
- ✅ **Multi-Server-Management** - Unbegrenzte ETS2-Server
- ✅ **Benutzer-Verwaltung** mit Rollen-System
- ✅ **HTTPS-Unterstützung** mit Let's Encrypt
- ✅ **Responsive Design** für Desktop und Mobile
- ✅ **WebSocket-Integration** für Live-Updates
- ✅ **REST API** für Integrationen
- ✅ **Mehrsprachige Unterstützung** (Deutsch/English)

#### Server-Management
- ✅ **One-Click Server-Erstellung**
- ✅ **Start/Stop/Restart-Kontrolle**
- ✅ **Echtzeit-Monitoring**
- ✅ **Log-Viewer**
- ✅ **Automatische Updates** über SteamCMD
- ✅ **Konfiguration-Management**

#### Sicherheit
- ✅ **JWT-Authentifizierung**
- ✅ **bcrypt-Passwort-Hashing**
- ✅ **HTTPS-Verschlüsselung**
- ✅ **CORS-Schutz**
- ✅ **Input-Validierung**
- ✅ **Firewall-Integration**

### 📖 Dokumentation

Die vollständige Dokumentation ist in beiden Sprachen verfügbar:

**English:**
- `ETS2_Server_Panel_Guide_en.md` - Complete installation and operation guide

**Deutsch:**
- `ETS2_Server_Panel_Anleitung.md` - Vollständige Installations- und Bedienungsanleitung

Beide Anleitungen enthalten:
1. **Detaillierte Installationsanleitung**
2. **Systemanforderungen und Kompatibilität**
3. **Schritt-für-Schritt-Konfiguration**
4. **HTTPS-Setup mit Let's Encrypt**
5. **Panel-Bedienung und Features**
6. **Server-Management-Guide**
7. **Troubleshooting und FAQ**
8. **API-Dokumentation**
9. **Entwicklung und Anpassung**

### 🔧 Manuelle Installation

Für erweiterte Setups oder Anpassungen siehe die detaillierte Anleitung in Ihrer bevorzugten Sprache.

### 🆘 Support und Troubleshooting

#### Häufige Probleme
- **Installation schlägt fehl:** Prüfen Sie Root-Rechte und Internetverbindung
- **Panel lädt nicht:** Überprüfen Sie Service-Status und Firewall
- **Server starten nicht:** Kontrollieren Sie Berechtigungen und Ports

#### Debug-Informationen sammeln
```bash
# Service-Status prüfen
sudo systemctl status ets2-panel-backend
sudo systemctl status nginx

# Logs anzeigen
sudo journalctl -u ets2-panel-backend -f
sudo tail -f /var/log/nginx/error.log
```

#### Community-Support
- **GitHub Issues:** Für Bug-Reports und Feature-Requests
- **Dokumentation:** Vollständige Anleitung mit FAQ in beiden Sprachen
- **Discord/Forum:** Community-Diskussionen (Links in der Dokumentation)

### 🔄 Updates und Wartung

#### Panel aktualisieren
```bash
# Neueste Version herunterladen
git pull origin main

# Deployment-Skript ausführen
./deploy-panel.sh
```

#### Backups erstellen
```bash
# Automatische Backups sind standardmäßig aktiviert
# Manuelle Backups:
sudo tar -czf ets2-panel-backup-$(date +%Y%m%d).tar.gz /opt/ets2-panel /opt/ets2-servers
```

### 📄 Lizenz

MIT License - Freie Nutzung für private und kommerzielle Zwecke.

### 🤝 Beitragen

Beiträge sind willkommen! Siehe CONTRIBUTING.md für Details.

### 📞 Kontakt
- **Autor:** Simon Dialler
- **Version:** 1.0
- **Datum:** Juli 2025

---

**Hinweis:** Dieses Panel ist ein unabhängiges Projekt und nicht offiziell von SCS Software unterstützt.

