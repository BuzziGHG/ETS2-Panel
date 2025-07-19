# ETS2 Server Management Panel - Design Konzept

## Überblick
Ein modernes, benutzerfreundliches Webpanel zur Verwaltung von Euro Truck Simulator 2 Dedicated Servern, inspiriert von Pterodactyl Panel.

## Architektur

### Backend (Flask)
- **API-Server**: RESTful API für alle Panel-Funktionen
- **Authentifizierung**: JWT-basierte Benutzeranmeldung
- **Server-Management**: Steuerung der ETS2-Server-Prozesse
- **Datenbankschicht**: SQLite für Benutzer- und Serverdaten
- **Sicherheit**: HTTPS, sichere Passwort-Hashing, Session-Management

### Frontend (React)
- **Dashboard**: Übersicht über alle Server und deren Status
- **Server-Management**: Start/Stop/Restart von Servern
- **Konfiguration**: Bearbeitung von Server-Einstellungen
- **Logs**: Echtzeit-Anzeige von Server-Logs
- **Benutzer-Management**: Admin-Panel für Benutzerverwaltung

## Kernfunktionen

### 1. Authentifizierung & Autorisierung
- **Login-System**: Sichere Benutzeranmeldung
- **Rollen**: Admin, Moderator, Benutzer
- **Session-Management**: Automatische Abmeldung bei Inaktivität
- **Passwort-Sicherheit**: Bcrypt-Hashing, Passwort-Richtlinien

### 2. Server-Management
- **Server-Erstellung**: Neue ETS2-Server erstellen
- **Prozess-Kontrolle**: Start, Stop, Restart, Kill
- **Status-Überwachung**: CPU, RAM, Spieleranzahl
- **Automatische Neustarts**: Bei Abstürzen oder geplant

### 3. Konfiguration
- **Server-Einstellungen**: server_config.sii bearbeiten
- **Mod-Management**: Mods hochladen und verwalten
- **Map-Konfiguration**: Verschiedene Karten auswählen
- **Netzwerk-Einstellungen**: Ports, IP-Bindung

### 4. Monitoring & Logs
- **Echtzeit-Logs**: Live-Anzeige der Server-Ausgabe
- **Performance-Metriken**: Grafische Darstellung der Serverleistung
- **Spieler-Tracking**: Verbundene Spieler anzeigen
- **Ereignis-Protokoll**: Wichtige Server-Ereignisse protokollieren

### 5. Datei-Management
- **Datei-Browser**: Server-Dateien durchsuchen und bearbeiten
- **Backup-System**: Automatische und manuelle Backups
- **Upload-Funktion**: Dateien über das Panel hochladen
- **Konfigurationstemplates**: Vorgefertigte Konfigurationen

## Technische Spezifikationen

### Backend-Technologien
- **Framework**: Flask (Python)
- **Datenbank**: SQLite (für einfache Installation)
- **Authentifizierung**: Flask-JWT-Extended
- **API**: RESTful mit JSON-Responses
- **Prozess-Management**: subprocess, psutil
- **WebSockets**: Flask-SocketIO für Echtzeit-Updates

### Frontend-Technologien
- **Framework**: React 18
- **Styling**: Tailwind CSS + shadcn/ui
- **Icons**: Lucide React
- **Charts**: Recharts für Performance-Grafiken
- **HTTP-Client**: Axios
- **WebSockets**: Socket.IO-Client

### Sicherheitsfeatures
- **HTTPS**: Let's Encrypt SSL-Zertifikate
- **CORS**: Konfigurierbare Cross-Origin-Richtlinien
- **Rate Limiting**: Schutz vor Brute-Force-Angriffen
- **Input Validation**: Validierung aller Benutzereingaben
- **File Upload Security**: Sichere Datei-Upload-Behandlung

## Benutzeroberfläche

### Dashboard
- **Server-Übersicht**: Karten-Layout mit Server-Status
- **Quick Actions**: Schnelle Server-Kontrollen
- **System-Status**: CPU, RAM, Festplatte des Host-Systems
- **Benachrichtigungen**: Wichtige Meldungen und Warnungen

