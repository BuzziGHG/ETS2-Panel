#!/bin/bash

# HTTPS-Setup für ETS2 Panel
# Dieses Skript richtet Let's Encrypt SSL-Zertifikate ein

set -e

# Farben
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

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

# Root-Rechte prüfen
check_root() {
    if [[ $EUID -ne 0 ]]; then
        error "Dieses Skript muss als root ausgeführt werden"
        exit 1
    fi
}

# Eingaben sammeln
collect_input() {
    echo "HTTPS-Setup für ETS2 Panel"
    echo "=========================="
    echo
    
    read -p "Domain für das Panel (z.B. panel.example.com): " DOMAIN
    if [[ -z "$DOMAIN" ]]; then
        error "Domain ist erforderlich"
        exit 1
    fi
    
    read -p "E-Mail-Adresse für Let's Encrypt: " EMAIL
    if [[ -z "$EMAIL" ]]; then
        error "E-Mail-Adresse ist erforderlich"
        exit 1
    fi
    
    # Domain-Validierung
    if ! dig +short "$DOMAIN" > /dev/null; then
        warning "Domain $DOMAIN scheint nicht zu existieren oder ist nicht erreichbar"
        read -p "Trotzdem fortfahren? (y/n): " CONTINUE
        if [[ "$CONTINUE" != "y" && "$CONTINUE" != "Y" ]]; then
            exit 1
        fi
    fi
}

# Certbot installieren
install_certbot() {
    log "Installiere Certbot..."
    
    apt-get update -y
    apt-get install -y certbot python3-certbot-nginx
    
    log "Certbot installiert"
}

# SSL-Zertifikat erstellen
create_certificate() {
    log "Erstelle SSL-Zertifikat für $DOMAIN..."
    
    # Nginx-Konfiguration für Domain aktualisieren
    sed -i "s/server_name .*/server_name $DOMAIN;/" /etc/nginx/sites-available/ets2-panel
    nginx -t && systemctl reload nginx
    
    # Zertifikat erstellen
    certbot --nginx \
        -d "$DOMAIN" \
        --email "$EMAIL" \
        --agree-tos \
        --non-interactive \
        --redirect
    
    log "SSL-Zertifikat erstellt"
}

# Automatische Erneuerung einrichten
setup_auto_renewal() {
    log "Richte automatische Zertifikatserneuerung ein..."
    
    # Cron-Job für automatische Erneuerung
    (crontab -l 2>/dev/null; echo "0 12 * * * /usr/bin/certbot renew --quiet --nginx") | crontab -
    
    # Systemd-Timer als Alternative (falls verfügbar)
    if systemctl list-unit-files | grep -q certbot.timer; then
        systemctl enable certbot.timer
        systemctl start certbot.timer
    fi
    
    log "Automatische Erneuerung eingerichtet"
}

# Firewall für HTTPS konfigurieren
configure_firewall() {
    log "Konfiguriere Firewall für HTTPS..."
    
    if command -v ufw &> /dev/null; then
        ufw allow 'Nginx Full'
        ufw --force enable
    elif command -v firewall-cmd &> /dev/null; then
        firewall-cmd --permanent --add-service=https
        firewall-cmd --reload
    fi
    
    log "Firewall konfiguriert"
}

# SSL-Konfiguration testen
test_ssl() {
    log "Teste SSL-Konfiguration..."
    
    # Nginx-Konfiguration testen
    nginx -t
    
    # SSL-Zertifikat testen
    if command -v openssl &> /dev/null; then
        echo | openssl s_client -servername "$DOMAIN" -connect "$DOMAIN:443" 2>/dev/null | openssl x509 -noout -dates
    fi
    
    log "SSL-Test abgeschlossen"
}

# Sicherheits-Headers hinzufügen
add_security_headers() {
    log "Füge Sicherheits-Headers hinzu..."
    
    # Nginx-Konfiguration erweitern
    cat >> /etc/nginx/sites-available/ets2-panel << 'EOF'

# Sicherheits-Headers
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header X-Content-Type-Options "nosniff" always;
add_header Referrer-Policy "no-referrer-when-downgrade" always;
add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

# SSL-Konfiguration optimieren
ssl_protocols TLSv1.2 TLSv1.3;
ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES128-SHA256:ECDHE-RSA-AES256-SHA384;
ssl_prefer_server_ciphers off;
ssl_session_cache shared:SSL:10m;
ssl_session_timeout 10m;
EOF
    
    # Nginx neustarten
    nginx -t && systemctl reload nginx
    
    log "Sicherheits-Headers hinzugefügt"
}

# Backup der Nginx-Konfiguration
backup_nginx_config() {
    log "Erstelle Backup der Nginx-Konfiguration..."
    
    cp /etc/nginx/sites-available/ets2-panel /etc/nginx/sites-available/ets2-panel.backup.$(date +%Y%m%d_%H%M%S)
    
    log "Backup erstellt"
}

# Hauptfunktion
main() {
    echo -e "${BLUE}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                    HTTPS-Setup für ETS2 Panel               ║"
    echo "║                  Let's Encrypt SSL-Zertifikate              ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    
    check_root
    collect_input
    backup_nginx_config
    install_certbot
    create_certificate
    setup_auto_renewal
    configure_firewall
    add_security_headers
    test_ssl
    
    echo
    echo -e "${GREEN}╔══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║                    HTTPS erfolgreich eingerichtet!          ║${NC}"
    echo -e "${GREEN}╚══════════════════════════════════════════════════════════════╝${NC}"
    echo
    echo -e "${BLUE}Panel-URL:${NC} https://$DOMAIN"
    echo -e "${BLUE}SSL-Status:${NC} Aktiv"
    echo -e "${BLUE}Auto-Renewal:${NC} Eingerichtet"
    echo
    echo -e "${YELLOW}Nützliche Befehle:${NC}"
    echo -e "  Zertifikat erneuern: certbot renew"
    echo -e "  SSL-Status prüfen: certbot certificates"
    echo -e "  Nginx-Status: systemctl status nginx"
    echo
}

# Fehlerbehandlung
trap 'error "HTTPS-Setup fehlgeschlagen in Zeile $LINENO"' ERR

# Skript ausführen
main "$@"

