#!/bin/bash

# ETS2 Panel Deployment-Skript
# Dieses Skript baut und deployed das Panel

set -e

# Farben
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

info() {
    echo -e "${BLUE}[INFO] $1${NC}"
}

# Konfiguration
INSTALL_DIR="/opt/ets2-panel"
BACKEND_DIR="$INSTALL_DIR/backend"
FRONTEND_DIR="$INSTALL_DIR/frontend"
NGINX_DIR="/var/www/html"

# Backend kopieren und konfigurieren
deploy_backend() {
    log "Deploye Backend..."
    
    # Backend-Verzeichnis erstellen
    sudo mkdir -p "$BACKEND_DIR"
    
    # Backend-Dateien kopieren
    sudo cp -r ets2-panel-backend/* "$BACKEND_DIR/"
    
    # Virtual Environment erstellen falls nicht vorhanden
    if [[ ! -d "$BACKEND_DIR/venv" ]]; then
        sudo python3.11 -m venv "$BACKEND_DIR/venv"
    fi
    
    # Abhängigkeiten installieren
    sudo "$BACKEND_DIR/venv/bin/pip" install -r "$BACKEND_DIR/requirements.txt"
    
    # Berechtigungen setzen
    sudo chown -R www-data:www-data "$BACKEND_DIR"
    sudo chmod +x "$BACKEND_DIR/venv/bin/python"
    
    log "Backend deployed"
}

# Frontend bauen und deployen
deploy_frontend() {
    log "Deploye Frontend..."
    
    # Frontend bauen
    cd ets2-panel-frontend
    pnpm install
    pnpm run build
    
    # Frontend-Dateien kopieren
    sudo mkdir -p "$NGINX_DIR"
    sudo cp -r dist/* "$NGINX_DIR/"
    
    # Berechtigungen setzen
    sudo chown -R www-data:www-data "$NGINX_DIR"
    
    log "Frontend deployed"
}

# Services neustarten
restart_services() {
    log "Starte Services neu..."
    
    sudo systemctl restart ets2-panel-backend
    sudo systemctl restart nginx
    
    # Status prüfen
    sleep 3
    if sudo systemctl is-active --quiet ets2-panel-backend; then
        log "Backend läuft"
    else
        echo "Backend-Status:"
        sudo systemctl status ets2-panel-backend --no-pager
    fi
    
    if sudo systemctl is-active --quiet nginx; then
        log "Nginx läuft"
    else
        echo "Nginx-Status:"
        sudo systemctl status nginx --no-pager
    fi
}

# Hauptfunktion
main() {
    info "Starte Panel-Deployment..."
    
    deploy_backend
    deploy_frontend
    restart_services
    
    log "Deployment abgeschlossen!"
    echo
    echo "Panel ist verfügbar unter: http://localhost"
    echo "Standard-Login: admin / admin123"
}

main "$@"

