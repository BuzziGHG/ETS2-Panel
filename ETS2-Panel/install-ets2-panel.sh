#!/bin/bash

# ETS2 Server Panel - Automatisches Installationsskript
# Dieses Skript installiert einen Euro Truck Simulator 2 Dedicated Server
# mit einem benutzerdefinierten Webpanel ähnlich Pterodactyl

set -e  # Beende bei Fehlern

# Farben für die Ausgabe
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging-Funktion
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

error() {
    echo -e "${RED}[ERROR] $1${NC}" >&2
}

warning() {
    echo -e "${YELLOW}[WARNING] $1${NC}"
}

info() {
    echo -e "${BLUE}[INFO] $1${NC}"
}

# Banner anzeigen
show_banner() {
    echo -e "${BLUE}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                    ETS2 Server Panel                        ║"
    echo "║              Automatisches Installationsskript              ║"
    echo "║                                                              ║"
    echo "║  Installiert Euro Truck Simulator 2 Dedicated Server        ║"
    echo "║  mit einem benutzerdefinierten Webpanel                     ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

# Systemanforderungen prüfen
check_requirements() {
    log "Prüfe Systemanforderungen..."
    
    # Betriebssystem prüfen
    if [[ ! -f /etc/os-release ]]; then
        error "Betriebssystem nicht erkannt"
        exit 1
    fi
    
    source /etc/os-release
    if [[ "$ID" != "ubuntu" && "$ID" != "debian" ]]; then
        error "Dieses Skript unterstützt nur Ubuntu und Debian"
        exit 1
    fi
    
    # Root-Rechte prüfen
    if [[ $EUID -ne 0 ]]; then
        error "Dieses Skript muss als root ausgeführt werden"
        exit 1
    fi
    
    # Mindest-RAM prüfen (2GB)
    total_ram=$(free -m | awk 'NR==2{printf "%.0f", $2}')
    if [[ $total_ram -lt 2048 ]]; then
        warning "Weniger als 2GB RAM erkannt. Empfohlen sind mindestens 2GB."
    fi
    
    # Freier Speicherplatz prüfen (10GB)
    free_space=$(df / | awk 'NR==2{printf "%.0f", $4/1024/1024}')
    if [[ $free_space -lt 10 ]]; then
        error "Nicht genügend freier Speicherplatz. Mindestens 10GB erforderlich."
        exit 1
    fi
    
    log "Systemanforderungen erfüllt"
}

# Benutzer-Eingaben sammeln
collect_user_input() {
    log "Sammle Konfigurationsdaten..."
    
    # Domain/IP für das Panel
    if [[ -z "$PANEL_HOST" ]]; then
        read -p "Geben Sie die Domain oder IP-Adresse für das Panel ein (z.B. panel.example.com oder 192.168.1.100): " PANEL_HOST
        if [[ -z "$PANEL_HOST" ]]; then
            error "Domain/IP ist erforderlich"
            exit 1
        fi
    fi

    # HTTPS-Konfiguration
    if [[ "$PANEL_HOST" =~ ^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$ ]]; then
        warning "Eine IP-Adresse wurde erkannt. HTTPS (Let\'s Encrypt) ist mit IP-Adressen nicht möglich. Das Panel wird über HTTP verfügbar sein."
        ENABLE_HTTPS="n"
    else
        if [[ -z "$ENABLE_HTTPS" ]]; then
            read -p "HTTPS mit Let\'s Encrypt aktivieren? (y/n) [y]: " ENABLE_HTTPS_INPUT
            ENABLE_HTTPS=${ENABLE_HTTPS_INPUT:-y}
        fi
    fi
    
    if [[ "$ENABLE_HTTPS" == "y" || "$ENABLE_HTTPS" == "Y" ]]; then
        if [[ -z "$LETSENCRYPT_EMAIL" ]]; then
            read -p "E-Mail-Adresse für Let\'s Encrypt: " LETSENCRYPT_EMAIL
            if [[ -z "$LETSENCRYPT_EMAIL" ]]; then
                error "E-Mail-Adresse ist für Let\'s Encrypt erforderlich, wenn HTTPS aktiviert ist."
                exit 1
            fi
        fi
    fi
    
    # Admin-Benutzer
    if [[ -z "$ADMIN_USERNAME" ]]; then
        read -p "Admin-Benutzername [admin]: " ADMIN_USERNAME
        ADMIN_USERNAME=${ADMIN_USERNAME:-admin}
    fi
    
    if [[ -z "$ADMIN_PASSWORD" ]]; then
        read -s -p "Admin-Passwort: " ADMIN_PASSWORD
        echo
        if [[ -z "$ADMIN_PASSWORD" ]]; then
            error "Admin-Passwort ist erforderlich"
            exit 1
        fi
    fi
    
    if [[ -z "$ADMIN_EMAIL" ]]; then
        read -p "Admin-E-Mail: " ADMIN_EMAIL
        if [[ -z "$ADMIN_EMAIL" ]]; then
            error "Admin-E-Mail ist erforderlich"
            exit 1
        fi
    fi
    
    # Installationsverzeichnis
    INSTALL_DIR="/opt/ets2-panel"
    SERVERS_DIR="/opt/ets2-servers"
    STEAMCMD_DIR="/opt/steamcmd"
    
    log "Konfiguration abgeschlossen"
}

# System aktualisieren
update_system() {
    log "Aktualisiere System..."
    apt-get update -y
    apt-get upgrade -y
    log "System aktualisiert"
}

# Abhängigkeiten installieren
install_dependencies() {
    log "Installiere Abhängigkeiten..."
    
    # Basis-Pakete
    apt-get install -y \
        curl \
        wget \
        git \
        unzip \
        tar \
        software-properties-common \
        apt-transport-https \
        ca-certificates \
        gnupg \
        lsb-release \
        build-essential \
        supervisor \
        nginx
    
    # Python 3.11 installieren
    if ! command -v python3.11 &> /dev/null; then
        add-apt-repository ppa:deadsnakes/ppa -y
        apt-get update -y
        apt-get install -y python3.11 python3.11-venv python3.11-dev python3-pip
    fi
    
    # Node.js 20 installieren
    if ! command -v node &> /dev/null; then
        curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
        apt-get install -y nodejs
    fi
    
    # pnpm installieren
    if ! command -v pnpm &> /dev/null; then
        npm install -g pnpm
    fi
    
    log "Abhängigkeiten installiert"
}

# SteamCMD installieren
install_steamcmd() {
    log "Installiere SteamCMD..."
    
    # Sicherstellen, dass wget und tar installiert sind
    if ! command -v wget &> /dev/null; then
        log "Installiere wget..."
        apt-get install -y wget
    fi
    if ! command -v tar &> /dev/null; then
        log "Installiere tar..."
        apt-get install -y tar
    fi

    # 32-bit Bibliotheken für SteamCMD
    dpkg --add-architecture i386
    apt-get update -y
    apt-get install -y lib32gcc-s1
    
    # SteamCMD-Verzeichnis erstellen
    mkdir -p "$STEAMCMD_DIR"
    
    # SteamCMD herunterladen und entpacken
    cd "$STEAMCMD_DIR"
    if ! wget -qO steamcmd_linux.tar.gz https://steamcdn-a.akamaihd.net/client/installer/steamcmd_linux.tar.gz; then
        error "Fehler beim Herunterladen von SteamCMD. Bitte überprüfen Sie Ihre Internetverbindung oder die URL."
        exit 1
    fi
    
    if ! tar -xzf steamcmd_linux.tar.gz; then
        error "Fehler beim Entpacken von SteamCMD. Die heruntergeladene Datei könnte beschädigt sein."
        exit 1
    fi
    rm steamcmd_linux.tar.gz
    
    # Sicherstellen, dass das SteamCMD-Skript ausführbar ist
    chmod +x "$STEAMCMD_DIR/steamcmd.sh"
    
    # SteamCMD einmal ausführen, um die Verzeichnisstruktur zu erstellen
    log "Führe SteamCMD einmal aus, um die Verzeichnisstruktur zu erstellen..."
    (cd "$STEAMCMD_DIR" && ./steamcmd.sh +quit)
    
    log "SteamCMD installiert"
}

# ETS2 Dedicated Server installieren
install_ets2_server() {
    log "Installiere ETS2 Dedicated Server..."
    (cd "$STEAMCMD_DIR" && ./steamcmd.sh +force_install_dir "$SERVERS_DIR/ets2-dedicated" \
             +login anonymous \
             +app_update 1948160 validate \
             +quit)
    
    # Berechtigungen setzen
    chown -R www-data:www-data "$SERVERS_DIR"
    chmod +x "$SERVERS_DIR/ets2-dedicated/bin/linux_x64/eurotrucks2_server"
    
    log "ETS2 Dedicated Server installiert"
}

# Panel-Backend installieren
install_panel_backend() {
    log "Installiere Panel-Backend..."
    
    mkdir -p "$INSTALL_DIR"
    cd "$INSTALL_DIR"
    
    # Backend-Code von GitHub klonen
    git clone https://github.com/BuzziGHG/ETS2-Panel.git temp_repo
    cp -r temp_repo/ets2-panel-backend backend
    rm -rf temp_repo
    
    # Python Virtual Environment erstellen
    python3.11 -m venv backend/venv
    source backend/venv/bin/activate
    
    # Python-Abhängigkeiten installieren
    pip install --upgrade pip
    pip install flask flask-sqlalchemy flask-jwt-extended flask-cors flask-socketio psutil werkzeug
    
    log "Panel-Backend installiert"
}

# Panel-Frontend installieren
install_panel_frontend() {
    log "Installiere Panel-Frontend..."
    
    cd "$INSTALL_DIR"
    
    # Frontend-Code von GitHub klonen
    git clone https://github.com/BuzziGHG/ETS2-Panel.git temp_repo
    cp -r temp_repo/ets2-panel-frontend frontend
    rm -rf temp_repo
    
    # Frontend-Code bauen
    cd frontend
    pnpm install
    pnpm run build
    
    # Gebaute Dateien nach nginx-Verzeichnis kopieren
    cp -r dist/* /var/www/html/
    
    log "Panel-Frontend installiert"
}

# Nginx konfigurieren
configure_nginx() {
    log "Konfiguriere Nginx..."
    
    # Nginx-Konfiguration erstellen
    cat > /etc/nginx/sites-available/ets2-panel << EOF
server {
    listen 80;
    server_name $PANEL_HOST;
    
    # Frontend-Dateien
    root /var/www/html;
    index index.html;
    
    # Frontend-Routing (SPA)
    location / {
        try_files \$uri \$uri/ /index.html;
    }
    
    # Backend-API
    location /api {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
    
    # WebSocket für Echtzeit-Updates
    location /socket.io {
        proxy_pass http://127.0.0.1:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF
    
    # Site aktivieren
    ln -sf /etc/nginx/sites-available/ets2-panel /etc/nginx/sites-enabled/
    rm -f /etc/nginx/sites-enabled/default
    
    # Nginx-Konfiguration testen
    nginx -t
    
    log "Nginx konfiguriert"
}

# HTTPS mit Let's Encrypt einrichten
setup_https() {
    if [[ "$ENABLE_HTTPS" != "y" && "$ENABLE_HTTPS" != "Y" ]]; then
        return
    fi
    
    log "Richte HTTPS mit Let's Encrypt ein..."
    
    # Certbot installieren
    apt-get install -y certbot python3-certbot-nginx
    
    # SSL-Zertifikat erstellen
    certbot --nginx -d "$PANEL_HOST" --email "$LETSENCRYPT_EMAIL" --agree-tos --non-interactive
    
    # Automatische Erneuerung einrichten
    (crontab -l 2>/dev/null; echo "0 12 * * * /usr/bin/certbot renew --quiet") | crontab -
    
    log "HTTPS eingerichtet"
}

# Systemd-Services erstellen
create_systemd_services() {
    log "Erstelle Systemd-Services..."
    
    # Backend-Service
    cat > /etc/systemd/system/ets2-panel-backend.service << EOF
[Unit]
Description=ETS2 Panel Backend
After=network.target

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=$INSTALL_DIR/backend
Environment=PATH=$INSTALL_DIR/backend/venv/bin
ExecStart=$INSTALL_DIR/backend/venv/bin/python src/main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF
    
    # Services aktivieren
    systemctl daemon-reload
    systemctl enable ets2-panel-backend
    systemctl enable nginx
    
    log "Systemd-Services erstellt"
}

# Datenbank initialisieren
initialize_database() {
    log "Initialisiere Datenbank..."
    
    cd "$INSTALL_DIR/backend"
    source venv/bin/activate
    
    # Datenbank-Tabellen erstellen (würde normalerweise durch Flask-Migrate gemacht)
    python -c "
from src.models.user import db, User
from src.main import app

with app.app_context():
    db.create_all()
    
    # Admin-Benutzer erstellen
    admin = User(
        username='$ADMIN_USERNAME',
        email='$ADMIN_EMAIL',
        role='admin'
    )
    admin.set_password('$ADMIN_PASSWORD')
    
    db.session.add(admin)
    db.session.commit()
    print('Admin-Benutzer erstellt')
"
    
    log "Datenbank initialisiert"
}

# Berechtigungen setzen
set_permissions() {
    log "Setze Berechtigungen..."
    
    # Panel-Verzeichnis
    chown -R www-data:www-data "$INSTALL_DIR"
    chmod -R 755 "$INSTALL_DIR"
    
    # Server-Verzeichnis
    chown -R www-data:www-data "$SERVERS_DIR"
    chmod -R 755 "$SERVERS_DIR"
    
    # SteamCMD-Verzeichnis
    chown -R www-data:www-data "$STEAMCMD_DIR"
    chmod -R 755 "$STEAMCMD_DIR"
    
    # Nginx-Verzeichnis
    chown -R www-data:www-data /var/www/html
    
    log "Berechtigungen gesetzt"
}

# Services starten
start_services() {
    log "Starte Services..."
    
    systemctl restart nginx
    systemctl restart ets2-panel-backend
    
    # Status prüfen
    sleep 5
    if systemctl is-active --quiet nginx; then
        log "Nginx läuft"
    else
        error "Nginx konnte nicht gestartet werden"
    fi
    
    if systemctl is-active --quiet ets2-panel-backend; then
        log "Backend läuft"
    else
        error "Backend konnte nicht gestartet werden"
    fi
    
    log "Services gestartet"
}

# Firewall konfigurieren
configure_firewall() {
    log "Konfiguriere Firewall..."
    
    if command -v ufw &> /dev/null; then
        ufw --force enable
        ufw allow ssh
        ufw allow 'Nginx Full'
        ufw allow 27015:27030/tcp  # ETS2 Server Ports
        ufw allow 27015:27030/udp
        log "UFW Firewall konfiguriert"
    elif command -v firewall-cmd &> /dev/null; then
        systemctl enable firewalld
        systemctl start firewalld
        firewall-cmd --permanent --add-service=ssh
        firewall-cmd --permanent --add-service=http
        firewall-cmd --permanent --add-service=https
        firewall-cmd --permanent --add-port=27015-27030/tcp
        firewall-cmd --permanent --add-port=27015-27030/udp
        firewall-cmd --reload
        log "Firewalld konfiguriert"
    else
        warning "Keine Firewall gefunden. Bitte manuell konfigurieren."
    fi
}

# Installation abschließen
finish_installation() {
    log "Installation abgeschlossen!"
    
    echo
    echo -e "${GREEN}╔══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║                    Installation erfolgreich!                ║${NC}"
    echo -e "${GREEN}╚══════════════════════════════════════════════════════════════╝${NC}"
    echo
    echo -e "${BLUE}Panel-URL:${NC} http${ENABLE_HTTPS:+s}://$PANEL_HOST"
    echo -e "${BLUE}Admin-Benutzer:${NC} $ADMIN_USERNAME"
    echo -e "${BLUE}Admin-E-Mail:${NC} $ADMIN_EMAIL"
    echo
    echo -e "${YELLOW}Wichtige Verzeichnisse:${NC}"
    echo -e "  Panel: $INSTALL_DIR"
    echo -e "  Server: $SERVERS_DIR"
    echo -e "  SteamCMD: $STEAMCMD_DIR"
    echo
    echo -e "${YELLOW}Nützliche Befehle:${NC}"
    echo -e "  Service-Status: systemctl status ets2-panel-backend"
    echo -e "  Logs anzeigen: journalctl -u ets2-panel-backend -f"
    echo -e "  Nginx-Status: systemctl status nginx"
    echo
    echo -e "${GREEN}Das ETS2 Server Panel ist jetzt bereit!${NC}"
}

# Hauptfunktion
main() {
    show_banner
    check_requirements

    # Process arguments passed to the script
    local ARGS=()
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --panel-host)
            PANEL_HOST="$2"
            shift 2
            ;;
            --enable-https)
            ENABLE_HTTPS="$2"
            shift 2
            ;;
            --le-email)
            LETSENCRYPT_EMAIL="$2"
            shift 2
            ;;
            --admin-username)
            ADMIN_USERNAME="$2"
            shift 2
            ;;
            --admin-password)
            ADMIN_PASSWORD="$2"
            shift 2
            ;;
            --admin-email)
            ADMIN_EMAIL="$2"
            shift 2
            ;;
            *)
            ARGS+=("$1") # Collect any other arguments
            shift
            ;;
        esac
    done
    set -- "${ARGS[@]}" # Set positional parameters to remaining arguments

    collect_user_input
    
    log "Starte Installation..."
    
    update_system
    install_dependencies
    install_steamcmd
    install_ets2_server
    install_panel_backend
    install_panel_frontend
    configure_nginx
    setup_https
    create_systemd_services
    initialize_database
    set_permissions
    configure_firewall
    start_services
    
    finish_installation
}

# Fehlerbehandlung
trap 'error "Installation fehlgeschlagen in Zeile $LINENO"' ERR

# Skript ausführen
main "$@"

