from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.user import User, db
from src.models.server import Server, ServerLog
from src.utils.server_manager import ServerManager
import os

servers_bp = Blueprint('servers', __name__)
server_manager = ServerManager()

@servers_bp.route('/', methods=['GET'])
@jwt_required()
def get_servers():
    """Alle Server des Benutzers abrufen"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'Benutzer nicht gefunden'}), 404
        
        # Admins sehen alle Server, normale Benutzer nur ihre eigenen
        if user.is_admin():
            servers = Server.query.all()
        else:
            servers = Server.query.filter_by(owner_id=current_user_id).all()
        
        # Server-Status aktualisieren
        for server in servers:
            server.status = server_manager.get_server_status(server.id)
        
        db.session.commit()
        
        return jsonify({
            'servers': [server.to_dict() for server in servers]
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Fehler beim Abrufen der Server'}), 500

@servers_bp.route('/', methods=['POST'])
@jwt_required()
def create_server():
    """Neuen Server erstellen"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'Benutzer nicht gefunden'}), 404
        
        data = request.get_json()
        
        if not data or not data.get('name') or not data.get('port'):
            return jsonify({'error': 'Name und Port sind erforderlich'}), 400
        
        name = data.get('name')
        port = int(data.get('port'))
        description = data.get('description', '')
        max_players = int(data.get('max_players', 8))
        server_name = data.get('server_name', name)
        password = data.get('password', '')
        welcome_message = data.get('welcome_message', '')
        
        # Port-Validierung
        if port < 1024 or port > 65535:
            return jsonify({'error': 'Port muss zwischen 1024 und 65535 liegen'}), 400
        
        # Prüfen ob Port bereits verwendet wird
        if Server.query.filter_by(port=port).first():
            return jsonify({'error': 'Port bereits in Verwendung'}), 400
        
        # Server erstellen
        server = Server(
            name=name,
            description=description,
            port=port,
            owner_id=current_user_id,
            max_players=max_players,
            server_name=server_name,
            password=password,
            welcome_message=welcome_message
        )
        
        db.session.add(server)
        db.session.commit()
        
        # Server-Verzeichnis und Konfiguration erstellen
        server_manager.create_server_files(server)
        
        return jsonify({
            'message': 'Server erfolgreich erstellt',
            'server': server.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Fehler beim Erstellen des Servers'}), 500

@servers_bp.route('/<int:server_id>', methods=['GET'])
@jwt_required()
def get_server(server_id):
    """Server-Details abrufen"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'Benutzer nicht gefunden'}), 404
        
        server = Server.query.get(server_id)
        
        if not server:
            return jsonify({'error': 'Server nicht gefunden'}), 404
        
        # Berechtigung prüfen
        if not user.is_admin() and server.owner_id != current_user_id:
            return jsonify({'error': 'Keine Berechtigung'}), 403
        
        # Server-Status aktualisieren
        server.status = server_manager.get_server_status(server_id)
        db.session.commit()
        
        # Zusätzliche Informationen
        server_info = server.to_dict()
        server_info['players'] = server_manager.get_connected_players(server_id)
        server_info['performance'] = server_manager.get_server_performance(server_id)
        
        return jsonify({'server': server_info}), 200
        
    except Exception as e:
        return jsonify({'error': 'Fehler beim Abrufen der Server-Details'}), 500

@servers_bp.route('/<int:server_id>', methods=['PUT'])
@jwt_required()
def update_server(server_id):
    """Server-Konfiguration aktualisieren"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'Benutzer nicht gefunden'}), 404
        
        server = Server.query.get(server_id)
        
        if not server:
            return jsonify({'error': 'Server nicht gefunden'}), 404
        
        # Berechtigung prüfen
        if not user.is_admin() and server.owner_id != current_user_id:
            return jsonify({'error': 'Keine Berechtigung'}), 403
        
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Keine Daten empfangen'}), 400
        
        # Aktualisierbare Felder
        if 'name' in data:
            server.name = data['name']
        if 'description' in data:
            server.description = data['description']
        if 'max_players' in data:
            server.max_players = int(data['max_players'])
        if 'server_name' in data:
            server.server_name = data['server_name']
        if 'password' in data:
            server.password = data['password']
        if 'welcome_message' in data:
            server.welcome_message = data['welcome_message']
        
        db.session.commit()
        
        # Konfigurationsdatei aktualisieren
        server_manager.update_server_config(server)
        
        return jsonify({
            'message': 'Server erfolgreich aktualisiert',
            'server': server.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Fehler beim Aktualisieren des Servers'}), 500

@servers_bp.route('/<int:server_id>', methods=['DELETE'])
@jwt_required()
def delete_server(server_id):
    """Server löschen"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'Benutzer nicht gefunden'}), 404
        
        server = Server.query.get(server_id)
        
        if not server:
            return jsonify({'error': 'Server nicht gefunden'}), 404
        
        # Berechtigung prüfen
        if not user.is_admin() and server.owner_id != current_user_id:
            return jsonify({'error': 'Keine Berechtigung'}), 403
        
        # Server stoppen falls er läuft
        if server.status == 'running':
            server_manager.stop_server(server_id)
        
        # Server-Dateien löschen
        server_manager.delete_server_files(server)
        
        # Logs löschen
        ServerLog.query.filter_by(server_id=server_id).delete()
        
        # Server aus Datenbank löschen
        db.session.delete(server)
        db.session.commit()
        
        return jsonify({'message': 'Server erfolgreich gelöscht'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Fehler beim Löschen des Servers'}), 500

@servers_bp.route('/<int:server_id>/start', methods=['POST'])
@jwt_required()
def start_server(server_id):
    """Server starten"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'Benutzer nicht gefunden'}), 404
        
        server = Server.query.get(server_id)
        
        if not server:
            return jsonify({'error': 'Server nicht gefunden'}), 404
        
        # Berechtigung prüfen
        if not user.is_admin() and server.owner_id != current_user_id:
            return jsonify({'error': 'Keine Berechtigung'}), 403
        
        # Server starten
        result = server_manager.start_server(server)
        
        if result['success']:
            server.status = 'running'
            server.pid = result['pid']
            db.session.commit()
            
            # Log-Eintrag erstellen
            log = ServerLog(
                server_id=server_id,
                level='INFO',
                message=f'Server gestartet von {user.username}'
            )
            db.session.add(log)
            db.session.commit()
            
            return jsonify({
                'message': 'Server erfolgreich gestartet',
                'server': server.to_dict()
            }), 200
        else:
            return jsonify({'error': result['error']}), 500
        
    except Exception as e:
        return jsonify({'error': 'Fehler beim Starten des Servers'}), 500

@servers_bp.route('/<int:server_id>/stop', methods=['POST'])
@jwt_required()
def stop_server(server_id):
    """Server stoppen"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'Benutzer nicht gefunden'}), 404
        
        server = Server.query.get(server_id)
        
        if not server:
            return jsonify({'error': 'Server nicht gefunden'}), 404
        
        # Berechtigung prüfen
        if not user.is_admin() and server.owner_id != current_user_id:
            return jsonify({'error': 'Keine Berechtigung'}), 403
        
        # Server stoppen
        result = server_manager.stop_server(server_id)
        
        if result['success']:
            server.status = 'stopped'
            server.pid = None
            db.session.commit()
            
            # Log-Eintrag erstellen
            log = ServerLog(
                server_id=server_id,
                level='INFO',
                message=f'Server gestoppt von {user.username}'
            )
            db.session.add(log)
            db.session.commit()
            
            return jsonify({
                'message': 'Server erfolgreich gestoppt',
                'server': server.to_dict()
            }), 200
        else:
            return jsonify({'error': result['error']}), 500
        
    except Exception as e:
        return jsonify({'error': 'Fehler beim Stoppen des Servers'}), 500

@servers_bp.route('/<int:server_id>/restart', methods=['POST'])
@jwt_required()
def restart_server(server_id):
    """Server neustarten"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'Benutzer nicht gefunden'}), 404
        
        server = Server.query.get(server_id)
        
        if not server:
            return jsonify({'error': 'Server nicht gefunden'}), 404
        
        # Berechtigung prüfen
        if not user.is_admin() and server.owner_id != current_user_id:
            return jsonify({'error': 'Keine Berechtigung'}), 403
        
        # Server neustarten
        result = server_manager.restart_server(server)
        
        if result['success']:
            server.status = 'running'
            server.pid = result['pid']
            db.session.commit()
            
            # Log-Eintrag erstellen
            log = ServerLog(
                server_id=server_id,
                level='INFO',
                message=f'Server neugestartet von {user.username}'
            )
            db.session.add(log)
            db.session.commit()
            
            return jsonify({
                'message': 'Server erfolgreich neugestartet',
                'server': server.to_dict()
            }), 200
        else:
            return jsonify({'error': result['error']}), 500
        
    except Exception as e:
        return jsonify({'error': 'Fehler beim Neustarten des Servers'}), 500

@servers_bp.route('/<int:server_id>/logs', methods=['GET'])
@jwt_required()
def get_server_logs(server_id):
    """Server-Logs abrufen"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'Benutzer nicht gefunden'}), 404
        
        server = Server.query.get(server_id)
        
        if not server:
            return jsonify({'error': 'Server nicht gefunden'}), 404
        
        # Berechtigung prüfen
        if not user.is_admin() and server.owner_id != current_user_id:
            return jsonify({'error': 'Keine Berechtigung'}), 403
        
        # Parameter für Paginierung
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 50, type=int)
        level = request.args.get('level', None)
        
        # Query erstellen
        query = ServerLog.query.filter_by(server_id=server_id)
        
        if level:
            query = query.filter_by(level=level)
        
        # Logs abrufen (neueste zuerst)
        logs = query.order_by(ServerLog.timestamp.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'logs': [log.to_dict() for log in logs.items],
            'total': logs.total,
            'pages': logs.pages,
            'current_page': page,
            'per_page': per_page
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Fehler beim Abrufen der Logs'}), 500