### Server-Detail-Ansicht
- **Konsole**: Terminal-ähnliche Ausgabe der Server-Logs
- **Einstellungen**: Formulare zur Konfiguration
- **Dateien**: Datei-Browser mit Editor-Funktionalität
- **Spieler**: Liste der verbundenen Spieler

### Admin-Bereich
- **Benutzer-Management**: Benutzer erstellen, bearbeiten, löschen
- **System-Einstellungen**: Panel-Konfiguration
- **Backup-Verwaltung**: Backup-Zeitpläne und -Wiederherstellung
- **Logs**: System- und Audit-Logs

## Installation & Deployment

### Systemanforderungen
- **Betriebssystem**: Ubuntu 20.04+ / Debian 11+
- **Python**: 3.8+
- **Node.js**: 16+
- **RAM**: Mindestens 2GB
- **Festplatte**: 10GB freier Speicher

### Installationsprozess
1. **System-Updates**: Paketquellen aktualisieren
2. **Abhängigkeiten**: Python, Node.js, nginx installieren
3. **SteamCMD**: Für ETS2 Dedicated Server
4. **Panel-Installation**: Backend und Frontend einrichten
5. **SSL-Konfiguration**: Let's Encrypt einrichten
6. **Service-Setup**: Systemd-Services erstellen

## Datenbankschema

### Benutzer-Tabelle
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);
```

### Server-Tabelle
```sql
CREATE TABLE servers (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    port INTEGER UNIQUE NOT NULL,
    status VARCHAR(20) DEFAULT 'stopped',
    owner_id INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    config_path VARCHAR(255),
    pid INTEGER
);
```

### Logs-Tabelle
```sql
CREATE TABLE server_logs (
    id INTEGER PRIMARY KEY,
    server_id INTEGER REFERENCES servers(id),
    level VARCHAR(10),
    message TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## API-Endpunkte

### Authentifizierung
- `POST /api/auth/login` - Benutzeranmeldung
- `POST /api/auth/logout` - Benutzerabmeldung
- `GET /api/auth/me` - Aktuelle Benutzerinformationen

### Server-Management
- `GET /api/servers` - Alle Server auflisten
- `POST /api/servers` - Neuen Server erstellen
- `GET /api/servers/{id}` - Server-Details abrufen
- `PUT /api/servers/{id}` - Server-Konfiguration aktualisieren
- `DELETE /api/servers/{id}` - Server löschen

### Server-Kontrolle
- `POST /api/servers/{id}/start` - Server starten
- `POST /api/servers/{id}/stop` - Server stoppen
- `POST /api/servers/{id}/restart` - Server neustarten
- `GET /api/servers/{id}/status` - Server-Status abrufen

### Datei-Management
- `GET /api/servers/{id}/files` - Dateien auflisten
- `GET /api/servers/{id}/files/content` - Dateiinhalt abrufen
- `PUT /api/servers/{id}/files/content` - Dateiinhalt speichern
- `POST /api/servers/{id}/files/upload` - Datei hochladen

## Sicherheitskonzept

### Authentifizierung
- JWT-Token mit kurzer Lebensdauer (15 Minuten)
- Refresh-Token für automatische Verlängerung
- Sichere Passwort-Richtlinien (min. 8 Zeichen, Sonderzeichen)
- Brute-Force-Schutz mit Rate Limiting

### Autorisierung
- Rollenbasierte Zugriffskontrolle (RBAC)
- Server-spezifische Berechtigungen
- Admin-only Funktionen (Benutzer-Management, System-Einstellungen)

### Datenschutz
- Passwort-Hashing mit bcrypt
- Sichere Session-Verwaltung
- HTTPS-Verschlüsselung für alle Verbindungen
- Input-Validierung und -Sanitization

### Server-Sicherheit
- Prozess-Isolation für jeden ETS2-Server
- Beschränkte Dateisystem-Zugriffe
- Sichere Datei-Upload-Behandlung
- Regelmäßige Sicherheits-Updates

Dieses Design bietet eine solide Grundlage für ein professionelles ETS2-Server-Management-Panel mit modernen Sicherheitsstandards und benutzerfreundlicher Oberfläche.

