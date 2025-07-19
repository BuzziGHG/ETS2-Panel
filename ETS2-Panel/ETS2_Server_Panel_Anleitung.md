# Euro Truck Simulator 2 Server Panel - Vollständige Installations- und Bedienungsanleitung

**Autor:** Simon Dialler  
**Version:** 1.0  
**Datum:** 19. Juli 2025  
**Lizenz:** MIT License

---

## Inhaltsverzeichnis

1. [Einführung](#einführung)
2. [Systemanforderungen](#systemanforderungen)
3. [Schnellstart-Installation](#schnellstart-installation)
4. [Manuelle Installation](#manuelle-installation)
5. [Konfiguration](#konfiguration)
6. [HTTPS-Einrichtung](#https-einrichtung)
7. [Bedienung des Panels](#bedienung-des-panels)
8. [Server-Verwaltung](#server-verwaltung)
9. [Troubleshooting](#troubleshooting)
10. [Wartung und Updates](#wartung-und-updates)
11. [Sicherheit](#sicherheit)
12. [API-Dokumentation](#api-dokumentation)
13. [Entwicklung und Anpassung](#entwicklung-und-anpassung)
14. [FAQ](#faq)
15. [Support und Community](#support-und-community)

---

## Einführung

Das Euro Truck Simulator 2 (ETS2) Server Panel ist eine moderne, webbasierte Verwaltungsoberfläche für ETS2 Dedicated Server. Inspiriert von bewährten Game-Server-Panels wie Pterodactyl, bietet es eine intuitive und sichere Möglichkeit, mehrere ETS2-Server zentral zu verwalten.

### Hauptfunktionen

Das Panel bietet eine umfassende Palette von Funktionen für die professionelle Server-Verwaltung:

**Server-Management:** Das Herzstück des Panels ermöglicht die vollständige Kontrolle über ETS2 Dedicated Server. Benutzer können Server erstellen, konfigurieren, starten, stoppen und überwachen. Die Oberfläche bietet Echtzeit-Informationen über Server-Status, Spieleranzahl und Performance-Metriken.

**Benutzer-Verwaltung:** Ein rollenbasiertes Berechtigungssystem ermöglicht es Administratoren, verschiedene Benutzertypen zu verwalten. Admins haben vollständigen Zugriff, während normale Benutzer nur ihre eigenen Server verwalten können. Das System unterstützt sichere Authentifizierung mit JWT-Token und Passwort-Hashing.

**Echtzeit-Monitoring:** Das Panel bietet Live-Updates über WebSocket-Verbindungen. Server-Status, Logs und Performance-Daten werden in Echtzeit aktualisiert, ohne dass die Seite neu geladen werden muss.

**Sichere Architektur:** Das System wurde mit Sicherheit als oberste Priorität entwickelt. Alle Verbindungen können über HTTPS verschlüsselt werden, Passwörter werden mit bcrypt gehashed, und das System bietet Schutz vor gängigen Web-Angriffen.

### Technische Architektur

Das Panel basiert auf einer modernen, dreischichtigen Architektur:

**Frontend (React):** Eine responsive Single-Page-Application, die mit React 18, Tailwind CSS und shadcn/ui-Komponenten entwickelt wurde. Das Frontend kommuniziert über RESTful APIs und WebSockets mit dem Backend.

**Backend (Flask):** Ein Python-basierter API-Server, der Flask, SQLAlchemy und Flask-SocketIO verwendet. Das Backend verwaltet die Datenbank, authentifiziert Benutzer und steuert die ETS2-Server-Prozesse.

**Datenbank (SQLite):** Eine leichtgewichtige SQLite-Datenbank speichert Benutzer-, Server- und Konfigurationsdaten. Für größere Installationen kann das System einfach auf PostgreSQL oder MySQL migriert werden.

### Zielgruppe

Dieses Panel richtet sich an verschiedene Benutzergruppen:

**Gaming-Communities:** Clans und Communities, die mehrere ETS2-Server für verschiedene Events oder Regionen betreiben möchten.

**Hosting-Anbieter:** Unternehmen, die ETS2-Server-Hosting als Service anbieten und eine professionelle Verwaltungsoberfläche für ihre Kunden benötigen.

**Privatpersonen:** Enthusiasten, die ihre eigenen ETS2-Server für Freunde und Familie betreiben möchten.

**Entwickler:** Personen, die das Panel als Basis für eigene Projekte verwenden oder erweitern möchten.




## Systemanforderungen

Die erfolgreiche Installation und der Betrieb des ETS2 Server Panels erfordern bestimmte Hardware- und Software-Voraussetzungen. Diese Anforderungen wurden basierend auf umfangreichen Tests und der Analyse typischer Server-Workloads entwickelt.

### Hardware-Anforderungen

**Minimale Anforderungen:**
- **CPU:** 2 CPU-Kerne (x86_64 Architektur)
- **RAM:** 2 GB verfügbarer Arbeitsspeicher
- **Speicher:** 10 GB freier Festplattenspeicher
- **Netzwerk:** Stabile Internetverbindung mit mindestens 10 Mbit/s

**Empfohlene Anforderungen:**
- **CPU:** 4 CPU-Kerne oder mehr (Intel/AMD x86_64)
- **RAM:** 4 GB oder mehr verfügbarer Arbeitsspeicher
- **Speicher:** 50 GB oder mehr freier SSD-Speicher
- **Netzwerk:** Dedizierte Internetverbindung mit 100 Mbit/s oder mehr

**Produktionsumgebung:**
- **CPU:** 8 CPU-Kerne oder mehr mit hoher Taktfrequenz
- **RAM:** 8 GB oder mehr verfügbarer Arbeitsspeicher
- **Speicher:** 100 GB oder mehr auf schnellen NVMe-SSDs
- **Netzwerk:** Redundante Internetverbindung mit geringer Latenz

Die Hardware-Anforderungen skalieren mit der Anzahl der gleichzeitig betriebenen ETS2-Server. Jeder aktive Server benötigt zusätzlich etwa 512 MB RAM und moderate CPU-Ressourcen. Bei der Planung sollten auch Spitzenlasten berücksichtigt werden, die auftreten können, wenn mehrere Server gleichzeitig gestartet oder gestoppt werden.

### Software-Anforderungen

**Unterstützte Betriebssysteme:**
- Ubuntu 20.04 LTS oder neuer (empfohlen)
- Debian 11 (Bullseye) oder neuer
- CentOS 8 oder neuer (mit Anpassungen)
- Red Hat Enterprise Linux 8 oder neuer (mit Anpassungen)

**Erforderliche Software-Komponenten:**
- Python 3.8 oder neuer (Python 3.11 empfohlen)
- Node.js 16 oder neuer (Node.js 20 empfohlen)
- Nginx oder Apache HTTP Server
- Git für die Installation
- Curl und Wget für Downloads
- Systemd für Service-Management

**Optionale Komponenten:**
- UFW oder Firewalld für Firewall-Management
- Certbot für Let's Encrypt SSL-Zertifikate
- Supervisor für erweiterte Prozess-Überwachung
- Logrotate für Log-Management

### Netzwerk-Anforderungen

Das Panel benötigt verschiedene Netzwerk-Ports für den ordnungsgemäßen Betrieb:

**Standard-Ports:**
- **Port 80:** HTTP-Zugriff auf das Panel (wird zu HTTPS umgeleitet)
- **Port 443:** HTTPS-Zugriff auf das Panel (empfohlen)
- **Port 22:** SSH-Zugriff für Administration
- **Port 5000:** Backend-API (nur intern, nicht öffentlich zugänglich)

**ETS2-Server-Ports:**
- **Ports 27015-27030:** Standard-Bereich für ETS2 Dedicated Server
- **Ports 27015-27030 UDP:** Query-Ports für Server-Informationen

Die genauen Port-Anforderungen können je nach Konfiguration variieren. Das Installationsskript konfiguriert automatisch die erforderlichen Firewall-Regeln für Ubuntu und Debian-Systeme.

### Sicherheitsanforderungen

**Grundlegende Sicherheit:**
- Root-Zugriff für die Installation (kann nach der Installation eingeschränkt werden)
- Sichere SSH-Konfiguration mit Key-basierter Authentifizierung
- Regelmäßige Sicherheitsupdates des Betriebssystems
- Starke Passwörter für alle Benutzerkonten

**Erweiterte Sicherheit:**
- Fail2ban für Brute-Force-Schutz
- Intrusion Detection System (IDS)
- Regelmäßige Sicherheits-Audits
- Backup-Strategie für kritische Daten

### Cloud-Provider-Kompatibilität

Das Panel wurde auf verschiedenen Cloud-Plattformen getestet und ist kompatibel mit:

**Vollständig getestet:**
- Amazon Web Services (AWS) EC2
- Google Cloud Platform (GCP) Compute Engine
- Microsoft Azure Virtual Machines
- DigitalOcean Droplets
- Vultr Cloud Compute
- Linode

**Kompatibel (mit möglichen Anpassungen):**
- Hetzner Cloud
- OVHcloud
- Scaleway
- Oracle Cloud Infrastructure

Bei der Auswahl eines Cloud-Providers sollten die Netzwerk-Performance und die geografische Nähe zu den Zielspielern berücksichtigt werden, da dies die Latenz und das Spielerlebnis erheblich beeinflusst.


## Schnellstart-Installation

Die Schnellstart-Installation ermöglicht es, das ETS2 Server Panel mit einem einzigen Befehl zu installieren. Das automatisierte Installationsskript übernimmt alle erforderlichen Schritte und konfiguriert das System für den sofortigen Einsatz.

### Vorbereitung

Bevor Sie mit der Installation beginnen, stellen Sie sicher, dass Ihr System die Mindestanforderungen erfüllt und Sie über Root-Zugriff verfügen. Die Installation sollte auf einem frischen System durchgeführt werden, um Konflikte mit bestehender Software zu vermeiden.

**Wichtige Vorbereitungsschritte:**

Aktualisieren Sie zunächst Ihr System auf den neuesten Stand. Dies stellt sicher, dass alle Sicherheitsupdates installiert sind und reduziert die Wahrscheinlichkeit von Kompatibilitätsproblemen während der Installation.

```bash
sudo apt update && sudo apt upgrade -y
```

Stellen Sie sicher, dass Ihr System über eine stabile Internetverbindung verfügt, da während der Installation verschiedene Pakete und Abhängigkeiten heruntergeladen werden. Eine unterbrochene Internetverbindung kann zu einer unvollständigen Installation führen.

Wenn Sie eine Domain für das Panel verwenden möchten, konfigurieren Sie die DNS-Einstellungen so, dass sie auf die IP-Adresse Ihres Servers zeigen. Dies ist besonders wichtig, wenn Sie HTTPS mit Let's Encrypt aktivieren möchten.

### Download und Ausführung

Das Installationsskript kann direkt von der Kommandozeile heruntergeladen und ausgeführt werden:

```bash
# Installationsskript herunterladen
wget https://raw.githubusercontent.com/your-repo/ets2-panel/main/install-ets2-panel.sh

# Skript ausführbar machen
chmod +x install-ets2-panel.sh

# Installation starten
sudo ./install-ets2-panel.sh
```

Alternativ können Sie das Skript in einem Schritt herunterladen und ausführen:

```bash
curl -sSL https://raw.githubusercontent.com/your-repo/ets2-panel/main/install-ets2-panel.sh | sudo bash
```

### Interaktive Konfiguration

Das Installationsskript führt Sie durch eine Reihe von Konfigurationsfragen. Bereiten Sie die folgenden Informationen vor:

**Domain-Konfiguration:**
Das Skript fragt nach der Domain oder IP-Adresse, unter der das Panel erreichbar sein soll. Wenn Sie eine Domain verwenden, stellen Sie sicher, dass die DNS-Einstellungen korrekt konfiguriert sind. Für lokale Tests können Sie auch die IP-Adresse des Servers verwenden.

Beispiel: `panel.ihredomain.com` oder `192.168.1.100`

**HTTPS-Konfiguration:**
Sie werden gefragt, ob Sie HTTPS mit Let's Encrypt aktivieren möchten. Dies wird für Produktionsumgebungen dringend empfohlen. Für die Aktivierung benötigen Sie eine gültige Domain und eine E-Mail-Adresse für die Zertifikatsverwaltung.

**Administrator-Konto:**
Das Skript erstellt automatisch ein Administrator-Konto. Sie müssen einen Benutzernamen, ein sicheres Passwort und eine E-Mail-Adresse angeben. Diese Informationen werden für den ersten Login benötigt.

Empfohlene Passwort-Richtlinien:
- Mindestens 12 Zeichen lang
- Kombination aus Groß- und Kleinbuchstaben
- Zahlen und Sonderzeichen
- Keine Wörterbuch-Wörter oder persönliche Informationen

### Installationsprozess

Der Installationsprozess läuft vollständig automatisiert ab und umfasst folgende Schritte:

**System-Updates:** Das Skript aktualisiert zunächst alle Systempakete und installiert erforderliche Abhängigkeiten wie Python, Node.js, Nginx und andere Komponenten.

**SteamCMD-Installation:** SteamCMD wird heruntergeladen und konfiguriert, um ETS2 Dedicated Server-Dateien zu verwalten. Dies ermöglicht es dem Panel, Server automatisch zu installieren und zu aktualisieren.

**Panel-Installation:** Das Backend und Frontend des Panels werden installiert und konfiguriert. Dies umfasst die Erstellung von Python Virtual Environments, die Installation von Abhängigkeiten und die Konfiguration der Datenbank.

**Service-Konfiguration:** Systemd-Services werden erstellt und aktiviert, um sicherzustellen, dass das Panel automatisch beim Systemstart gestartet wird und bei Fehlern neu gestartet wird.

**Nginx-Konfiguration:** Der Webserver wird konfiguriert, um das Panel zu hosten und als Reverse Proxy für das Backend zu fungieren.

**Firewall-Konfiguration:** Die Firewall wird automatisch konfiguriert, um die erforderlichen Ports zu öffnen und gleichzeitig die Sicherheit zu gewährleisten.

### Erste Schritte nach der Installation

Nach erfolgreicher Installation erhalten Sie eine Zusammenfassung mit wichtigen Informationen:

```
╔══════════════════════════════════════════════════════════════╗
║                    Installation erfolgreich!                ║
╚══════════════════════════════════════════════════════════════╝

Panel-URL: https://panel.ihredomain.com
Admin-Benutzer: admin
Admin-E-Mail: admin@ihredomain.com

Wichtige Verzeichnisse:
  Panel: /opt/ets2-panel
  Server: /opt/ets2-servers
  SteamCMD: /opt/steamcmd

Nützliche Befehle:
  Service-Status: systemctl status ets2-panel-backend
  Logs anzeigen: journalctl -u ets2-panel-backend -f
  Nginx-Status: systemctl status nginx
```

**Erster Login:**
Öffnen Sie die angegebene URL in Ihrem Browser und melden Sie sich mit den während der Installation angegebenen Administrator-Anmeldedaten an. Das Panel sollte das Dashboard anzeigen und bereit für die Konfiguration Ihres ersten ETS2-Servers sein.

**Sicherheitsüberprüfung:**
Überprüfen Sie nach der Installation die Sicherheitseinstellungen:
- Stellen Sie sicher, dass HTTPS ordnungsgemäß funktioniert
- Überprüfen Sie die Firewall-Konfiguration
- Testen Sie die Backup-Funktionalität
- Ändern Sie Standard-Passwörter falls erforderlich

### Häufige Installationsprobleme

**Unzureichende Berechtigungen:**
Stellen Sie sicher, dass Sie das Skript mit sudo-Rechten ausführen. Ohne Root-Zugriff können erforderliche Systemänderungen nicht vorgenommen werden.

**Netzwerk-Probleme:**
Überprüfen Sie Ihre Internetverbindung, wenn Downloads fehlschlagen. Einige Firewalls oder Proxy-Server können die Installation beeinträchtigen.

**Port-Konflikte:**
Wenn andere Webserver auf dem System laufen, können Port-Konflikte auftreten. Stoppen Sie andere Webserver vor der Installation oder konfigurieren Sie alternative Ports.

**DNS-Probleme:**
Wenn Sie HTTPS aktivieren möchten, stellen Sie sicher, dass Ihre Domain korrekt auf den Server zeigt. Let's Encrypt kann keine Zertifikate für nicht erreichbare Domains ausstellen.


## Manuelle Installation

Für Benutzer, die mehr Kontrolle über den Installationsprozess benötigen oder das Panel in bestehende Infrastrukturen integrieren möchten, bietet die manuelle Installation maximale Flexibilität. Dieser Ansatz ermöglicht es, jeden Schritt individuell anzupassen und zu verstehen.

### Systemvorbereitung

Die manuelle Installation beginnt mit der sorgfältigen Vorbereitung des Systems. Dies umfasst die Installation aller erforderlichen Abhängigkeiten und die Konfiguration der Grundumgebung.

**Paket-Repository aktualisieren:**
```bash
sudo apt update && sudo apt upgrade -y
```

**Grundlegende Abhängigkeiten installieren:**
```bash
sudo apt install -y curl wget git unzip tar software-properties-common \
    apt-transport-https ca-certificates gnupg lsb-release build-essential \
    supervisor nginx
```

**Python 3.11 installieren:**
```bash
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update
sudo apt install -y python3.11 python3.11-venv python3.11-dev python3-pip
```

**Node.js 20 installieren:**
```bash
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs
```

**pnpm installieren:**
```bash
sudo npm install -g pnpm
```

### SteamCMD-Installation

SteamCMD ist erforderlich für die Verwaltung der ETS2 Dedicated Server-Dateien. Die Installation erfordert spezielle 32-Bit-Bibliotheken.

**32-Bit-Architektur aktivieren:**
```bash
sudo dpkg --add-architecture i386
sudo apt update
```

**SteamCMD-Abhängigkeiten installieren:**
```bash
sudo apt install -y lib32gcc-s1 steamcmd
```

**SteamCMD-Verzeichnis erstellen:**
```bash
sudo mkdir -p /opt/steamcmd
sudo chown $USER:$USER /opt/steamcmd
```

**SteamCMD herunterladen (falls nicht über Paket verfügbar):**
```bash
cd /opt/steamcmd
wget https://steamcdn-a.akamaihd.net/client/installer/steamcmd_linux.tar.gz
tar -xzf steamcmd_linux.tar.gz
rm steamcmd_linux.tar.gz
chmod +x steamcmd.sh
```

**Symbolischen Link erstellen:**
```bash
sudo ln -sf /opt/steamcmd/steamcmd.sh /usr/local/bin/steamcmd
```

### Backend-Installation

Das Backend basiert auf Flask und Python. Die Installation umfasst die Erstellung einer virtuellen Umgebung und die Installation aller erforderlichen Python-Pakete.

**Projektverzeichnisse erstellen:**
```bash
sudo mkdir -p /opt/ets2-panel/backend
sudo mkdir -p /opt/ets2-servers
sudo chown -R $USER:$USER /opt/ets2-panel /opt/ets2-servers
```

**Backend-Code herunterladen:**
```bash
cd /opt/ets2-panel
git clone https://github.com/your-repo/ets2-panel-backend.git backend
# Oder kopieren Sie die Backend-Dateien manuell
```

**Python Virtual Environment erstellen:**
```bash
cd /opt/ets2-panel/backend
python3.11 -m venv venv
source venv/bin/activate
```

**Python-Abhängigkeiten installieren:**
```bash
pip install --upgrade pip
pip install flask flask-sqlalchemy flask-jwt-extended flask-cors \
    flask-socketio psutil werkzeug bcrypt python-dotenv
```

**Requirements-Datei erstellen:**
```bash
pip freeze > requirements.txt
```

### Frontend-Installation

Das Frontend ist eine React-Anwendung, die gebaut und als statische Dateien bereitgestellt wird.

**Frontend-Code herunterladen:**
```bash
cd /opt/ets2-panel
git clone https://github.com/your-repo/ets2-panel-frontend.git frontend-src
# Oder kopieren Sie die Frontend-Dateien manuell
```

**Frontend-Abhängigkeiten installieren:**
```bash
cd frontend-src
pnpm install
```

**Frontend bauen:**
```bash
pnpm run build
```

**Gebaute Dateien kopieren:**
```bash
sudo mkdir -p /var/www/ets2-panel
sudo cp -r dist/* /var/www/ets2-panel/
sudo chown -R www-data:www-data /var/www/ets2-panel
```

### Datenbank-Konfiguration

Das Panel verwendet standardmäßig SQLite für die Datenspeicherung. Für Produktionsumgebungen kann PostgreSQL oder MySQL konfiguriert werden.

**SQLite-Datenbank initialisieren:**
```bash
cd /opt/ets2-panel/backend
source venv/bin/activate
python -c "
from src.models.user import db, User
from src.main import app

with app.app_context():
    db.create_all()
    
    # Admin-Benutzer erstellen
    admin = User(
        username='admin',
        email='admin@localhost',
        role='admin'
    )
    admin.set_password('admin123')  # Ändern Sie dieses Passwort!
    
    db.session.add(admin)
    db.session.commit()
    print('Datenbank initialisiert und Admin-Benutzer erstellt')
"
```

### Nginx-Konfiguration

Nginx fungiert als Reverse Proxy und stellt die Frontend-Dateien bereit.

**Nginx-Konfiguration erstellen:**
```bash
sudo tee /etc/nginx/sites-available/ets2-panel << 'EOF'
server {
    listen 80;
    server_name localhost;  # Ändern Sie dies zu Ihrer Domain
    
    # Frontend-Dateien
    root /var/www/ets2-panel;
    index index.html;
    
    # Frontend-Routing (SPA)
    location / {
        try_files $uri $uri/ /index.html;
    }
    
    # Backend-API
    location /api {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # WebSocket für Echtzeit-Updates
    location /socket.io {
        proxy_pass http://127.0.0.1:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # Sicherheits-Headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
}
EOF
```

**Site aktivieren:**
```bash
sudo ln -sf /etc/nginx/sites-available/ets2-panel /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl reload nginx
```

### Systemd-Services

Systemd-Services stellen sicher, dass das Panel automatisch startet und bei Fehlern neu gestartet wird.

**Backend-Service erstellen:**
```bash
sudo tee /etc/systemd/system/ets2-panel-backend.service << 'EOF'
[Unit]
Description=ETS2 Panel Backend
After=network.target

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=/opt/ets2-panel/backend
Environment=PATH=/opt/ets2-panel/backend/venv/bin
ExecStart=/opt/ets2-panel/backend/venv/bin/python src/main.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF
```

**Services aktivieren und starten:**
```bash
sudo systemctl daemon-reload
sudo systemctl enable ets2-panel-backend
sudo systemctl enable nginx
sudo systemctl start ets2-panel-backend
sudo systemctl start nginx
```

### Berechtigungen und Sicherheit

Korrekte Berechtigungen sind entscheidend für die Sicherheit und Funktionalität des Panels.

**Verzeichnis-Berechtigungen setzen:**
```bash
sudo chown -R www-data:www-data /opt/ets2-panel
sudo chown -R www-data:www-data /opt/ets2-servers
sudo chown -R www-data:www-data /opt/steamcmd
sudo chmod -R 755 /opt/ets2-panel
sudo chmod -R 755 /opt/ets2-servers
sudo chmod +x /opt/ets2-panel/backend/venv/bin/python
```

**Firewall konfigurieren:**
```bash
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
sudo ufw allow 27015:27030/tcp  # ETS2 Server Ports
sudo ufw allow 27015:27030/udp
sudo ufw --force enable
```

### Erste Tests

Nach der Installation sollten Sie die Funktionalität des Panels testen.

**Service-Status überprüfen:**
```bash
sudo systemctl status ets2-panel-backend
sudo systemctl status nginx
```

**Logs überprüfen:**
```bash
sudo journalctl -u ets2-panel-backend -f
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

**Panel-Zugriff testen:**
Öffnen Sie einen Webbrowser und navigieren Sie zu `http://ihre-server-ip`. Sie sollten die Login-Seite des Panels sehen.

### Erweiterte Konfiguration

**Umgebungsvariablen konfigurieren:**
```bash
sudo tee /opt/ets2-panel/backend/.env << 'EOF'
FLASK_ENV=production
SECRET_KEY=ihr-geheimer-schluessel-hier
DATABASE_URL=sqlite:///panel.db
JWT_SECRET_KEY=ihr-jwt-schluessel-hier
SERVERS_DIR=/opt/ets2-servers
STEAMCMD_PATH=/opt/steamcmd/steamcmd.sh
EOF
```

**Log-Rotation einrichten:**
```bash
sudo tee /etc/logrotate.d/ets2-panel << 'EOF'
/var/log/ets2-panel/*.log {
    daily
    missingok
    rotate 52
    compress
    delaycompress
    notifempty
    create 644 www-data www-data
    postrotate
        systemctl reload ets2-panel-backend
    endscript
}
EOF
```

Die manuelle Installation bietet vollständige Kontrolle über jeden Aspekt des Panels und ermöglicht es, das System an spezifische Anforderungen anzupassen. Obwohl sie mehr Zeit und technisches Verständnis erfordert, ist sie ideal für Produktionsumgebungen und komplexe Setups.


## HTTPS-Einrichtung

Die Einrichtung von HTTPS ist für Produktionsumgebungen unerlässlich und bietet Verschlüsselung, Authentizität und Vertrauen für Ihre Benutzer. Das Panel unterstützt sowohl Let's Encrypt für kostenlose Zertifikate als auch die Verwendung eigener SSL-Zertifikate.

### Let's Encrypt-Integration

Let's Encrypt bietet kostenlose, automatisch erneuerte SSL-Zertifikate und ist die empfohlene Lösung für die meisten Installationen.

**Voraussetzungen für Let's Encrypt:**
- Eine registrierte Domain, die auf Ihren Server zeigt
- Port 80 und 443 müssen öffentlich erreichbar sein
- Eine gültige E-Mail-Adresse für die Zertifikatsverwaltung

**Automatische HTTPS-Einrichtung:**
Das mitgelieferte HTTPS-Setup-Skript automatisiert den gesamten Prozess:

```bash
# HTTPS-Setup-Skript herunterladen
wget https://raw.githubusercontent.com/your-repo/ets2-panel/main/setup-https.sh
chmod +x setup-https.sh

# HTTPS einrichten
sudo ./setup-https.sh
```

Das Skript führt Sie durch die folgenden Schritte:

**Domain-Validierung:** Das Skript überprüft, ob Ihre Domain korrekt auf den Server zeigt. Dies ist entscheidend für die erfolgreiche Zertifikatserstellung.

**Certbot-Installation:** Falls noch nicht installiert, wird Certbot automatisch heruntergeladen und konfiguriert.

**Zertifikatserstellung:** Let's Encrypt erstellt ein SSL-Zertifikat für Ihre Domain und konfiguriert Nginx automatisch.

**Automatische Erneuerung:** Ein Cron-Job wird eingerichtet, um Zertifikate automatisch zu erneuern, bevor sie ablaufen.

### Manuelle HTTPS-Konfiguration

Für erweiterte Setups oder wenn Sie eigene Zertifikate verwenden möchten, können Sie HTTPS manuell konfigurieren.

**Certbot installieren:**
```bash
sudo apt install -y certbot python3-certbot-nginx
```

**SSL-Zertifikat erstellen:**
```bash
sudo certbot --nginx -d ihre-domain.com --email ihre-email@domain.com --agree-tos --non-interactive
```

**Nginx-Konfiguration überprüfen:**
Nach der Zertifikatserstellung aktualisiert Certbot automatisch Ihre Nginx-Konfiguration. Die aktualisierte Konfiguration sollte etwa so aussehen:

```nginx
server {
    listen 80;
    server_name ihre-domain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name ihre-domain.com;
    
    ssl_certificate /etc/letsencrypt/live/ihre-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/ihre-domain.com/privkey.pem;
    
    # SSL-Konfiguration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
    
    # Sicherheits-Headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    
    # Rest der Konfiguration...
}
```

### Erweiterte SSL-Konfiguration

Für maximale Sicherheit können Sie zusätzliche SSL-Optimierungen vornehmen.

**OCSP Stapling aktivieren:**
```nginx
ssl_stapling on;
ssl_stapling_verify on;
ssl_trusted_certificate /etc/letsencrypt/live/ihre-domain.com/chain.pem;
resolver 8.8.8.8 8.8.4.4 valid=300s;
resolver_timeout 5s;
```

**Perfect Forward Secrecy:**
```bash
# DH-Parameter generieren (kann einige Minuten dauern)
sudo openssl dhparam -out /etc/nginx/dhparam.pem 2048

# In Nginx-Konfiguration hinzufügen:
ssl_dhparam /etc/nginx/dhparam.pem;
```

**Content Security Policy (CSP):**
```nginx
add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self'; connect-src 'self' wss: https:;" always;
```

### Automatische Zertifikatserneuerung

Let's Encrypt-Zertifikate sind 90 Tage gültig und müssen regelmäßig erneuert werden.

**Cron-Job für automatische Erneuerung:**
```bash
# Crontab bearbeiten
sudo crontab -e

# Folgende Zeile hinzufügen (erneuert täglich um 12:00 Uhr)
0 12 * * * /usr/bin/certbot renew --quiet --nginx
```

**Systemd-Timer (alternative Methode):**
```bash
# Timer aktivieren (falls verfügbar)
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer

# Timer-Status überprüfen
sudo systemctl status certbot.timer
```

**Erneuerung testen:**
```bash
# Trockenlauf der Erneuerung
sudo certbot renew --dry-run
```

### Eigene SSL-Zertifikate

Wenn Sie bereits SSL-Zertifikate von einer anderen Zertifizierungsstelle haben, können Sie diese verwenden.

**Zertifikatsdateien kopieren:**
```bash
sudo mkdir -p /etc/ssl/certs/ets2-panel
sudo cp ihr-zertifikat.crt /etc/ssl/certs/ets2-panel/
sudo cp ihr-privater-schluessel.key /etc/ssl/private/ets2-panel/
sudo cp zwischenzertifikat.crt /etc/ssl/certs/ets2-panel/
```

**Nginx-Konfiguration anpassen:**
```nginx
ssl_certificate /etc/ssl/certs/ets2-panel/ihr-zertifikat.crt;
ssl_certificate_key /etc/ssl/private/ets2-panel/ihr-privater-schluessel.key;
```

### SSL-Monitoring und -Wartung

**Zertifikatsstatus überprüfen:**
```bash
# Zertifikatsinformationen anzeigen
sudo certbot certificates

# Ablaufdatum überprüfen
echo | openssl s_client -servername ihre-domain.com -connect ihre-domain.com:443 2>/dev/null | openssl x509 -noout -dates
```

**SSL-Konfiguration testen:**
```bash
# Nginx-Konfiguration testen
sudo nginx -t

# SSL-Verbindung testen
openssl s_client -connect ihre-domain.com:443 -servername ihre-domain.com
```

**Online-SSL-Tests:**
- SSL Labs Server Test: https://www.ssllabs.com/ssltest/
- Mozilla Observatory: https://observatory.mozilla.org/

### Troubleshooting HTTPS-Probleme

**Häufige Probleme und Lösungen:**

**Domain zeigt nicht auf den Server:**
```bash
# DNS-Auflösung überprüfen
nslookup ihre-domain.com
dig ihre-domain.com

# Wenn die IP nicht stimmt, DNS-Einstellungen korrigieren
```

**Port 80/443 nicht erreichbar:**
```bash
# Firewall-Status überprüfen
sudo ufw status
sudo iptables -L

# Ports öffnen
sudo ufw allow 80
sudo ufw allow 443
```

**Zertifikatserstellung fehlgeschlagen:**
```bash
# Certbot-Logs überprüfen
sudo tail -f /var/log/letsencrypt/letsencrypt.log

# Nginx-Konfiguration überprüfen
sudo nginx -t
```

**Mixed Content-Warnungen:**
Stellen Sie sicher, dass alle Ressourcen (CSS, JavaScript, Bilder) über HTTPS geladen werden. Das Panel ist so konfiguriert, dass es automatisch HTTPS verwendet, wenn verfügbar.

### Sicherheitsempfehlungen

**Regelmäßige Sicherheitsüberprüfungen:**
- Überwachen Sie Zertifikatsabläufe
- Führen Sie regelmäßige SSL-Tests durch
- Aktualisieren Sie SSL-Konfigurationen bei neuen Sicherheitsempfehlungen
- Überwachen Sie Sicherheitslogs auf verdächtige Aktivitäten

**Backup-Strategien:**
```bash
# Zertifikate sichern
sudo tar -czf letsencrypt-backup-$(date +%Y%m%d).tar.gz /etc/letsencrypt/

# Nginx-Konfiguration sichern
sudo cp /etc/nginx/sites-available/ets2-panel /etc/nginx/sites-available/ets2-panel.backup.$(date +%Y%m%d)
```

Die ordnungsgemäße HTTPS-Konfiguration ist entscheidend für die Sicherheit Ihres Panels und das Vertrauen Ihrer Benutzer. Mit Let's Encrypt ist die Einrichtung kostenlos und automatisiert, während erweiterte Konfigurationen maximale Sicherheit bieten.


## Bedienung des Panels

Das ETS2 Server Panel bietet eine intuitive und benutzerfreundliche Oberfläche für die Verwaltung von Euro Truck Simulator 2 Dedicated Servern. Die moderne React-basierte Benutzeroberfläche ist sowohl für Desktop- als auch für mobile Geräte optimiert.

### Anmeldung und erste Schritte

**Login-Prozess:**
Nach der Installation können Sie sich mit den während der Einrichtung erstellten Administrator-Anmeldedaten anmelden. Öffnen Sie Ihren Webbrowser und navigieren Sie zur Panel-URL. Die Login-Seite präsentiert sich mit einem modernen, professionellen Design.

Die Anmeldemaske erfordert Benutzername und Passwort. Das System verwendet sichere JWT-Token für die Authentifizierung und speichert die Sitzungsinformationen lokal im Browser. Nach erfolgreicher Anmeldung werden Sie automatisch zum Dashboard weitergeleitet.

**Standard-Anmeldedaten:**
- Benutzername: `admin`
- Passwort: `admin123` (sollte sofort geändert werden)

**Passwort ändern:**
Aus Sicherheitsgründen sollten Sie das Standard-Passwort sofort nach der ersten Anmeldung ändern. Klicken Sie auf Ihr Benutzerprofil in der oberen rechten Ecke und wählen Sie "Profil bearbeiten".

### Dashboard-Übersicht

Das Dashboard ist die zentrale Schaltstelle des Panels und bietet einen umfassenden Überblick über alle wichtigen Informationen.

**Statistik-Karten:**
Das Dashboard zeigt drei Hauptstatistiken in übersichtlichen Karten:

*Gesamt Server:* Zeigt die Gesamtanzahl aller konfigurierten Server in Ihrem Panel an. Dies umfasst sowohl laufende als auch gestoppte Server.

*Aktive Server:* Displays die Anzahl der derzeit laufenden Server. Diese Zahl wird in Echtzeit aktualisiert und zeigt den aktuellen Betriebsstatus.

*Benutzerrolle:* Zeigt Ihre aktuelle Berechtigung im System an (Admin, Benutzer, etc.).

**Server-Übersicht:**
Der untere Bereich des Dashboards zeigt eine detaillierte Liste aller Server mit folgenden Informationen:
- Server-Name und Beschreibung
- Aktueller Status (Läuft, Gestoppt, Startet, Stoppt)
- Port-Nummer und maximale Spieleranzahl
- Besitzer-Information
- Schnellaktionen (Start, Stop, Neustart)

**Echtzeit-Updates:**
Das Dashboard verwendet WebSocket-Verbindungen für Live-Updates. Server-Status-Änderungen, neue Server und andere wichtige Ereignisse werden automatisch angezeigt, ohne dass die Seite neu geladen werden muss.

### Navigation und Menüstruktur

**Hauptnavigation:**
Die Seitenleiste bietet Zugriff auf alle Hauptfunktionen des Panels:

*Dashboard:* Übersicht und Schnellzugriff auf alle wichtigen Funktionen
*Server:* Detaillierte Server-Verwaltung und -Konfiguration
*Benutzer:* Benutzerverwaltung (nur für Administratoren)
*Einstellungen:* System- und Panel-Konfiguration (nur für Administratoren)

**Responsive Design:**
Das Panel ist vollständig responsive und passt sich automatisch an verschiedene Bildschirmgrößen an. Auf mobilen Geräten wird die Navigation zu einem ausklappbaren Menü, um den verfügbaren Platz optimal zu nutzen.

**Benutzer-Menü:**
Das Benutzer-Menü in der oberen rechten Ecke bietet Zugriff auf:
- Profil-Einstellungen
- Passwort ändern
- Abmelden

### Server-Verwaltung im Dashboard

**Server-Aktionen:**
Jeder Server in der Dashboard-Liste bietet Schnellaktionen für die grundlegende Verwaltung:

*Start-Button:* Startet einen gestoppten Server. Der Button ist nur verfügbar, wenn der Server gestoppt ist.

*Stop-Button:* Stoppt einen laufenden Server sicher. Alle aktiven Verbindungen werden ordnungsgemäß beendet.

*Neustart-Button:* Führt einen kontrollierten Neustart durch, indem der Server gestoppt und anschließend wieder gestartet wird.

*Details-Button:* Öffnet die detaillierte Server-Verwaltungsseite mit erweiterten Konfigurationsoptionen.

**Status-Anzeigen:**
Server-Status werden durch farbkodierte Badges angezeigt:
- **Grün (Läuft):** Server ist aktiv und bereit für Verbindungen
- **Grau (Gestoppt):** Server ist nicht aktiv
- **Gelb (Startet):** Server wird gerade gestartet
- **Orange (Stoppt):** Server wird gerade gestoppt

### Benutzerfreundlichkeit und Accessibility

**Tastatur-Navigation:**
Das Panel unterstützt vollständige Tastatur-Navigation für bessere Accessibility. Alle interaktiven Elemente können mit der Tab-Taste erreicht und mit Enter oder Leertaste aktiviert werden.

**Farbkontrast und Lesbarkeit:**
Das Design folgt modernen Accessibility-Standards mit ausreichendem Farbkontrast und klarer Typografie. Wichtige Informationen sind auch ohne Farbe erkennbar.

**Mehrsprachigkeit:**
Das Panel ist für Mehrsprachigkeit vorbereitet. Derzeit ist die deutsche Benutzeroberfläche vollständig implementiert, weitere Sprachen können einfach hinzugefügt werden.

### Fehlerbehandlung und Feedback

**Benutzer-Feedback:**
Das Panel bietet umfassendes Feedback für alle Benutzeraktionen:
- Erfolgreiche Aktionen werden mit grünen Benachrichtigungen bestätigt
- Fehler werden mit roten Warnmeldungen angezeigt
- Lade-Zustände werden mit Spinner-Animationen visualisiert

**Fehlerbehandlung:**
Wenn Aktionen fehlschlagen, zeigt das Panel detaillierte Fehlermeldungen an, die dem Benutzer helfen, das Problem zu verstehen und zu lösen. Häufige Fehlerszenarien werden mit hilfreichen Lösungsvorschlägen versehen.

**Offline-Verhalten:**
Das Panel erkennt Verbindungsunterbrechungen und zeigt entsprechende Warnungen an. Wenn die Verbindung wiederhergestellt wird, synchronisiert sich das Panel automatisch mit dem aktuellen Server-Status.

### Performance und Optimierung

**Lazy Loading:**
Große Listen und Datenmengen werden bei Bedarf geladen, um die initiale Ladezeit zu minimieren und die Performance zu optimieren.

**Caching:**
Häufig verwendete Daten werden intelligent gecacht, um die Anzahl der Server-Anfragen zu reduzieren und die Benutzerfreundlichkeit zu verbessern.

**Optimierte Aktualisierungen:**
Das Panel verwendet effiziente Update-Mechanismen, die nur die tatsächlich geänderten Daten aktualisieren, anstatt die gesamte Seite neu zu laden.

### Anpassung und Personalisierung

**Theme-Unterstützung:**
Das Panel unterstützt verschiedene Farbthemes und kann an Corporate Design-Anforderungen angepasst werden. Das Standard-Theme bietet eine professionelle, moderne Optik.

**Dashboard-Anpassung:**
Benutzer können ihre Dashboard-Ansicht personalisieren, indem sie die Anzeige von Statistiken und Server-Listen nach ihren Präferenzen konfigurieren.

**Benachrichtigungseinstellungen:**
Benutzer können konfigurieren, welche Arten von Benachrichtigungen sie erhalten möchten und wie diese angezeigt werden sollen.

Die Benutzeroberfläche des ETS2 Server Panels wurde mit Fokus auf Benutzerfreundlichkeit, Effizienz und moderne Webstandards entwickelt. Sie bietet sowohl Anfängern als auch erfahrenen Administratoren eine intuitive Möglichkeit, ihre ETS2-Server zu verwalten.


## Troubleshooting

Dieser Abschnitt behandelt häufige Probleme und deren Lösungen, die bei der Installation, Konfiguration und dem Betrieb des ETS2 Server Panels auftreten können.

### Installationsprobleme

**Problem: Installationsskript bricht mit Berechtigungsfehlern ab**

*Symptome:* Das Installationsskript zeigt Fehler wie "Permission denied" oder "Operation not permitted" an.

*Ursachen:* Das Skript wird nicht mit ausreichenden Berechtigungen ausgeführt oder der Benutzer hat keinen sudo-Zugriff.

*Lösungen:*
```bash
# Stellen Sie sicher, dass Sie sudo verwenden
sudo ./install-ets2-panel.sh

# Überprüfen Sie sudo-Berechtigungen
sudo -l

# Falls sudo nicht verfügbar ist, als root ausführen
su -
./install-ets2-panel.sh
```

**Problem: Netzwerk-Timeouts während der Installation**

*Symptome:* Downloads schlagen fehl oder die Installation hängt bei Netzwerk-Operationen.

*Ursachen:* Langsame Internetverbindung, Firewall-Blockierungen oder DNS-Probleme.

*Lösungen:*
```bash
# DNS-Server überprüfen
cat /etc/resolv.conf

# Alternative DNS-Server verwenden
echo "nameserver 8.8.8.8" | sudo tee /etc/resolv.conf

# Internetverbindung testen
ping -c 4 google.com
wget -O /dev/null http://speedtest.wdc01.softlayer.com/downloads/test10.zip

# Proxy-Einstellungen überprüfen (falls vorhanden)
echo $http_proxy
echo $https_proxy
```

**Problem: Python-Abhängigkeiten können nicht installiert werden**

*Symptome:* pip-Installation schlägt fehl mit Compiler-Fehlern oder fehlenden Abhängigkeiten.

*Ursachen:* Fehlende Entwicklungstools oder veraltete pip-Version.

*Lösungen:*
```bash
# Build-Tools installieren
sudo apt install -y build-essential python3-dev

# pip aktualisieren
python3 -m pip install --upgrade pip

# Alternative: System-Pakete verwenden
sudo apt install -y python3-flask python3-sqlalchemy

# Virtual Environment neu erstellen
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip setuptools wheel
```

### Backend-Probleme

**Problem: Backend startet nicht oder stürzt sofort ab**

*Symptome:* Der ets2-panel-backend Service kann nicht gestartet werden oder zeigt Fehler in den Logs.

*Lösungen:*
```bash
# Service-Status überprüfen
sudo systemctl status ets2-panel-backend

# Detaillierte Logs anzeigen
sudo journalctl -u ets2-panel-backend -f

# Manuell starten für Debugging
cd /opt/ets2-panel/backend
source venv/bin/activate
python src/main.py

# Häufige Fixes:
# 1. Berechtigungen korrigieren
sudo chown -R www-data:www-data /opt/ets2-panel
sudo chown -R www-data:www-data /opt/ets2-servers

# 2. Abhängigkeiten neu installieren
source venv/bin/activate
pip install -r requirements.txt

# 3. Datenbank neu initialisieren
rm -f panel.db
python -c "from src.models.user import db; from src.main import app; app.app_context().push(); db.create_all()"
```

**Problem: Datenbank-Verbindungsfehler**

*Symptome:* Fehler wie "database is locked" oder "no such table" in den Logs.

*Lösungen:*
```bash
# SQLite-Datei überprüfen
ls -la /opt/ets2-panel/backend/panel.db

# Berechtigungen korrigieren
sudo chown www-data:www-data /opt/ets2-panel/backend/panel.db
sudo chmod 664 /opt/ets2-panel/backend/panel.db

# Datenbank-Integrität prüfen
sqlite3 /opt/ets2-panel/backend/panel.db "PRAGMA integrity_check;"

# Datenbank neu erstellen (Vorsicht: Datenverlust!)
cd /opt/ets2-panel/backend
source venv/bin/activate
python -c "
from src.models.user import db, User
from src.main import app
with app.app_context():
    db.drop_all()
    db.create_all()
    admin = User(username='admin', email='admin@localhost', role='admin')
    admin.set_password('admin123')
    db.session.add(admin)
    db.session.commit()
"
```

**Problem: API-Endpunkte geben 500-Fehler zurück**

*Symptome:* Frontend kann nicht mit Backend kommunizieren, API-Aufrufe schlagen fehl.

*Lösungen:*
```bash
# Backend-Logs überprüfen
sudo journalctl -u ets2-panel-backend -n 50

# Flask-Debug-Modus aktivieren (nur für Debugging)
cd /opt/ets2-panel/backend
source venv/bin/activate
export FLASK_DEBUG=1
python src/main.py

# CORS-Probleme beheben
# In src/main.py sicherstellen, dass CORS konfiguriert ist:
# from flask_cors import CORS
# CORS(app, origins=['http://localhost:3000', 'https://ihre-domain.com'])
```

### Frontend-Probleme

**Problem: Frontend lädt nicht oder zeigt weiße Seite**

*Symptome:* Browser zeigt leere Seite oder JavaScript-Fehler in der Konsole.

*Lösungen:*
```bash
# Browser-Konsole überprüfen (F12 -> Console)
# Häufige Fehler: CORS, 404 für Assets, JavaScript-Syntax-Fehler

# Frontend neu bauen
cd /opt/ets2-panel/frontend-src
pnpm install
pnpm run build
sudo cp -r dist/* /var/www/ets2-panel/

# Nginx-Konfiguration überprüfen
sudo nginx -t
sudo systemctl reload nginx

# Browser-Cache leeren
# Strg+F5 oder Strg+Shift+R
```

**Problem: Login funktioniert nicht**

*Symptome:* Anmeldung schlägt fehl, obwohl Anmeldedaten korrekt sind.

*Lösungen:*
```bash
# Backend-API testen
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'

# JWT-Konfiguration überprüfen
# In backend/.env oder src/main.py:
# JWT_SECRET_KEY muss gesetzt sein

# Benutzer in Datenbank überprüfen
cd /opt/ets2-panel/backend
sqlite3 panel.db "SELECT * FROM users;"

# Passwort zurücksetzen
cd /opt/ets2-panel/backend
source venv/bin/activate
python -c "
from src.models.user import db, User
from src.main import app
with app.app_context():
    user = User.query.filter_by(username='admin').first()
    if user:
        user.set_password('admin123')
        db.session.commit()
        print('Passwort zurückgesetzt')
    else:
        print('Benutzer nicht gefunden')
"
```

### Server-Management-Probleme

**Problem: ETS2-Server können nicht gestartet werden**

*Symptome:* Server-Start schlägt fehl oder Server stoppt sofort nach dem Start.

*Lösungen:*
```bash
# SteamCMD-Installation überprüfen
/opt/steamcmd/steamcmd.sh +quit

# ETS2 Dedicated Server-Dateien überprüfen
ls -la /opt/ets2-servers/ets2-dedicated/bin/linux_x64/

# Berechtigungen korrigieren
sudo chown -R www-data:www-data /opt/ets2-servers
sudo chmod +x /opt/ets2-servers/ets2-dedicated/bin/linux_x64/eurotrucks2_server

# Server manuell testen
cd /opt/ets2-servers/ets2-dedicated/bin/linux_x64/
./eurotrucks2_server -help

# Logs überprüfen
tail -f /opt/ets2-servers/*/logs/*.log
```

**Problem: Server-Ports sind nicht erreichbar**

*Symptome:* Spieler können sich nicht mit dem Server verbinden.

*Lösungen:*
```bash
# Firewall-Status überprüfen
sudo ufw status
sudo iptables -L

# ETS2-Ports öffnen
sudo ufw allow 27015:27030/tcp
sudo ufw allow 27015:27030/udp

# Port-Verfügbarkeit testen
netstat -tulpn | grep :27015
ss -tulpn | grep :27015

# Externe Erreichbarkeit testen
# Von einem anderen Computer:
telnet ihre-server-ip 27015
```

### Nginx-Probleme

**Problem: Nginx startet nicht oder zeigt Konfigurationsfehler**

*Symptome:* Webserver ist nicht erreichbar oder zeigt 502/503-Fehler.

*Lösungen:*
```bash
# Nginx-Konfiguration testen
sudo nginx -t

# Nginx-Status überprüfen
sudo systemctl status nginx

# Nginx-Logs überprüfen
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log

# Konfiguration neu laden
sudo systemctl reload nginx

# Bei Syntax-Fehlern: Backup-Konfiguration wiederherstellen
sudo cp /etc/nginx/sites-available/ets2-panel.backup /etc/nginx/sites-available/ets2-panel
sudo nginx -t && sudo systemctl reload nginx
```

**Problem: 502 Bad Gateway-Fehler**

*Symptome:* Nginx kann nicht mit dem Backend kommunizieren.

*Lösungen:*
```bash
# Backend-Status überprüfen
sudo systemctl status ets2-panel-backend
curl http://localhost:5000/api/health

# SELinux-Probleme (falls aktiviert)
sudo setsebool -P httpd_can_network_connect 1

# Proxy-Konfiguration überprüfen
# In /etc/nginx/sites-available/ets2-panel:
# proxy_pass http://127.0.0.1:5000; sollte korrekt sein
```

### Performance-Probleme

**Problem: Panel reagiert langsam oder hängt**

*Symptome:* Lange Ladezeiten, Timeouts oder unresponsive Benutzeroberfläche.

*Lösungen:*
```bash
# System-Ressourcen überprüfen
top
htop
free -h
df -h

# Backend-Performance analysieren
sudo journalctl -u ets2-panel-backend -n 100 | grep -i slow

# Datenbank optimieren
cd /opt/ets2-panel/backend
sqlite3 panel.db "VACUUM; ANALYZE;"

# Nginx-Caching aktivieren
# In /etc/nginx/sites-available/ets2-panel:
location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

### Netzwerk- und Sicherheitsprobleme

**Problem: SSL-Zertifikat-Fehler**

*Symptome:* Browser zeigt Sicherheitswarnungen oder HTTPS funktioniert nicht.

*Lösungen:*
```bash
# Zertifikatsstatus überprüfen
sudo certbot certificates

# Zertifikat erneuern
sudo certbot renew --force-renewal

# SSL-Konfiguration testen
openssl s_client -connect ihre-domain.com:443 -servername ihre-domain.com

# Nginx SSL-Konfiguration überprüfen
sudo nginx -t
```

### Monitoring und Debugging

**Umfassendes System-Debugging:**

```bash
#!/bin/bash
# Debug-Skript für ETS2 Panel

echo "=== ETS2 Panel Debug Report ==="
echo "Datum: $(date)"
echo

echo "=== System-Information ==="
uname -a
cat /etc/os-release
free -h
df -h
echo

echo "=== Service-Status ==="
sudo systemctl status ets2-panel-backend --no-pager
sudo systemctl status nginx --no-pager
echo

echo "=== Aktuelle Logs ==="
echo "--- Backend Logs ---"
sudo journalctl -u ets2-panel-backend -n 20 --no-pager
echo
echo "--- Nginx Error Logs ---"
sudo tail -n 20 /var/log/nginx/error.log
echo

echo "=== Netzwerk-Status ==="
netstat -tulpn | grep -E ':(80|443|5000|27015)'
echo

echo "=== Berechtigungen ==="
ls -la /opt/ets2-panel/
ls -la /opt/ets2-servers/
echo

echo "=== Firewall-Status ==="
sudo ufw status
echo

echo "Debug-Report abgeschlossen."
```

Speichern Sie dieses Skript als `debug-ets2-panel.sh`, machen Sie es ausführbar und führen Sie es aus, um einen umfassenden Systembericht zu erhalten.


## FAQ (Häufig gestellte Fragen)

### Allgemeine Fragen

**F: Kann ich das Panel auf einem Windows-Server installieren?**
A: Das Panel ist primär für Linux-Systeme (Ubuntu/Debian) entwickelt. Eine Windows-Installation ist theoretisch möglich, erfordert aber erhebliche Anpassungen. Wir empfehlen die Verwendung von Linux oder einer Linux-VM unter Windows.

**F: Wie viele ETS2-Server kann ich gleichzeitig betreiben?**
A: Die Anzahl hängt von Ihren Hardware-Ressourcen ab. Jeder ETS2-Server benötigt etwa 512 MB RAM und moderate CPU-Ressourcen. Ein Server mit 8 GB RAM kann typischerweise 10-15 Server gleichzeitig betreiben.

**F: Ist das Panel kostenlos?**
A: Ja, das ETS2 Server Panel ist Open Source und kostenlos nutzbar. Sie benötigen lediglich einen Server und optional eine Domain für den Betrieb.

**F: Kann ich das Panel für andere Spiele verwenden?**
A: Das Panel ist speziell für ETS2 entwickelt, aber die Architektur ist erweiterbar. Mit Entwicklungskenntnissen können Sie es für andere SCS-Spiele wie American Truck Simulator anpassen.

### Installation und Setup

**F: Welche Linux-Distribution wird empfohlen?**
A: Ubuntu 20.04 LTS oder neuer wird empfohlen. Debian 11+ funktioniert ebenfalls gut. Diese Distributionen bieten die beste Kompatibilität und Unterstützung.

**F: Kann ich das Panel auf einem Shared Hosting installieren?**
A: Nein, das Panel benötigt Root-Zugriff und die Möglichkeit, Services zu installieren. Sie benötigen einen VPS, dedizierten Server oder Cloud-Instance.

**F: Wie lange dauert die Installation?**
A: Die automatische Installation dauert typischerweise 15-30 Minuten, abhängig von der Internetgeschwindigkeit und Server-Performance.

**F: Kann ich das Panel auf einem Server mit anderen Anwendungen installieren?**
A: Grundsätzlich ja, aber es können Port-Konflikte auftreten. Stellen Sie sicher, dass die Ports 80, 443 und 5000 verfügbar sind.

### Konfiguration und Verwaltung

**F: Wie ändere ich den Standard-Admin-Benutzer?**
A: Nach der ersten Anmeldung können Sie über das Benutzer-Menü ein neues Admin-Konto erstellen und das Standard-Konto löschen oder deaktivieren.

**F: Kann ich mehrere Administratoren haben?**
A: Ja, Sie können beliebig viele Benutzer mit Admin-Rechten erstellen. Jeder Admin hat vollständigen Zugriff auf alle Panel-Funktionen.

**F: Wie sichere ich meine Server-Konfigurationen?**
A: Das Panel erstellt automatisch Backups der Server-Konfigurationen. Sie können auch manuelle Backups über die Einstellungen erstellen.

**F: Kann ich Server-Templates erstellen?**
A: Ja, Sie können Server-Konfigurationen als Templates speichern und für neue Server wiederverwenden.

### Server-Management

**F: Wie installiere ich Mods auf meinen ETS2-Servern?**
A: Mods können über die Server-Konfiguration hochgeladen und aktiviert werden. Das Panel unterstützt sowohl .scs-Dateien als auch Mod-Ordner.

**F: Kann ich Server automatisch starten lassen?**
A: Ja, in den Server-Einstellungen können Sie den automatischen Start beim System-Boot aktivieren.

**F: Wie überwache ich die Server-Performance?**
A: Das Panel bietet integrierte Monitoring-Tools mit CPU-, RAM- und Netzwerk-Statistiken. Zusätzlich können externe Monitoring-Tools integriert werden.

**F: Kann ich Server-Logs einsehen?**
A: Ja, alle Server-Logs sind über das Panel zugänglich und können in Echtzeit verfolgt werden.

### Netzwerk und Sicherheit

**F: Welche Ports muss ich in der Firewall öffnen?**
A: Für das Panel: 80 (HTTP), 443 (HTTPS). Für ETS2-Server: 27015-27030 (TCP/UDP). Das Installationsskript konfiguriert diese automatisch.

**F: Ist das Panel sicher?**
A: Ja, das Panel verwendet moderne Sicherheitsstandards: HTTPS-Verschlüsselung, JWT-Authentifizierung, bcrypt-Passwort-Hashing und Schutz vor gängigen Web-Angriffen.

**F: Kann ich das Panel hinter einem Reverse Proxy betreiben?**
A: Ja, das Panel funktioniert mit Reverse Proxies wie Cloudflare, nginx oder Apache. Beachten Sie die WebSocket-Konfiguration für Echtzeit-Updates.

**F: Wie aktiviere ich Zwei-Faktor-Authentifizierung?**
A: 2FA ist in der aktuellen Version noch nicht implementiert, ist aber für zukünftige Versionen geplant.

### Performance und Skalierung

**F: Wie kann ich die Performance des Panels verbessern?**
A: Verwenden Sie SSD-Speicher, ausreichend RAM und eine schnelle Internetverbindung. Für große Installationen können Sie Redis für Caching und PostgreSQL als Datenbank verwenden.

**F: Kann ich das Panel horizontal skalieren?**
A: Die aktuelle Version ist für Single-Server-Deployments optimiert. Horizontale Skalierung ist möglich, erfordert aber Anpassungen an der Architektur.

**F: Wie viele gleichzeitige Benutzer unterstützt das Panel?**
A: Das hängt von der Server-Hardware ab. Ein typischer VPS kann 50-100 gleichzeitige Panel-Benutzer unterstützen.

### Wartung und Updates

**F: Wie aktualisiere ich das Panel?**
A: Updates können über Git-Pull oder durch Herunterladen neuer Versionen durchgeführt werden. Ein Update-Skript automatisiert den Prozess.

**F: Wie oft sollte ich Backups erstellen?**
A: Tägliche automatische Backups werden empfohlen. Kritische Änderungen sollten sofort gesichert werden.

**F: Kann ich das Panel ohne Downtime aktualisieren?**
A: Kleinere Updates sind oft ohne Downtime möglich. Größere Updates können kurze Wartungsfenster erfordern.

### Troubleshooting

**F: Das Panel lädt nicht - was kann ich tun?**
A: Überprüfen Sie den Service-Status (`systemctl status ets2-panel-backend`), Nginx-Logs und Firewall-Einstellungen. Das Debug-Skript im Troubleshooting-Abschnitt hilft bei der Diagnose.

**F: Server starten nicht - woran liegt das?**
A: Häufige Ursachen sind fehlende Berechtigungen, Port-Konflikte oder unvollständige ETS2-Installation. Überprüfen Sie die Server-Logs für Details.

**F: Wie kann ich gelöschte Server wiederherstellen?**
A: Gelöschte Server können aus Backups wiederhergestellt werden, falls diese aktiviert sind. Ohne Backup ist eine Wiederherstellung nicht möglich.

### Entwicklung und Anpassung

**F: Kann ich das Panel anpassen?**
A: Ja, das Panel ist Open Source. Sie können das Frontend (React) und Backend (Flask) nach Ihren Anforderungen modifizieren.

**F: Wie kann ich neue Funktionen hinzufügen?**
A: Neue Features können durch Erweiterung der API-Endpunkte (Backend) und UI-Komponenten (Frontend) hinzugefügt werden.

**F: Gibt es eine API-Dokumentation?**
A: Ja, eine vollständige API-Dokumentation ist im Panel verfügbar und kann auch separat abgerufen werden.

**F: Kann ich Plugins entwickeln?**
A: Ein Plugin-System ist für zukünftige Versionen geplant. Derzeit sind Anpassungen durch direkte Code-Modifikation möglich.

### Lizenz und Support

**F: Unter welcher Lizenz steht das Panel?**
A: Das Panel steht unter der MIT-Lizenz, die kommerzielle und private Nutzung erlaubt.

**F: Wo bekomme ich Support?**
A: Community-Support ist über GitHub Issues verfügbar. Professioneller Support kann separat angefragt werden.

**F: Kann ich das Panel kommerziell nutzen?**
A: Ja, die MIT-Lizenz erlaubt kommerzielle Nutzung ohne Einschränkungen.

### Migration und Integration

**F: Kann ich von anderen Panel-Lösungen migrieren?**
A: Migration ist möglich, erfordert aber manuelle Übertragung der Server-Konfigurationen. Ein Migrations-Tool ist in Planung.

**F: Lässt sich das Panel in bestehende Systeme integrieren?**
A: Ja, über die REST-API kann das Panel in bestehende Infrastrukturen und Billing-Systeme integriert werden.

**F: Unterstützt das Panel LDAP/Active Directory?**
A: LDAP-Integration ist nicht standardmäßig verfügbar, kann aber durch Erweiterung des Authentifizierungs-Systems implementiert werden.

Diese FAQ wird regelmäßig aktualisiert. Wenn Sie weitere Fragen haben, die hier nicht beantwortet werden, erstellen Sie bitte ein Issue im GitHub-Repository oder kontaktieren Sie die Community.

