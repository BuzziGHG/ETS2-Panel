import os
import subprocess
import psutil
import signal
import time
import json
from datetime import datetime
from pathlib import Path

class ServerManager:
    def __init__(self):
        self.servers_dir = "/opt/ets2-servers"
        self.steamcmd_dir = "/opt/steamcmd"
        self.ets2_server_app_id = "1948160"  # ETS2 Dedicated Server App ID
        self.running_servers = {}
        
        # Verzeichnisse erstellen falls sie nicht existieren
        os.makedirs(self.servers_dir, exist_ok=True)
        os.makedirs(self.steamcmd_dir, exist_ok=True)
    
    def install_steamcmd(self):
        """SteamCMD installieren falls nicht vorhanden"""
        steamcmd_path = os.path.join(self.steamcmd_dir, "steamcmd.sh")
        
        if not os.path.exists(steamcmd_path):
            try:
                # SteamCMD herunterladen
                subprocess.run([
                    "wget", "-O", "/tmp/steamcmd_linux.tar.gz",
                    "https://steamcdn-a.akamaihd.net/client/installer/steamcmd_linux.tar.gz"
                ], check=True)
                
                # Extrahieren
                subprocess.run([
                    "tar", "-xzf", "/tmp/steamcmd_linux.tar.gz", 
                    "-C", self.steamcmd_dir
                ], check=True)
                
                # Ausführbar machen
                os.chmod(steamcmd_path, 0o755)
                
                return True
            except subprocess.CalledProcessError:
                return False
        
        return True
    
    def install_ets2_server(self):
        """ETS2 Dedicated Server installieren/aktualisieren"""
        if not self.install_steamcmd():
            return False
        
        steamcmd_path = os.path.join(self.steamcmd_dir, "steamcmd.sh")
        server_install_dir = os.path.join(self.servers_dir, "ets2-dedicated")
        
        try:
            # ETS2 Dedicated Server installieren
            subprocess.run([
                steamcmd_path,
                "+force_install_dir", server_install_dir,
                "+login", "anonymous",
                "+app_update", self.ets2_server_app_id, "validate",
                "+quit"
            ], check=True)
            
            return True
        except subprocess.CalledProcessError:
            return False
    
    def create_server_files(self, server):
        """Server-Verzeichnis und Konfigurationsdateien erstellen"""
        server_dir = os.path.join(self.servers_dir, f"server_{server.id}")
        config_dir = os.path.join(server_dir, "config")
        
        # Verzeichnisse erstellen
        os.makedirs(server_dir, exist_ok=True)
        os.makedirs(config_dir, exist_ok=True)
        
        # Konfigurationsdatei erstellen
        config_path = os.path.join(config_dir, "server_config.sii")
        self._create_server_config(server, config_path)
        
        # Config-Pfad in Datenbank speichern
        server.config_path = config_path
        
        return server_dir
    
    def _create_server_config(self, server, config_path):
        """ETS2 Server-Konfigurationsdatei erstellen"""
        config_content = f"""SiiNunit
{{
server_config : _nameless.1.2.3.4 {{
 lobby_name: "{server.server_name}"
 description: "{server.description}"
 welcome_message: "{server.welcome_message}"
 max_players: {server.max_players}
 password: "{server.password}"
 max_vehicles_total: {server.max_players}
 max_ai_vehicles_player: 50
 max_ai_vehicles_player_spawn: 50
 connection_virtual_port: {server.port}
 query_virtual_port: {server.port + 1}
 connection_dedicated_port: {server.port}
 query_dedicated_port: {server.port + 1}
 server_logon_token: ""
 player_damage: true
 traffic: true
 hide_in_company: false
 hide_colliding: true
 force_speed_limiter: false
 mods_optioning: false
 timezones: 0
 service_no_collision: false
 in_menu: 1
 in_pause: 1
 start_on_load: false
 auto_save_period: 10
 auto_start: true
 disown_abandoned_trailer: -1
}}
}}"""
        
        with open(config_path, 'w', encoding='utf-8') as f:
            f.write(config_content)
    
    def update_server_config(self, server):
        """Server-Konfiguration aktualisieren"""
        if server.config_path and os.path.exists(server.config_path):
            self._create_server_config(server, server.config_path)
    
    def start_server(self, server):
        """ETS2 Server starten"""
        try:
            # Prüfen ob ETS2 Server installiert ist
            ets2_server_dir = os.path.join(self.servers_dir, "ets2-dedicated")
            server_executable = os.path.join(ets2_server_dir, "bin", "linux_x64", "eurotrucks2_server")
            
            if not os.path.exists(server_executable):
                if not self.install_ets2_server():
                    return {'success': False, 'error': 'ETS2 Server konnte nicht installiert werden'}
            
            # Server-Verzeichnis
            server_dir = os.path.join(self.servers_dir, f"server_{server.id}")
            
            # Prüfen ob Server bereits läuft
            if server.pid and self._is_process_running(server.pid):
                return {'success': False, 'error': 'Server läuft bereits'}
            
            # Server starten
            cmd = [
                server_executable,
                "-server_cfg", server.config_path,
                "-homedir", server_dir
            ]
            
            process = subprocess.Popen(
                cmd,
                cwd=server_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                preexec_fn=os.setsid
            )
            
            # Kurz warten und prüfen ob Prozess noch läuft
            time.sleep(2)
            if process.poll() is not None:
                stdout, stderr = process.communicate()
                return {
                    'success': False, 
                    'error': f'Server konnte nicht gestartet werden: {stderr.decode()}'
                }
            
            self.running_servers[server.id] = process
            
            return {'success': True, 'pid': process.pid}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def stop_server(self, server_id):
        """Server stoppen"""
        try:
            if server_id in self.running_servers:
                process = self.running_servers[server_id]
                
                # Graceful shutdown versuchen
                os.killpg(os.getpgid(process.pid), signal.SIGTERM)
                
                # Warten bis Prozess beendet ist
                try:
                    process.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    # Force kill falls graceful shutdown nicht funktioniert
                    os.killpg(os.getpgid(process.pid), signal.SIGKILL)
                    process.wait()
                
                del self.running_servers[server_id]
                
            return {'success': True}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def restart_server(self, server):
        """Server neustarten"""
        # Erst stoppen
        stop_result = self.stop_server(server.id)
        if not stop_result['success']:
            return stop_result
        
        # Kurz warten
        time.sleep(2)
        
        # Dann starten
        return self.start_server(server)
    
    def get_server_status(self, server_id):
        """Server-Status abrufen"""
        if server_id in self.running_servers:
            process = self.running_servers[server_id]
            if process.poll() is None:
                return 'running'
            else:
                # Prozess ist beendet, aus Liste entfernen
                del self.running_servers[server_id]
                return 'stopped'
        
        return 'stopped'
    
    def get_connected_players(self, server_id):
        """Verbundene Spieler abrufen (Placeholder)"""
        # TODO: Implementierung für ETS2 Server Player Query
        return []
    
    def get_server_performance(self, server_id):
        """Server-Performance-Metriken abrufen"""
        if server_id in self.running_servers:
            try:
                process = self.running_servers[server_id]
                proc = psutil.Process(process.pid)
                
                return {
                    'cpu_percent': proc.cpu_percent(),
                    'memory_mb': proc.memory_info().rss / 1024 / 1024,
                    'uptime_seconds': time.time() - proc.create_time()
                }
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                return None
        
        return None
    
    def delete_server_files(self, server):
        """Server-Dateien löschen"""
        server_dir = os.path.join(self.servers_dir, f"server_{server.id}")
        
        if os.path.exists(server_dir):
            import shutil
            shutil.rmtree(server_dir)
    
    def _is_process_running(self, pid):
        """Prüfen ob Prozess mit gegebener PID läuft"""
        try:
            return psutil.pid_exists(pid)
        except:
            return False
    
    def get_server_logs(self, server_id, lines=100):
        """Server-Logs aus Datei lesen"""
        server_dir = os.path.join(self.servers_dir, f"server_{server_id}")
        log_file = os.path.join(server_dir, "game.log")
        
        if not os.path.exists(log_file):
            return []
        
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                all_lines = f.readlines()
                return all_lines[-lines:] if len(all_lines) > lines else all_lines
        except:
            return []
    
    def backup_server(self, server_id):
        """Server-Backup erstellen"""
        server_dir = os.path.join(self.servers_dir, f"server_{server_id}")
        backup_dir = os.path.join(self.servers_dir, "backups")
        
        os.makedirs(backup_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"server_{server_id}_backup_{timestamp}.tar.gz"
        backup_path = os.path.join(backup_dir, backup_name)
        
        try:
            subprocess.run([
                "tar", "-czf", backup_path, "-C", 
                os.path.dirname(server_dir), 
                os.path.basename(server_dir)
            ], check=True)
            
            return {'success': True, 'backup_path': backup_path}
        except subprocess.CalledProcessError as e:
            return {'success': False, 'error': str(e)}

