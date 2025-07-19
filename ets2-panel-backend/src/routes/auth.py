from flask import Blueprint, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, create_refresh_token, get_jwt
from datetime import datetime, timedelta
from src.models.user import User, db

auth_bp = Blueprint('auth', __name__)

# JWT Blacklist für Logout
blacklisted_tokens = set()

@auth_bp.route('/login', methods=['POST'])
def login():
    """Benutzeranmeldung"""
    try:
        data = request.get_json()
        
        if not data or not data.get('username') or not data.get('password'):
            return jsonify({'error': 'Benutzername und Passwort sind erforderlich'}), 400
        
        username = data.get('username')
        password = data.get('password')
        
        # Benutzer suchen
        user = User.query.filter_by(username=username).first()
        
        if not user or not user.check_password(password):
            return jsonify({'error': 'Ungültige Anmeldedaten'}), 401
        
        if not user.is_active:
            return jsonify({'error': 'Benutzerkonto ist deaktiviert'}), 401
        
        # Letzten Login aktualisieren
        user.last_login = datetime.utcnow()
        db.session.commit()
        
        # JWT-Token erstellen
        access_token = create_access_token(
            identity=user.id,
            expires_delta=timedelta(hours=1)
        )
        refresh_token = create_refresh_token(
            identity=user.id,
            expires_delta=timedelta(days=30)
        )
        
        return jsonify({
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Anmeldefehler'}), 500

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """Benutzerabmeldung"""
    try:
        jti = get_jwt()['jti']
        blacklisted_tokens.add(jti)
        return jsonify({'message': 'Erfolgreich abgemeldet'}), 200
    except Exception as e:
        return jsonify({'error': 'Abmeldefehler'}), 500

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """Token erneuern"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user or not user.is_active:
            return jsonify({'error': 'Benutzer nicht gefunden oder deaktiviert'}), 401
        
        new_token = create_access_token(
            identity=current_user_id,
            expires_delta=timedelta(hours=1)
        )
        
        return jsonify({'access_token': new_token}), 200
        
    except Exception as e:
        return jsonify({'error': 'Token-Erneuerungsfehler'}), 500

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Aktuelle Benutzerinformationen abrufen"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'Benutzer nicht gefunden'}), 404
        
        return jsonify({'user': user.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': 'Fehler beim Abrufen der Benutzerinformationen'}), 500

@auth_bp.route('/register', methods=['POST'])
def register():
    """Neue Benutzerregistrierung (nur für Admins oder erste Installation)"""
    try:
        data = request.get_json()
        
        if not data or not all(k in data for k in ('username', 'email', 'password')):
            return jsonify({'error': 'Benutzername, E-Mail und Passwort sind erforderlich'}), 400
        
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        
        # Validierung
        if len(username) < 3:
            return jsonify({'error': 'Benutzername muss mindestens 3 Zeichen lang sein'}), 400
        
        if len(password) < 8:
            return jsonify({'error': 'Passwort muss mindestens 8 Zeichen lang sein'}), 400
        
        # Prüfen ob Benutzer bereits existiert
        if User.query.filter_by(username=username).first():
            return jsonify({'error': 'Benutzername bereits vergeben'}), 400
        
        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'E-Mail bereits registriert'}), 400
        
        # Ersten Benutzer als Admin erstellen
        user_count = User.query.count()
        role = 'admin' if user_count == 0 else 'user'
        
        # Neuen Benutzer erstellen
        user = User(
            username=username,
            email=email,
            role=role
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            'message': 'Benutzer erfolgreich registriert',
            'user': user.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Registrierungsfehler'}), 500

def check_if_token_revoked(jwt_header, jwt_payload):
    """Prüfen ob Token widerrufen wurde"""
    jti = jwt_payload['jti']
    return jti in blacklisted_tokens

