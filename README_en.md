# ETS2 Server Panel - Complete Installation Package

A modern, web-based administration panel for Euro Truck Simulator 2 Dedicated Servers, inspired by Pterodactyl Panel.

## 🚛 Overview

This package contains everything you need to install and operate a professional ETS2 Server Panel:

- **Automatic Installation Script** for one-click setup
- **Complete Backend** (Python/Flask) with REST API
- **Modern Frontend** (React/Tailwind CSS) with responsive design
- **HTTPS Support** with Let's Encrypt Integration
- **Comprehensive Documentation** with Troubleshooting Guide

## 📁 Package Contents

### Installation Scripts
- `install-ets2-panel.sh` - Main installation script (automatic)
- `deploy-panel.sh` - Deployment script for updates
- `setup-https.sh` - HTTPS/SSL configuration

### Backend (Python/Flask)
- `ets2-panel-backend/` - Complete Backend with API
  - User Authentication (JWT)
  - Server Management API
  - WebSocket for real-time updates
  - SQLite Database

### Frontend (React)
- `ets2-panel-frontend/` - Modern React Application
  - Responsive Design
  - Dashboard with Real-time Monitoring
  - Server Management
  - User Management

### Documentation
- `ETS2_Server_Panel_Anleitung.md` - Complete Guide (50+ pages)
- `README.md` - This overview file

## 🚀 Quick Start

### Automatic Installation (Recommended)

```bash
curl -sSL https://raw.githubusercontent.com/BuzziGHG/ETS2-Panel/main/install-ets2-panel.sh | sudo bash
```

The script guides you through the configuration and automatically installs:
- All dependencies (Python, Node.js, Nginx)
- SteamCMD for ETS2 Server Management
- Backend and Frontend
- SSL Certificates (optional)
- Systemd Services

### After Installation

1. **Access Panel:** `https://your-domain.com` or `http://your-server-ip`
2. **Login:** Default login is `admin` / `admin123`
3. **Change Password:** Immediately after the first login
4. **Create First Server:** Via the Dashboard

## 🔧 System Requirements

### Minimal
- **OS:** Ubuntu 20.04+ or Debian 11+
- **RAM:** 2 GB
- **CPU:** 2 Cores
- **Storage:** 10 GB
- **Network:** Stable Internet Connection

### Recommended
- **OS:** Ubuntu 22.04 LTS
- **RAM:** 4 GB or more
- **CPU:** 4 Cores or more
- **Storage:** 50 GB SSD
- **Network:** 100 Mbit/s or more

## 🌟 Features

### Panel Features
- ✅ **Modern Dashboard** with Real-time Updates
- ✅ **Multi-Server Management** - Unlimited ETS2 Servers
- ✅ **User Management** with Role System
- ✅ **HTTPS Support** with Let's Encrypt
- ✅ **Responsive Design** for Desktop and Mobile
- ✅ **WebSocket Integration** for Live Updates
- ✅ **REST API** for Integrations

### Server Management
- ✅ **One-Click Server Creation**
- ✅ **Start/Stop/Restart Control**
- ✅ **Real-time Monitoring**
- ✅ **Log Viewer**
- ✅ **Automatic Updates** via SteamCMD
- ✅ **Configuration Management**

### Security
- ✅ **JWT Authentication**
- ✅ **bcrypt Password Hashing**
- ✅ **HTTPS Encryption**
- ✅ **CORS Protection**
- ✅ **Input Validation**
- ✅ **Firewall Integration**

## 📖 Documentation

The complete documentation (`ETS2_Server_Panel_Anleitung.md`) contains:

1. **Detailed Installation Guide**
2. **System Requirements and Compatibility**
3. **Step-by-Step Configuration**
4. **HTTPS Setup with Let's Encrypt**
5. **Panel Operation and Features**
6. **Server Management Guide**
7. **Troubleshooting and FAQ**
8. **API Documentation**
9. **Development and Customization**

## 🔧 Manual Installation

For advanced setups or customizations, see the detailed guide in `ETS2_Server_Panel_Anleitung.md`, Chapter "Manual Installation".

## 🆘 Support and Troubleshooting

### Common Issues
- **Installation fails:** Check root privileges and internet connection
- **Panel does not load:** Check service status and firewall
- **Servers do not start:** Check permissions and ports

### Collect Debug Information
```bash
# Check service status
sudo systemctl status ets2-panel-backend
sudo systemctl status nginx

# View logs
sudo journalctl -u ets2-panel-backend -f
sudo tail -f /var/log/nginx/error.log
```

### Community Support
- **GitHub Issues:** For bug reports and feature requests
- **Documentation:** Complete guide with FAQ
- **Discord/Forum:** Community discussions (Links in the documentation)

## 🔄 Updates and Maintenance

### Update Panel
```bash
# Download latest version
git pull origin main

# Execute deployment script
./deploy-panel.sh
```

### Create Backups
```bash
# Automatic backups are enabled by default
# Manual backups:
sudo tar -czf ets2-panel-backup-$(date +%Y%m%d).tar.gz /opt/ets2-panel /opt/ets2-servers
```

## 📄 License

MIT License - Free to use for private and commercial purposes.

## 🤝 Contribute

Contributions are welcome! See CONTRIBUTING.md for details.

## 📞 Contact
- **Author:** Simon Dialler
- **Version:** 1.0
- **Date:** July 2025

---

**Note:** This panel is an independent project and not officially supported by SCS Software.


