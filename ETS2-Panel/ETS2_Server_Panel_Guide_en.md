# Euro Truck Simulator 2 Server Panel - Complete Installation and Operation Guide

**Author:** Simon Dialler  
**Version:** 1.0  
**Date:** July 19, 2025  
**License:** MIT License

---

## Table of Contents

1. [Introduction](#introduction)
2. [System Requirements](#system-requirements)
3. [Quick Start Installation](#quick-start-installation)
4. [Manual Installation](#manual-installation)
5. [Configuration](#configuration)
6. [HTTPS Setup](#https-setup)
7. [Panel Operation](#panel-operation)
8. [Server Management](#server-management)
9. [Troubleshooting](#troubleshooting)
10. [Maintenance and Updates](#maintenance-and-updates)
11. [Security](#security)
12. [API Documentation](#api-documentation)
13. [Development and Customization](#development-and-customization)
14. [FAQ](#faq)
15. [Support and Community](#support-and-community)

---

## Introduction

The Euro Truck Simulator 2 (ETS2) Server Panel is a modern, web-based administration interface for ETS2 Dedicated Servers. Inspired by proven game server panels like Pterodactyl, it offers an intuitive and secure way to centrally manage multiple ETS2 servers.

### Key Features

The panel offers a comprehensive range of functions for professional server management:

**Server Management:** The core of the panel enables full control over ETS2 Dedicated Servers. Users can create, configure, start, stop, and monitor servers. The interface provides real-time information on server status, player count, and performance metrics.

**User Management:** A role-based permission system allows administrators to manage different user types. Admins have full access, while regular users can only manage their own servers. The system supports secure authentication with JWT tokens and password hashing.

**Real-time Monitoring:** The panel provides live updates via WebSocket connections. Server status, logs, and performance data are updated in real-time without the need to refresh the page.

**Secure Architecture:** The system was developed with security as a top priority. All connections can be encrypted via HTTPS, passwords are hashed with bcrypt, and the system offers protection against common web attacks.

### Technical Architecture

The panel is based on a modern, three-tier architecture:

**Frontend (React):** A responsive single-page application developed with React 18, Tailwind CSS, and shadcn/ui components. The frontend communicates with the backend via RESTful APIs and WebSockets.

**Backend (Flask):** A Python-based API server that uses Flask, SQLAlchemy, and Flask-SocketIO. The backend manages the database, authenticates users, and controls the ETS2 server processes.

**Database (SQLite):** A lightweight SQLite database stores user, server, and configuration data. For larger installations, the system can be easily migrated to PostgreSQL or MySQL.

### Target Audience

This panel is aimed at various user groups:

**Gaming Communities:** Clans and communities who want to run multiple ETS2 servers for different events or regions.

**Hosting Providers:** Companies that offer ETS2 server hosting as a service and need a professional administration interface for their customers.

**Individuals:** Enthusiasts who want to run their own ETS2 servers for friends and family.

**Developers:** People who want to use or extend the panel as a basis for their own projects.




## System Requirements

The successful installation and operation of the ETS2 Server Panel require certain hardware and software prerequisites. These requirements were developed based on extensive testing and analysis of typical server workloads.

### Hardware Requirements

**Minimum Requirements:**
- **CPU:** 2 CPU cores (x86_64 architecture)
- **RAM:** 2 GB available RAM
- **Storage:** 10 GB free disk space
- **Network:** Stable internet connection with at least 10 Mbit/s

**Recommended Requirements:**
- **CPU:** 4 CPU cores or more (Intel/AMD x86_64)
- **RAM:** 4 GB or more available RAM
- **Storage:** 50 GB or more free SSD space
- **Network:** Dedicated internet connection with 100 Mbit/s or more

**Production Environment:**
- **CPU:** 8 CPU cores or more with high clock frequency
- **RAM:** 8 GB or more available RAM
- **Storage:** 100 GB or more on fast NVMe SSDs
- **Network:** Redundant internet connection with low latency

The hardware requirements scale with the number of ETS2 servers operated simultaneously. Each active server additionally requires approximately 512 MB RAM and moderate CPU resources. When planning, peak loads that can occur when multiple servers are started or stopped simultaneously should also be taken into account.

### Software Requirements

**Supported Operating Systems:**
- Ubuntu 20.04 LTS or newer (recommended)



- Debian 11+ or newer
- CentOS 8+ or newer (with EPEL repository)
- Red Hat Enterprise Linux 8+ or newer

**Required Software Dependencies:**
- Python 3.8 or newer with pip package manager
- Node.js 16.0 or newer with npm package manager
- Git version control system for repository management
- Nginx web server for reverse proxy and static file serving
- SQLite 3.0 or newer for database functionality
- OpenSSL for SSL/TLS certificate management

**Network Requirements:**
- Inbound access on port 80 (HTTP) for initial setup and Let's Encrypt validation
- Inbound access on port 443 (HTTPS) for secure panel access
- Inbound access on ports 27015-27030 (UDP/TCP) for ETS2 server communication
- Outbound access to package repositories and SteamCMD servers
- Domain name with DNS A-record pointing to server IP (recommended for HTTPS)

The system has been extensively tested on Ubuntu 22.04 LTS, which represents the recommended platform for production deployments. While other Linux distributions are supported, Ubuntu provides the most streamlined installation experience due to its comprehensive package repositories and well-documented dependency management.

### Performance Considerations

When planning your hardware configuration, several factors influence the overall performance requirements. The panel itself has minimal resource overhead, typically consuming less than 100 MB of RAM and negligible CPU resources during normal operation. However, the ETS2 dedicated servers represent the primary resource consumers in the system.

Each ETS2 server instance requires approximately 512 MB of RAM during active gameplay, with additional memory needed for map loading and player data caching. CPU requirements scale with the number of connected players and the complexity of the game world. A single server with 8 players typically utilizes 10-15% of a modern CPU core, while servers with maximum player counts may require dedicated CPU resources.

Storage performance significantly impacts server startup times and player connection speeds. Traditional hard drives can result in server startup times exceeding 60 seconds, while SSD storage reduces this to 10-15 seconds. NVMe SSDs provide the best performance, with server startup times under 10 seconds and improved responsiveness during gameplay.

Network bandwidth requirements depend on the number of active servers and connected players. Each player connection consumes approximately 50-100 KB/s of bandwidth during active gameplay. A server with 8 players typically requires 400-800 KB/s of sustained bandwidth, with peaks during map transitions and player synchronization events.

## Quick Start Installation

The automated installation script provides the fastest and most reliable method for deploying the ETS2 Server Panel. This script has been designed to handle all dependency installation, configuration, and initial setup tasks automatically, minimizing the potential for configuration errors and reducing deployment time to under 30 minutes on most systems.

### Pre-Installation Checklist

Before beginning the installation process, ensure that your system meets all prerequisites and that you have gathered the necessary information for configuration. The installation script requires root privileges to install system packages and configure services, so ensure that you have sudo access or are logged in as the root user.

**System Preparation:**
Verify that your system is fully updated with the latest security patches and package updates. On Ubuntu systems, execute `sudo apt update && sudo apt upgrade -y` to ensure all packages are current. This step prevents potential conflicts with dependency installation and ensures compatibility with the latest package versions.

**Network Configuration:**
If you plan to use HTTPS (strongly recommended for production deployments), ensure that your domain name is properly configured with DNS A-records pointing to your server's public IP address. The Let's Encrypt certificate authority requires domain validation, which fails if DNS records are not properly configured.

**Firewall Considerations:**
Most cloud providers and server configurations include firewall rules that may block the required ports. Ensure that your firewall allows inbound connections on ports 80, 443, and the ETS2 server port range (27015-27030). The installation script can configure UFW (Uncomplicated Firewall) automatically, but manual firewall configuration may be required for other firewall systems.

### Automated Installation Process

The automated installation script streamlines the entire deployment process into a single command execution. This script performs comprehensive system analysis, dependency resolution, and configuration management to ensure a successful installation regardless of the starting system state.

```bash
curl -sSL https://raw.githubusercontent.com/BuzziGHG/ETS2-Panel/main/install-ets2-panel.sh | sudo bash
```

**Installation Script Workflow:**

The script begins by detecting the operating system and version to ensure compatibility and select appropriate package installation methods. It then performs a comprehensive system check to verify that all prerequisites are met and identifies any potential conflicts or missing dependencies.

**Dependency Installation Phase:**
The script automatically installs all required system packages, including Python 3.8+, Node.js 16+, Nginx, SQLite, and development tools necessary for compiling Python packages. Package installation is performed using the system's native package manager (apt on Ubuntu/Debian, yum on CentOS/RHEL) to ensure compatibility and proper integration with system services.

**SteamCMD Installation:**
SteamCMD (Steam Console Client) is installed and configured for automatic ETS2 server downloads and updates. The script creates a dedicated steam user account with appropriate permissions and configures SteamCMD for unattended operation. This includes accepting the Steam Subscriber Agreement and configuring anonymous login for public game server downloads.

**Backend Configuration:**
The Python Flask backend is installed in a virtual environment to prevent conflicts with system Python packages. All required Python dependencies are installed using pip, and the database schema is initialized with default administrative credentials. The backend service is configured as a systemd service for automatic startup and process management.

**Frontend Build Process:**
The React frontend is built using Node.js and npm, with all dependencies resolved and the application compiled for production deployment. The build process includes optimization steps such as code minification, asset compression, and bundle splitting to ensure optimal loading performance.

**Web Server Configuration:**
Nginx is configured as a reverse proxy to serve the React frontend and proxy API requests to the Flask backend. The configuration includes security headers, compression settings, and caching rules optimized for the panel's architecture. SSL/TLS configuration is prepared for Let's Encrypt certificate installation.

### Interactive Configuration

During the installation process, the script prompts for several configuration parameters that customize the panel for your specific environment and requirements. These prompts are designed to be user-friendly while providing advanced users with the flexibility to customize the installation.

**Domain Configuration:**
The script prompts for your domain name or server IP address. If you provide a domain name, the script automatically configures HTTPS with Let's Encrypt certificates. IP address configuration results in HTTP-only access, which is suitable for development or internal network deployments but not recommended for production use.

**Administrative Account Setup:**
You will be prompted to create the initial administrative account, including username and password. The script enforces strong password requirements to ensure security. This account has full administrative privileges and can create additional user accounts through the web interface.

**Server Configuration:**
The script asks for basic server configuration parameters, including the default ETS2 server installation directory, port ranges for server allocation, and backup configuration preferences. These settings can be modified later through the web interface, but proper initial configuration reduces post-installation setup time.

**SSL Certificate Configuration:**
If you provided a domain name, the script offers to automatically obtain and install Let's Encrypt SSL certificates. This process includes domain validation, certificate generation, and automatic renewal configuration. The script configures Nginx to redirect HTTP traffic to HTTPS and implements security best practices for SSL/TLS configuration.

### Post-Installation Verification

After the installation script completes, several verification steps ensure that all components are properly installed and configured. The script performs automated testing of all major system components and provides detailed status information for troubleshooting any issues.

**Service Status Verification:**
The script checks the status of all installed services, including the ETS2 Panel backend, Nginx web server, and any configured monitoring services. Service status information includes process IDs, memory usage, and startup logs to verify proper operation.

**Network Connectivity Testing:**
Automated tests verify that the panel is accessible via the configured domain name or IP address. These tests include HTTP/HTTPS connectivity, SSL certificate validation (if configured), and API endpoint responsiveness. Any connectivity issues are reported with specific troubleshooting recommendations.

**Database Initialization Verification:**
The script verifies that the SQLite database has been properly initialized with the correct schema and default data. This includes testing database connectivity, verifying table structure, and confirming that the administrative account has been created successfully.

**File Permissions and Security:**
All installed files and directories are checked for proper ownership and permissions. The script ensures that sensitive configuration files are protected from unauthorized access while maintaining the necessary permissions for proper operation.

## Manual Installation

While the automated installation script provides the most convenient deployment method, manual installation offers greater control over the configuration process and enables customization for specific environments or requirements. Manual installation is particularly valuable for advanced users who need to integrate the panel with existing infrastructure or implement custom security policies.

### System Preparation

Manual installation begins with comprehensive system preparation to ensure that all dependencies are properly installed and configured. This process requires careful attention to package versions and configuration details to ensure compatibility and optimal performance.

**Package Repository Configuration:**
Begin by updating your system's package repositories to ensure access to the latest package versions. On Ubuntu systems, this involves updating the apt package cache and optionally adding additional repositories for newer software versions.

```bash
sudo apt update
sudo apt upgrade -y
sudo apt install -y curl wget gnupg2 software-properties-common
```

**Python Environment Setup:**
Install Python 3.8 or newer along with the pip package manager and development headers necessary for compiling Python packages. The development headers are essential for packages that include C extensions, which are common in web application dependencies.

```bash
sudo apt install -y python3 python3-pip python3-dev python3-venv
python3 --version  # Verify Python 3.8+
```

**Node.js Installation:**
Install Node.js 16.0 or newer using the NodeSource repository, which provides more recent versions than the default Ubuntu repositories. This ensures compatibility with modern React development tools and build processes.

```bash
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs
node --version  # Verify Node.js 16+
npm --version   # Verify npm installation
```

**Database and Web Server Installation:**
Install SQLite for database functionality and Nginx for web server capabilities. These components form the foundation of the panel's infrastructure and require proper configuration for optimal performance.

```bash
sudo apt install -y sqlite3 nginx git
sudo systemctl enable nginx
sudo systemctl start nginx
```

### Backend Installation and Configuration

The backend installation process involves creating a dedicated environment for the Python application, installing dependencies, and configuring the database and application settings. This process requires careful attention to security considerations and proper file permissions.

**Application Directory Structure:**
Create a dedicated directory structure for the panel installation, with appropriate ownership and permissions. This structure separates the application code from system files and provides a clean organization for maintenance and updates.

```bash
sudo mkdir -p /opt/ets2-panel
sudo chown $USER:$USER /opt/ets2-panel
cd /opt/ets2-panel
```

**Repository Cloning and Setup:**
Clone the ETS2 Panel repository and navigate to the backend directory. This provides access to all application code and configuration files necessary for manual installation.

```bash
git clone https://github.com/BuzziGHG/ETS2-Panel.git .
cd ets2-panel-backend
```

**Python Virtual Environment:**
Create and activate a Python virtual environment to isolate the application dependencies from system Python packages. This prevents conflicts with system packages and enables easier maintenance and updates.

```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
```

**Dependency Installation:**
Install all required Python packages using the provided requirements file. This process may take several minutes as packages are downloaded and compiled.

```bash
pip install -r requirements.txt
```

**Database Initialization:**
Initialize the SQLite database with the required schema and default data. This process creates all necessary tables and indexes for proper application operation.

```bash
python app.py init-db
```

**Configuration File Setup:**
Create and configure the application configuration file with appropriate settings for your environment. This includes database paths, security keys, and operational parameters.

```bash
cp config.example.py config.py
# Edit config.py with your specific settings
```

### Frontend Build and Deployment

The frontend build process compiles the React application into static files that can be served by Nginx. This process includes dependency resolution, code compilation, and optimization for production deployment.

**Frontend Directory Navigation:**
Navigate to the frontend directory and install all required Node.js dependencies. This process downloads and installs all packages specified in the package.json file.

```bash
cd ../ets2-panel-frontend
npm install
```

**Production Build:**
Compile the React application for production deployment. This process includes code minification, asset optimization, and bundle generation for optimal loading performance.

```bash
npm run build
```

**Static File Deployment:**
Copy the compiled frontend files to the appropriate directory for Nginx serving. This typically involves copying files to the web server's document root or a dedicated directory for the application.

```bash
sudo cp -r dist/* /var/www/ets2-panel/
sudo chown -R www-data:www-data /var/www/ets2-panel/
```

### Web Server Configuration

Nginx configuration for the ETS2 Panel requires careful setup of reverse proxy rules, static file serving, and security headers. The configuration must balance performance, security, and functionality to provide optimal user experience.

**Nginx Site Configuration:**
Create a new Nginx site configuration file for the ETS2 Panel. This configuration includes server blocks for HTTP and HTTPS, proxy rules for API requests, and static file serving for the frontend.

```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com;
    
    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
    
    # Security Headers
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";
    
    # Frontend Static Files
    location / {
        root /var/www/ets2-panel;
        try_files $uri $uri/ /index.html;
    }
    
    # Backend API Proxy
    location /api/ {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # WebSocket Support
    location /socket.io/ {
        proxy_pass http://127.0.0.1:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
    }
}
```

**Site Activation:**
Enable the new site configuration and restart Nginx to apply the changes. This process includes syntax validation to prevent configuration errors.

```bash
sudo ln -s /etc/nginx/sites-available/ets2-panel /etc/nginx/sites-enabled/
sudo nginx -t  # Test configuration syntax
sudo systemctl restart nginx
```

### Service Configuration

Proper service configuration ensures that the ETS2 Panel starts automatically on system boot and can be managed using standard system tools. This involves creating systemd service files and configuring automatic startup.

**Backend Service Configuration:**
Create a systemd service file for the Flask backend application. This service file defines how the application should be started, stopped, and monitored by the system.

```ini
[Unit]
Description=ETS2 Panel Backend
After=network.target

[Service]
Type=simple
User=ets2panel
WorkingDirectory=/opt/ets2-panel/ets2-panel-backend
Environment=PATH=/opt/ets2-panel/ets2-panel-backend/venv/bin
ExecStart=/opt/ets2-panel/ets2-panel-backend/venv/bin/python app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Service Activation:**
Enable and start the backend service, then verify that it is running correctly. This process includes checking service status and reviewing startup logs for any errors.

```bash
sudo systemctl daemon-reload
sudo systemctl enable ets2-panel-backend
sudo systemctl start ets2-panel-backend
sudo systemctl status ets2-panel-backend
```

## Configuration

The ETS2 Server Panel offers extensive configuration options that allow administrators to customize the system for their specific requirements and environment. Configuration encompasses both system-level settings that affect overall operation and user-facing options that control panel behavior and appearance.

### Database Configuration

The panel uses SQLite as its default database system, providing a lightweight and maintenance-free solution for most installations. However, the system architecture supports migration to more robust database systems for high-traffic or enterprise deployments.

**SQLite Configuration:**
The default SQLite configuration provides excellent performance for installations managing up to 50 concurrent servers and 100 user accounts. The database file is stored in the backend directory with appropriate permissions to ensure security while maintaining accessibility for the application.

Database optimization for SQLite includes enabling Write-Ahead Logging (WAL) mode for improved concurrent access performance and configuring appropriate cache sizes for optimal query performance. These optimizations are automatically applied during the initialization process but can be customized for specific performance requirements.

**Connection Pooling:**
The Flask application implements connection pooling to manage database connections efficiently and prevent resource exhaustion under high load conditions. Connection pool settings can be adjusted based on expected concurrent user counts and server management activity levels.

**Backup Configuration:**
Automated database backups are configured by default, with daily backups retained for 30 days and weekly backups retained for 12 weeks. Backup files are compressed and stored in a dedicated backup directory with appropriate permissions to ensure data security.

### Security Configuration

Security configuration encompasses multiple layers of protection, from network-level security to application-level authentication and authorization. The panel implements industry-standard security practices while maintaining usability for administrators and end users.

**Authentication Configuration:**
The system uses JSON Web Tokens (JWT) for user authentication, providing stateless authentication that scales well across multiple server instances. JWT tokens are configured with appropriate expiration times and are signed using cryptographically secure keys generated during installation.

Password security is enforced through bcrypt hashing with configurable work factors that balance security and performance. The default work factor provides strong protection against brute-force attacks while maintaining reasonable authentication response times.

**Session Management:**
User sessions are managed through secure HTTP cookies with appropriate security flags including HttpOnly, Secure, and SameSite attributes. Session timeout is configurable and defaults to 24 hours for regular users and 8 hours for administrative accounts.

**API Security:**
All API endpoints implement proper authentication and authorization checks, with rate limiting configured to prevent abuse and denial-of-service attacks. CORS (Cross-Origin Resource Sharing) is configured to allow access only from authorized domains, preventing unauthorized cross-site requests.

### Server Management Configuration

Server management configuration controls how ETS2 dedicated servers are created, managed, and monitored within the panel. These settings affect server performance, resource allocation, and operational behavior.

**Server Directory Structure:**
Each ETS2 server instance is allocated a dedicated directory within the configured server root directory. This structure provides isolation between servers and simplifies backup and maintenance operations. Directory permissions are configured to ensure security while allowing necessary access for server operation.

**Port Allocation:**
The panel automatically allocates ports for new server instances within a configured range, typically 27015-27030 for standard installations. Port allocation includes both the primary server port and additional ports required for query and RCON functionality.

**Resource Limits:**
Server resource limits can be configured to prevent individual servers from consuming excessive system resources. These limits include memory usage caps, CPU time limits, and disk space quotas. Resource monitoring is implemented to track usage and alert administrators when limits are approached.

**Automatic Updates:**
SteamCMD integration enables automatic updates for ETS2 server binaries and game content. Update scheduling can be configured to occur during maintenance windows to minimize disruption to active players. The system supports both automatic updates and manual update triggering through the web interface.

## HTTPS Setup

HTTPS configuration is essential for production deployments of the ETS2 Server Panel, providing encryption for all communication between users and the server. The panel supports both Let's Encrypt automatic certificate management and manual certificate installation for enterprise environments.

### Let's Encrypt Integration

Let's Encrypt provides free SSL/TLS certificates with automatic renewal, making it the preferred solution for most installations. The panel includes integrated support for Let's Encrypt certificate acquisition and management, simplifying the HTTPS setup process.

**Domain Validation Requirements:**
Let's Encrypt requires domain validation to issue certificates, which means your server must be accessible from the internet using the domain name for which you're requesting a certificate. DNS A-records must be properly configured to point to your server's public IP address before attempting certificate acquisition.

**Automatic Certificate Acquisition:**
The installation script can automatically acquire Let's Encrypt certificates during the initial setup process. This involves temporarily configuring Nginx to serve the validation files required by Let's Encrypt's domain validation process.

```bash
sudo certbot --nginx -d your-domain.com
```

**Certificate Renewal Configuration:**
Let's Encrypt certificates are valid for 90 days and must be renewed regularly. The system automatically configures a cron job to check for certificate renewal twice daily, ensuring that certificates are renewed well before expiration.

```bash
# Automatic renewal check (configured automatically)
0 12 * * * /usr/bin/certbot renew --quiet
```

**Renewal Testing:**
After initial certificate installation, test the renewal process to ensure that automatic renewal will function correctly when needed. This prevents certificate expiration issues that could disrupt service availability.

```bash
sudo certbot renew --dry-run
```

### Manual Certificate Installation

For enterprise environments or installations that require specific certificate authorities, manual certificate installation provides complete control over the SSL/TLS configuration. This process involves obtaining certificates from your chosen certificate authority and configuring Nginx appropriately.

**Certificate File Preparation:**
Manual certificate installation requires three files: the server certificate, the certificate private key, and the certificate authority chain file. These files must be properly formatted and stored in secure locations with appropriate permissions.

**Nginx SSL Configuration:**
Configure Nginx with the manually installed certificates, including proper SSL/TLS settings for security and performance. This configuration should include modern cipher suites, HSTS headers, and other security best practices.

```nginx
ssl_certificate /etc/ssl/certs/ets2-panel.crt;
ssl_certificate_key /etc/ssl/private/ets2-panel.key;
ssl_trusted_certificate /etc/ssl/certs/ca-chain.crt;

ssl_protocols TLSv1.2 TLSv1.3;
ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
ssl_prefer_server_ciphers off;

add_header Strict-Transport-Security "max-age=63072000" always;
```

### Security Best Practices

HTTPS configuration should implement current security best practices to protect against various attack vectors and ensure compliance with security standards. These practices evolve over time as new vulnerabilities are discovered and mitigation techniques are developed.

**SSL/TLS Protocol Configuration:**
Disable older SSL/TLS protocol versions that contain known vulnerabilities, including SSLv2, SSLv3, and TLSv1.0. Configure the server to prefer TLSv1.2 and TLSv1.3, which provide the strongest security and best performance.

**Cipher Suite Selection:**
Configure strong cipher suites that provide forward secrecy and resist known cryptographic attacks. Prefer ECDHE (Elliptic Curve Diffie-Hellman Ephemeral) key exchange and AES-GCM encryption modes for optimal security and performance.

**HTTP Security Headers:**
Implement security headers that protect against common web application attacks, including cross-site scripting (XSS), clickjacking, and content type sniffing attacks. These headers provide defense-in-depth security for web applications.

```nginx
add_header X-Frame-Options DENY;
add_header X-Content-Type-Options nosniff;
add_header X-XSS-Protection "1; mode=block";
add_header Referrer-Policy "strict-origin-when-cross-origin";
add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';";
```

**Certificate Monitoring:**
Implement monitoring for certificate expiration and validity to ensure that certificates are renewed before expiration and that the certificate chain is properly configured. This prevents service disruptions due to certificate issues.

## Panel Operation

The ETS2 Server Panel provides an intuitive web-based interface for managing Euro Truck Simulator 2 dedicated servers. The interface is designed to be accessible to users with varying levels of technical expertise while providing advanced functionality for experienced administrators.

### User Interface Overview

The panel interface follows modern web application design principles, with a responsive layout that adapts to different screen sizes and devices. The interface is organized into logical sections that correspond to different aspects of server management and administration.

**Navigation Structure:**
The main navigation is organized into primary sections including Dashboard, Server Management, User Management (for administrators), and Settings. Each section contains related functionality and provides clear visual indicators of the current location within the application.

**Dashboard Overview:**
The dashboard provides a comprehensive overview of system status, including active servers, connected players, system resource usage, and recent activity. Real-time updates ensure that the information displayed is current and accurate.

**Language Selection:**
The panel now supports multiple languages with a convenient language selector in the top navigation. Users can switch between German and English interfaces, with their language preference saved for future sessions. The language selection affects all interface elements, including menus, buttons, status messages, and help text.

### User Management

User management functionality enables administrators to create and manage user accounts with different permission levels. The system supports role-based access control to ensure that users have appropriate access to functionality based on their responsibilities.

**User Roles:**
The system defines two primary user roles: Administrator and User. Administrators have full access to all panel functionality, including user management, system settings, and all server management capabilities. Regular users have access to server management functionality but cannot modify system settings or manage other user accounts.

**Account Creation:**
New user accounts can be created through the web interface by administrators. The account creation process includes username validation, password strength requirements, and role assignment. Email addresses can be optionally associated with accounts for password recovery functionality.

**Permission Management:**
User permissions are managed through the role system, with the ability to customize permissions for specific users when necessary. This flexibility enables administrators to grant specific capabilities to users based on their responsibilities and trust level.

### Server Creation and Configuration

Server creation is streamlined through a wizard-based interface that guides users through the configuration process. The wizard collects necessary information and validates settings to ensure successful server creation.

**Server Creation Wizard:**
The server creation wizard begins by collecting basic server information including server name, description, and initial configuration parameters. The wizard validates each step to prevent configuration errors and provides helpful guidance for complex settings.

**Configuration Templates:**
Pre-configured templates are available for common server configurations, including different game modes, player limits, and performance settings. These templates provide a starting point that can be customized for specific requirements.

**Advanced Configuration:**
Advanced users can access detailed configuration options for fine-tuning server behavior. This includes network settings, gameplay parameters, and integration options for external tools and services.

### Real-time Monitoring

The panel provides comprehensive real-time monitoring of server status, player activity, and system performance. This monitoring capability enables administrators to quickly identify and respond to issues before they impact player experience.

**Server Status Monitoring:**
Each server's status is continuously monitored and displayed in the interface, including online/offline status, current player count, and basic performance metrics. Status updates are delivered in real-time through WebSocket connections, ensuring that the interface reflects current conditions.

**Performance Metrics:**
System performance metrics including CPU usage, memory consumption, and network activity are collected and displayed through interactive charts and graphs. Historical data is retained to enable trend analysis and capacity planning.

**Alert System:**
The monitoring system can generate alerts for various conditions including server crashes, high resource usage, and connectivity issues. Alerts can be delivered through the web interface and optionally via email or other notification systems.

## Server Management

Server management represents the core functionality of the ETS2 Panel, providing comprehensive tools for creating, configuring, and operating Euro Truck Simulator 2 dedicated servers. The management interface is designed to handle both simple server operations and complex multi-server deployments.

### Server Lifecycle Management

Server lifecycle management encompasses all aspects of server operation from initial creation through ongoing maintenance and eventual decommissioning. The panel provides tools and automation to simplify each phase of the server lifecycle.

**Server Creation Process:**
New server creation begins with the server creation wizard, which guides users through the configuration process step by step. The wizard collects essential information including server name, game mode, player limits, and network configuration. Input validation ensures that all settings are compatible and will result in a functional server.

The creation process includes automatic allocation of network ports from the configured port range, creation of dedicated server directories with appropriate permissions, and installation of the latest ETS2 server binaries through SteamCMD integration. Configuration files are generated based on the selected options and can be customized after creation if needed.

**Server Configuration Management:**
Once created, servers can be reconfigured through the web interface without requiring direct file system access. Configuration changes are validated before application to prevent invalid settings that could prevent server startup. The system maintains configuration history to enable rollback to previous settings if needed.

Configuration templates enable rapid deployment of servers with standardized settings. Templates can be created from existing server configurations and applied to new servers, ensuring consistency across multiple server instances.

**Server Updates and Maintenance:**
The panel integrates with SteamCMD to provide automatic server updates when new ETS2 versions are released. Update scheduling can be configured to occur during maintenance windows to minimize disruption to active players. The system supports both automatic updates and manual update triggering for administrators who prefer to control the update process.

Maintenance operations including log rotation, temporary file cleanup, and performance optimization are automated to reduce administrative overhead. These operations are scheduled during low-activity periods to minimize impact on server performance.

### Performance Monitoring and Optimization

Performance monitoring provides detailed insights into server operation and resource utilization, enabling administrators to optimize performance and identify potential issues before they impact players.

**Resource Utilization Tracking:**
The panel continuously monitors CPU usage, memory consumption, disk I/O, and network activity for each server instance. This data is collected at regular intervals and stored for historical analysis. Resource usage patterns can reveal optimization opportunities and help with capacity planning for server growth.

Memory usage monitoring is particularly important for ETS2 servers, as memory leaks or excessive memory consumption can lead to server instability. The panel tracks memory usage trends and can alert administrators when usage exceeds configured thresholds.

**Performance Optimization:**
The panel includes automated performance optimization features that adjust server settings based on current load and resource availability. These optimizations include dynamic player limits based on server performance, automatic garbage collection scheduling, and network buffer tuning for optimal throughput.

Server affinity settings can be configured to bind servers to specific CPU cores, improving performance on multi-core systems by reducing context switching and improving cache locality. This is particularly beneficial for high-performance servers with demanding player loads.

**Capacity Planning:**
Historical performance data enables capacity planning for server growth and hardware upgrades. The panel provides reports and visualizations that show resource usage trends over time, helping administrators predict when additional hardware resources will be needed.

Load testing capabilities enable administrators to evaluate server performance under various load conditions without impacting production servers. This testing can reveal performance bottlenecks and validate optimization strategies before implementation.

### Player Management

Player management functionality provides tools for monitoring player activity, managing player access, and maintaining server community standards. These tools are essential for creating positive gaming experiences and maintaining server reputation.

**Player Activity Monitoring:**
The panel tracks player connections, session duration, and activity patterns for each server. This information helps administrators understand player behavior and optimize server settings for the player community. Activity logs can be filtered and searched to investigate specific incidents or track player history.

Real-time player lists show currently connected players with connection information, play time, and basic statistics. This information is updated continuously to provide accurate current status information.

**Access Control and Moderation:**
Player access control includes ban management, whitelist functionality, and temporary restrictions for players who violate server rules. The ban system supports both permanent and temporary bans with automatic expiration. Ban reasons and administrator notes are recorded for accountability and appeal processes.

Whitelist functionality enables servers to restrict access to approved players only, which is useful for private servers or communities that require membership approval. The whitelist can be managed through the web interface with bulk import/export capabilities for large player lists.

**Community Management Tools:**
The panel provides tools for community management including player statistics, achievement tracking, and communication features. These tools help build engaged player communities and encourage regular participation.

Player feedback and reporting systems enable community members to report issues or provide suggestions for server improvement. These reports are tracked and can be assigned to administrators for follow-up action.

## Troubleshooting

Troubleshooting the ETS2 Server Panel requires a systematic approach to identify and resolve issues that may affect system operation. The panel includes comprehensive logging and diagnostic tools to assist with problem identification and resolution.

### Common Installation Issues

Installation issues are among the most frequently encountered problems, often resulting from system configuration differences, missing dependencies, or network connectivity problems. Understanding common installation issues and their solutions can significantly reduce deployment time and frustration.

**Dependency Resolution Problems:**
Package dependency conflicts can occur when the system has conflicting package versions or when required packages are not available in the configured repositories. These issues typically manifest as package installation failures or version compatibility errors during the installation process.

Resolution involves identifying the conflicting packages and either updating the system packages or configuring alternative package sources. On Ubuntu systems, enabling the universe repository often resolves package availability issues. For systems with older package versions, adding third-party repositories for newer software versions may be necessary.

**Permission and Ownership Issues:**
File permission problems can prevent proper installation or operation of the panel components. These issues often occur when installation is performed with incorrect user privileges or when file ownership is not properly configured during the installation process.

Systematic permission checking involves verifying that all application files have appropriate ownership and permissions for the user account under which the services will run. The installation script automatically configures permissions, but manual installations may require careful attention to permission settings.

**Network Connectivity Problems:**
Network connectivity issues can prevent package downloads, certificate acquisition, or proper operation of the installed panel. These problems may be caused by firewall restrictions, DNS configuration issues, or network routing problems.

Diagnostic steps include testing basic network connectivity, verifying DNS resolution for required hostnames, and checking firewall rules for the necessary ports. Network connectivity testing should be performed from the perspective of the user account under which the services will run, as different users may have different network access permissions.

### Service Management Issues

Service management problems typically involve issues with systemd service configuration, process startup failures, or inter-service communication problems. These issues can prevent the panel from starting correctly or cause intermittent operation problems.

**Backend Service Startup Failures:**
The Flask backend service may fail to start due to configuration errors, missing dependencies, or database connectivity issues. Service startup failures are typically logged to the systemd journal and can be diagnosed using standard systemd troubleshooting tools.

```bash
# Check service status and recent logs
sudo systemctl status ets2-panel-backend
sudo journalctl -u ets2-panel-backend -f

# Check for configuration errors
cd /opt/ets2-panel/ets2-panel-backend
source venv/bin/activate
python app.py --check-config
```

Common backend startup issues include database file permissions, missing Python dependencies, and configuration file syntax errors. Each of these issues has specific diagnostic steps and resolution procedures.

**Web Server Configuration Problems:**
Nginx configuration errors can prevent proper serving of the frontend application or proxying of backend API requests. Configuration syntax errors are typically detected during nginx configuration testing, while runtime issues may require log analysis to identify.

```bash
# Test nginx configuration syntax
sudo nginx -t

# Check nginx error logs
sudo tail -f /var/log/nginx/error.log

# Verify site configuration
sudo nginx -T | grep -A 20 -B 5 "ets2-panel"
```

**Database Connectivity Issues:**
Database connectivity problems can occur due to file permissions, disk space issues, or database corruption. SQLite databases are generally reliable, but issues can occur under certain conditions such as disk full conditions or improper shutdown.

Database diagnostic procedures include checking file permissions, verifying database integrity, and testing database connectivity from the application. Database backup and recovery procedures should be tested regularly to ensure data protection.

### Performance Troubleshooting

Performance issues can significantly impact user experience and may indicate underlying system problems that require attention. Performance troubleshooting involves identifying bottlenecks and implementing appropriate optimizations.

**Resource Utilization Analysis:**
High CPU usage, memory consumption, or disk I/O can indicate performance problems that require investigation. Resource monitoring tools can help identify which components are consuming excessive resources and when these issues occur.

```bash
# Monitor system resource usage
htop
iotop
free -h
df -h

# Check for memory leaks in panel processes
ps aux | grep -E "(python|nginx)" | sort -k 4 -nr
```

**Database Performance Issues:**
Database performance problems can manifest as slow page loading, timeout errors, or high CPU usage from database processes. SQLite performance can be affected by database size, query complexity, and concurrent access patterns.

Database optimization techniques include analyzing query performance, optimizing database schema, and configuring appropriate SQLite settings for the workload. For high-traffic installations, migration to PostgreSQL or MySQL may be necessary.

**Network Performance Problems:**
Network performance issues can affect both panel responsiveness and ETS2 server performance. These issues may be caused by bandwidth limitations, network congestion, or configuration problems.

Network diagnostic tools can help identify performance bottlenecks and configuration issues. Bandwidth testing, latency measurement, and packet loss analysis provide insights into network performance characteristics.

### Log Analysis and Debugging

Comprehensive logging is essential for troubleshooting complex issues and understanding system behavior. The panel generates logs at multiple levels and locations, requiring systematic analysis to identify relevant information.

**Application Log Analysis:**
The Flask backend generates detailed application logs that include request processing, database operations, and error conditions. These logs are essential for diagnosing application-level issues and understanding user activity patterns.

```bash
# View backend application logs
sudo journalctl -u ets2-panel-backend -f

# Search for specific error patterns
sudo journalctl -u ets2-panel-backend | grep -i error

# Analyze log patterns over time
sudo journalctl -u ets2-panel-backend --since "1 hour ago" | grep -E "(ERROR|WARNING)"
```

**Web Server Log Analysis:**
Nginx access and error logs provide information about web requests, response times, and server errors. These logs are valuable for diagnosing frontend issues and understanding user access patterns.

```bash
# Monitor nginx access logs
sudo tail -f /var/log/nginx/access.log

# Analyze error patterns
sudo grep -E "(4[0-9]{2}|5[0-9]{2})" /var/log/nginx/access.log | tail -20

# Check for configuration issues
sudo tail -f /var/log/nginx/error.log
```

**System Log Analysis:**
System logs contain information about hardware issues, kernel messages, and system service status. These logs can provide insights into underlying system problems that may affect panel operation.

```bash
# Check system messages
sudo dmesg | tail -20

# Monitor system logs
sudo journalctl -f

# Check for disk or memory issues
sudo journalctl --since "1 hour ago" | grep -E "(error|failed|critical)"
```

## Maintenance and Updates

Regular maintenance and updates are essential for ensuring the security, performance, and reliability of the ETS2 Server Panel. A comprehensive maintenance strategy includes both automated and manual procedures to keep the system operating optimally.

### Update Management

Update management encompasses both system-level updates for the underlying operating system and application-level updates for the panel software and ETS2 server binaries. Proper update management balances security and stability requirements with the need to minimize service disruption.

**System Package Updates:**
Operating system package updates should be applied regularly to ensure security patches and bug fixes are installed promptly. However, updates should be tested in a development environment when possible to identify potential compatibility issues before applying to production systems.

```bash
# Check for available updates
sudo apt list --upgradable

# Apply security updates only
sudo unattended-upgrade

# Apply all available updates (schedule during maintenance window)
sudo apt update && sudo apt upgrade -y
```

**Panel Software Updates:**
Panel software updates are distributed through the GitHub repository and can be applied using git pull operations. Before applying updates, ensure that any local customizations are properly backed up and that the update process is tested in a development environment.

```bash
# Backup current installation
sudo tar -czf ets2-panel-backup-$(date +%Y%m%d).tar.gz /opt/ets2-panel

# Update panel software
cd /opt/ets2-panel
git pull origin main

# Apply database migrations if needed
cd ets2-panel-backend
source venv/bin/activate
python app.py migrate

# Rebuild frontend if needed
cd ../ets2-panel-frontend
npm install
npm run build

# Restart services
sudo systemctl restart ets2-panel-backend nginx
```

**ETS2 Server Updates:**
ETS2 server binaries are updated through SteamCMD integration, which can be configured for automatic updates or manual triggering. Server updates should be scheduled during maintenance windows to minimize disruption to active players.

The panel provides update scheduling functionality that can automatically update servers during configured maintenance windows. Update notifications can be sent to players in advance to inform them of scheduled maintenance periods.

### Backup and Recovery

Comprehensive backup and recovery procedures are essential for protecting against data loss and ensuring rapid recovery from system failures. Backup strategies should address both system-level backups and application-specific data protection.

**Database Backup Procedures:**
Database backups are automatically configured during installation, with daily incremental backups and weekly full backups. Backup retention policies can be customized based on storage capacity and recovery requirements.

```bash
# Manual database backup
sqlite3 /opt/ets2-panel/ets2-panel-backend/database.db ".backup /backup/database-$(date +%Y%m%d).db"

# Verify backup integrity
sqlite3 /backup/database-$(date +%Y%m%d).db "PRAGMA integrity_check;"

# Restore from backup
sudo systemctl stop ets2-panel-backend
cp /backup/database-20250719.db /opt/ets2-panel/ets2-panel-backend/database.db
sudo systemctl start ets2-panel-backend
```

**Configuration Backup:**
System and application configuration files should be backed up regularly to enable rapid recovery from configuration errors or system failures. Configuration backups should include both panel-specific settings and system-level configuration files.

**Server Data Backup:**
ETS2 server data including save games, configuration files, and custom content should be backed up regularly. Server data backups can be large, so compression and incremental backup strategies may be necessary for systems with multiple servers.

### Performance Monitoring and Optimization

Ongoing performance monitoring enables proactive identification of performance issues and optimization opportunities. Performance monitoring should include both automated monitoring systems and regular manual performance reviews.

**Automated Monitoring:**
Automated monitoring systems can track key performance metrics and generate alerts when thresholds are exceeded. Monitoring should include system resources, application performance, and user experience metrics.

Performance monitoring tools can be integrated with the panel to provide real-time dashboards and historical trend analysis. These tools help identify performance patterns and predict when system upgrades or optimizations may be needed.

**Performance Optimization:**
Regular performance optimization reviews should evaluate system performance against established baselines and identify opportunities for improvement. Optimization strategies may include database tuning, system configuration adjustments, and hardware upgrades.

Performance optimization should be approached systematically, with changes implemented incrementally and results measured to ensure that optimizations provide the expected benefits without introducing new issues.

### Security Maintenance

Security maintenance involves regular security assessments, vulnerability management, and security configuration updates. Security maintenance is critical for protecting against evolving threats and maintaining compliance with security best practices.

**Security Updates:**
Security updates should be prioritized and applied promptly to address known vulnerabilities. Security update procedures should include testing in development environments when possible, but critical security updates may need to be applied immediately to production systems.

**Vulnerability Scanning:**
Regular vulnerability scanning can identify potential security issues before they are exploited by attackers. Vulnerability scanning should include both system-level scanning and application-specific security assessments.

**Security Configuration Reviews:**
Security configuration should be reviewed regularly to ensure that security settings remain appropriate as the system evolves. Security reviews should include access controls, network security, and application security configurations.

## Security

Security is a fundamental aspect of the ETS2 Server Panel design and operation. The panel implements multiple layers of security controls to protect against various threat vectors while maintaining usability for legitimate users.

### Authentication and Authorization

The panel implements a comprehensive authentication and authorization system based on industry-standard practices and technologies. This system ensures that only authorized users can access the panel and that users have appropriate permissions for their assigned roles.

**Multi-Factor Authentication:**
While not enabled by default, the panel architecture supports multi-factor authentication (MFA) implementation for enhanced security. MFA can be particularly valuable for administrative accounts that have elevated privileges within the system.

**Session Security:**
User sessions are protected through multiple security mechanisms including secure session tokens, appropriate session timeouts, and session invalidation on suspicious activity. Session security helps prevent unauthorized access even if session tokens are compromised.

**Password Security:**
Password security is enforced through strong password requirements, secure password storage using bcrypt hashing, and protection against common password attacks such as brute force and dictionary attacks.

### Network Security

Network security controls protect the panel from network-based attacks and ensure that communication between components is properly secured. These controls include both perimeter security and internal network protection.

**Firewall Configuration:**
Proper firewall configuration is essential for limiting network access to only the necessary ports and services. The panel requires specific ports for web access and ETS2 server communication, while all other ports should be blocked by default.

**SSL/TLS Security:**
All web communication should be encrypted using SSL/TLS protocols with strong cipher suites and proper certificate validation. SSL/TLS configuration should follow current best practices and be updated regularly as security standards evolve.

**Network Monitoring:**
Network monitoring can detect suspicious activity and potential attacks before they impact system security. Monitoring should include both automated intrusion detection and regular manual review of network logs.

### Application Security

Application security encompasses the security measures implemented within the panel software itself. These measures protect against common web application vulnerabilities and ensure that the application handles user input and data securely.

**Input Validation:**
All user input is validated both on the client side and server side to prevent injection attacks and data corruption. Input validation includes both format validation and business logic validation to ensure data integrity.

**Cross-Site Scripting (XSS) Protection:**
The panel implements multiple layers of XSS protection including input sanitization, output encoding, and Content Security Policy (CSP) headers. These protections prevent malicious scripts from being executed in user browsers.

**SQL Injection Prevention:**
Database queries use parameterized statements and prepared queries to prevent SQL injection attacks. The ORM (Object-Relational Mapping) layer provides additional protection against database-related security vulnerabilities.

**Cross-Site Request Forgery (CSRF) Protection:**
CSRF protection is implemented through token-based validation of state-changing requests. This protection prevents unauthorized actions from being performed on behalf of authenticated users.

### Data Protection

Data protection measures ensure that sensitive information is properly secured both in transit and at rest. These measures include encryption, access controls, and data handling procedures.

**Data Encryption:**
Sensitive data is encrypted both in transit and at rest using industry-standard encryption algorithms. Database encryption can be implemented for additional protection of stored data, particularly in environments with strict data protection requirements.

**Access Logging:**
All access to sensitive data and administrative functions is logged for audit purposes. Access logs can be used to detect unauthorized access attempts and to investigate security incidents.

**Data Backup Security:**
Backup data is protected using the same security measures as production data, including encryption and access controls. Backup security is particularly important as backups may be stored in less secure locations or transmitted over networks.

## API Documentation

The ETS2 Server Panel provides a comprehensive REST API that enables programmatic access to panel functionality. The API is designed to support both web interface operations and third-party integrations, providing flexibility for custom applications and automation scripts.

### API Architecture

The API follows REST (Representational State Transfer) principles, providing a consistent and predictable interface for accessing panel functionality. The API uses standard HTTP methods and status codes, making it compatible with a wide range of client libraries and tools.

**Authentication:**
API authentication uses JWT (JSON Web Tokens) for stateless authentication that scales well across multiple server instances. API clients must obtain authentication tokens through the login endpoint and include these tokens in subsequent requests.

```bash
# Obtain authentication token
curl -X POST https://your-domain.com/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "your-password"}'

# Use token in subsequent requests
curl -X GET https://your-domain.com/api/servers \
  -H "Authorization: Bearer your-jwt-token"
```

**Rate Limiting:**
API rate limiting prevents abuse and ensures fair resource allocation among API clients. Rate limits are applied per user account and can be customized based on user roles and specific requirements.

**Error Handling:**
The API provides consistent error responses with appropriate HTTP status codes and detailed error messages. Error responses include both human-readable messages and machine-readable error codes for programmatic handling.

### Server Management API

The server management API provides comprehensive access to server lifecycle operations, configuration management, and monitoring functionality. This API enables automation of server operations and integration with external management systems.

**Server Creation:**
Server creation through the API requires the same parameters as the web interface, with additional validation to ensure that all required settings are provided and valid.

```bash
# Create new server
curl -X POST https://your-domain.com/api/servers \
  -H "Authorization: Bearer your-jwt-token" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My ETS2 Server",
    "description": "Test server for API",
    "max_players": 8,
    "port": 27015,
    "password": "server-password"
  }'
```

**Server Control:**
Server control operations including start, stop, and restart are available through simple API endpoints. These operations return immediately with status information, while the actual server state changes occur asynchronously.

```bash
# Start server
curl -X POST https://your-domain.com/api/servers/1/start \
  -H "Authorization: Bearer your-jwt-token"

# Stop server
curl -X POST https://your-domain.com/api/servers/1/stop \
  -H "Authorization: Bearer your-jwt-token"

# Get server status
curl -X GET https://your-domain.com/api/servers/1/status \
  -H "Authorization: Bearer your-jwt-token"
```

**Configuration Management:**
Server configuration can be retrieved and updated through the API, enabling programmatic configuration management and bulk configuration operations.

### User Management API

The user management API provides functionality for managing user accounts, roles, and permissions. This API is restricted to administrative users and enables integration with external user management systems.

**User Account Operations:**
User account creation, modification, and deletion are supported through standard REST operations. User account operations include validation of user data and enforcement of business rules such as unique usernames.

```bash
# Create new user
curl -X POST https://your-domain.com/api/users \
  -H "Authorization: Bearer admin-jwt-token" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "newuser",
    "password": "secure-password",
    "email": "user@example.com",
    "role": "user"
  }'

# List all users
curl -X GET https://your-domain.com/api/users \
  -H "Authorization: Bearer admin-jwt-token"
```

**Permission Management:**
User permissions can be queried and modified through the API, enabling dynamic permission management based on external criteria or automated workflows.

### Monitoring and Statistics API

The monitoring API provides access to real-time and historical data about server performance, user activity, and system status. This API enables integration with external monitoring systems and custom dashboard applications.

**Real-time Data:**
Real-time server status, player counts, and performance metrics are available through API endpoints that return current data. This data is updated continuously and reflects the actual system state.

**Historical Data:**
Historical performance data and usage statistics are available through API endpoints that support date range queries and data aggregation. This data enables trend analysis and capacity planning.

```bash
# Get current server statistics
curl -X GET https://your-domain.com/api/stats/servers \
  -H "Authorization: Bearer your-jwt-token"

# Get historical performance data
curl -X GET "https://your-domain.com/api/stats/performance?start=2025-07-01&end=2025-07-19" \
  -H "Authorization: Bearer your-jwt-token"
```

## Development and Customization

The ETS2 Server Panel is designed to be extensible and customizable to meet specific requirements and integrate with existing infrastructure. The modular architecture and comprehensive API enable various customization approaches from simple configuration changes to extensive feature additions.

### Development Environment Setup

Setting up a development environment enables safe testing of modifications and custom features without affecting production systems. The development environment should closely mirror the production environment while providing additional tools for debugging and testing.

**Local Development Setup:**
Local development setup involves cloning the repository, installing dependencies, and configuring the development environment for both backend and frontend components. Development environments typically use different database configurations and may include additional debugging tools.

```bash
# Clone repository for development
git clone https://github.com/BuzziGHG/ETS2-Panel.git
cd ETS2-Panel

# Setup backend development environment
cd ets2-panel-backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Development dependencies

# Setup frontend development environment
cd ../ets2-panel-frontend
npm install
npm run dev  # Start development server
```

**Development Database:**
Development environments should use separate database instances to prevent interference with production data. SQLite databases can be easily copied for development use, while more complex database systems may require additional setup procedures.

**Testing Framework:**
The panel includes comprehensive testing frameworks for both backend and frontend components. Tests should be run regularly during development to ensure that modifications do not introduce regressions or break existing functionality.

### Customization Options

The panel provides multiple levels of customization from simple configuration changes to extensive code modifications. Understanding the available customization options helps determine the best approach for specific requirements.

**Configuration-Based Customization:**
Many aspects of panel behavior can be customized through configuration files without requiring code changes. Configuration-based customization is the safest and most maintainable approach for most requirements.

**Theme and Branding Customization:**
The frontend interface can be customized with different themes, colors, and branding elements. Theme customization involves modifying CSS files and potentially updating React components for more extensive changes.

**Feature Extensions:**
New features can be added to the panel through the plugin system or by extending existing components. Feature extensions should follow the established architecture patterns to ensure compatibility with future updates.

### Plugin Development

The panel architecture supports plugin development for adding custom functionality without modifying core code. Plugins provide a clean separation between core functionality and custom features, making updates and maintenance easier.

**Plugin Architecture:**
Plugins are implemented as separate modules that integrate with the core system through defined interfaces. The plugin system provides hooks for extending various aspects of panel functionality including user interface, API endpoints, and background processing.

**Plugin Development Guidelines:**
Plugin development should follow established coding standards and architectural patterns to ensure compatibility and maintainability. Plugins should be thoroughly tested and documented to facilitate deployment and maintenance.

### Integration Possibilities

The panel can be integrated with various external systems and services to provide enhanced functionality or to fit into existing infrastructure. Integration possibilities include authentication systems, monitoring platforms, and automation tools.

**Authentication Integration:**
The panel can be integrated with external authentication systems such as LDAP, Active Directory, or OAuth providers. Authentication integration enables single sign-on functionality and centralized user management.

**Monitoring Integration:**
Panel metrics and status information can be exported to external monitoring systems such as Prometheus, Grafana, or custom monitoring platforms. Monitoring integration enables centralized monitoring of multiple panel instances and integration with existing monitoring infrastructure.

**Automation Integration:**
The comprehensive API enables integration with automation tools and configuration management systems. Automation integration can include server provisioning, configuration management, and automated response to system events.

## FAQ

This section addresses frequently asked questions about the ETS2 Server Panel installation, configuration, and operation. These questions are based on common issues and inquiries from users and administrators.

### Installation and Setup Questions

**Q: What are the minimum system requirements for running the panel?**
A: The minimum requirements are 2 CPU cores, 2 GB RAM, 10 GB storage, and Ubuntu 20.04+ or equivalent. However, we recommend 4 CPU cores, 4 GB RAM, and 50 GB SSD storage for better performance, especially when running multiple servers.

**Q: Can I install the panel on Windows or macOS?**
A: The panel is designed for Linux systems and has been tested primarily on Ubuntu. While it may be possible to run on Windows using WSL (Windows Subsystem for Linux) or on macOS, these configurations are not officially supported and may require additional configuration.

**Q: How do I enable HTTPS with Let's Encrypt?**
A: HTTPS with Let's Encrypt can be enabled during the automated installation by providing a domain name when prompted. For manual setup, use certbot with the nginx plugin: `sudo certbot --nginx -d your-domain.com`

**Q: What should I do if the installation script fails?**
A: First, check the error message and ensure your system meets all requirements. Common issues include insufficient permissions (run with sudo), network connectivity problems, or missing system updates. Check the troubleshooting section for specific error resolution steps.

### Configuration and Management Questions

**Q: How do I change the default admin password?**
A: Log in to the panel with the default credentials (admin/admin123), click on your username in the top right corner, and select "Change Password" from the dropdown menu. You will be prompted to enter your current password and set a new one.

**Q: Can I run multiple ETS2 servers on the same machine?**
A: Yes, the panel is designed to manage multiple ETS2 servers on a single machine. Each server is allocated unique ports and runs in its own directory. The number of servers you can run depends on your system resources and the number of players per server.

**Q: How do I backup my server data?**
A: The panel includes automatic backup functionality that runs daily. Manual backups can be created using the backup script: `sudo tar -czf backup-$(date +%Y%m%d).tar.gz /opt/ets2-panel /opt/ets2-servers`

**Q: How do I update the panel to a newer version?**
A: Updates can be applied by pulling the latest code from the repository and running the deployment script: `git pull origin main && ./deploy-panel.sh`. Always backup your data before updating.

### Server Management Questions

**Q: Why won't my ETS2 server start?**
A: Common causes include port conflicts, insufficient permissions, missing game files, or configuration errors. Check the server logs through the panel interface or system logs for specific error messages. Ensure that the required ports are not in use by other applications.

**Q: How do I configure server mods?**
A: Server mods can be installed by placing mod files in the server's mod directory and updating the server configuration to load the mods. The panel provides file management capabilities for uploading and managing mod files.

**Q: Can players connect to servers without the panel?**
A: Yes, once servers are running, players can connect directly using the server IP and port. The panel is used for server management and administration, not for player connections.

**Q: How do I set up automatic server restarts?**
A: Automatic server restarts can be configured through the panel's scheduling system. You can set up daily restarts during low-activity periods to maintain server performance and apply updates.

### Technical Questions

**Q: What database does the panel use?**
A: The panel uses SQLite by default, which is suitable for most installations. For high-traffic deployments, the system can be configured to use PostgreSQL or MySQL for better performance and scalability.

**Q: Is the panel secure for internet-facing deployments?**
A: Yes, the panel implements multiple security measures including HTTPS encryption, JWT authentication, input validation, and protection against common web vulnerabilities. However, you should follow security best practices including regular updates and strong passwords.

**Q: Can I customize the panel interface?**
A: Yes, the panel interface can be customized through theme modifications, CSS changes, and component customization. The React-based frontend provides flexibility for interface modifications.

**Q: Does the panel support clustering or high availability?**
A: The current version is designed for single-server deployments. High availability configurations may be possible with external load balancing and database clustering, but this requires advanced configuration and is not officially supported.

### Troubleshooting Questions

**Q: The panel loads but shows connection errors**
A: This typically indicates that the backend service is not running or is not accessible. Check the backend service status with `sudo systemctl status ets2-panel-backend` and review the service logs for error messages.

**Q: I can't access the panel from external networks**
A: Ensure that your firewall allows connections on ports 80 and 443, and that your router/cloud provider security groups are configured to allow these connections. Also verify that the panel is configured to listen on all interfaces (0.0.0.0) rather than just localhost.

**Q: Server performance is poor with multiple servers running**
A: Performance issues with multiple servers usually indicate resource constraints. Monitor CPU, memory, and disk usage to identify bottlenecks. Consider upgrading hardware or optimizing server configurations to reduce resource usage.

**Q: How do I recover from a corrupted database?**
A: If the database becomes corrupted, restore from the most recent backup using: `sudo systemctl stop ets2-panel-backend && cp /backup/database-backup.db /opt/ets2-panel/ets2-panel-backend/database.db && sudo systemctl start ets2-panel-backend`

## Support and Community

The ETS2 Server Panel project maintains an active community of users and contributors who provide support, share knowledge, and contribute to the project's development. Community participation is encouraged and provides valuable resources for users at all skill levels.

### Getting Help

When you encounter issues or have questions about the panel, several resources are available to provide assistance. The most effective approach is to start with the documentation and then escalate to community resources if needed.

**Documentation Resources:**
This comprehensive guide covers most common scenarios and issues. The troubleshooting section provides systematic approaches to diagnosing and resolving problems. Before seeking help from the community, review the relevant documentation sections to ensure you haven't missed important information.

**GitHub Issues:**
The project's GitHub repository includes an issue tracking system where you can report bugs, request features, and seek help with specific problems. When creating issues, provide detailed information including system specifications, error messages, and steps to reproduce the problem.

**Community Forums:**
Community forums provide a platform for users to share experiences, ask questions, and provide mutual support. Forums are particularly valuable for discussing best practices, sharing configuration tips, and getting advice from experienced users.

### Contributing to the Project

The ETS2 Server Panel is an open-source project that welcomes contributions from the community. Contributions can take many forms, from bug reports and documentation improvements to code contributions and feature development.

**Bug Reports:**
High-quality bug reports are valuable contributions that help improve the software for all users. Effective bug reports include detailed descriptions of the problem, steps to reproduce the issue, system information, and any relevant log files or error messages.

**Documentation Contributions:**
Documentation improvements help make the software more accessible to new users and reduce support burden. Documentation contributions can include corrections, clarifications, additional examples, or entirely new sections covering advanced topics.

**Code Contributions:**
Code contributions should follow the project's coding standards and development guidelines. Before beginning significant development work, discuss your plans with the project maintainers to ensure that your contributions align with the project's direction and requirements.

**Translation Contributions:**
The panel now supports multiple languages, and additional translations are welcome. Translation contributions help make the software accessible to users who prefer languages other than English and German.

### Project Roadmap

The ETS2 Server Panel project continues to evolve with new features and improvements based on user feedback and changing requirements. Understanding the project roadmap helps users plan for future capabilities and identify opportunities for contribution.

**Planned Features:**
Future releases may include enhanced monitoring capabilities, additional authentication options, improved user interface features, and expanded API functionality. Specific feature development is prioritized based on user demand and development resources.

**Long-term Vision:**
The long-term vision for the project includes support for additional game servers beyond ETS2, enhanced automation capabilities, and improved scalability for large deployments. Community feedback and contributions play important roles in shaping this vision.

### Commercial Support

While the ETS2 Server Panel is open-source software with community support, commercial support options may be available for organizations that require guaranteed response times, custom development, or specialized consulting services.

**Professional Services:**
Professional services may include custom installation and configuration, performance optimization, security assessments, and custom feature development. These services are provided by qualified professionals with extensive experience with the panel and related technologies.

**Training and Consulting:**
Training and consulting services can help organizations maximize their investment in the panel by ensuring that administrators are properly trained and that the system is optimally configured for their specific requirements.

---

**Contact Information:**
- **Author:** Simon Dialler
- **Project Repository:** https://github.com/BuzziGHG/ETS2-Panel
- **Version:** 1.0
- **Last Updated:** July 19, 2025

---

**Disclaimer:** This panel is an independent project and is not officially endorsed or supported by SCS Software, the developer of Euro Truck Simulator 2. Use of this software is at your own risk, and users are responsible for ensuring compliance with all applicable terms of service and licensing agreements.

