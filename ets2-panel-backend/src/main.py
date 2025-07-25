import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_socketio import SocketIO
from datetime import timedelta

from src.models.user import db
from src.routes.user import user_bp
from src.routes.auth import auth_bp, check_if_token_revoked
from src.routes.servers import servers_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))

# Konfiguration
app.config['SECRET_KEY'] = 'ets2-panel-secret-key-change-in-production'
app.config['JWT_SECRET_KEY'] = 'ets2-panel-jwt-secret-change-in-production'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)

# CORS aktivieren
CORS(app, origins="*")

# JWT initialisieren
jwt = JWTManager(app)
jwt.token_in_blocklist_loader(check_if_token_revoked)

# SocketIO für Echtzeit-Updates
socketio = SocketIO(app, cors_allowed_origins="*")

# Blueprints registrieren
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(servers_bp, url_prefix='/api/servers')

# Datenbank konfigurieren
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Datenbank initialisieren
with app.app_context():
    db.create_all()
    
    # Standard-Admin-Benutzer erstellen falls keine Benutzer existieren
    from src.models.user import User
    if User.query.count() == 0:
        admin = User(
            username='admin',
            email='admin@ets2panel.local',
            role='admin'
        )
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print("Standard-Admin-Benutzer erstellt: admin / admin123")

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404

# SocketIO Events für Echtzeit-Updates
@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)

