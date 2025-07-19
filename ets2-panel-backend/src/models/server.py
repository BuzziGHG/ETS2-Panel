from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.models.user import db

class Server(db.Model):
    __tablename__ = 'servers'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    port = db.Column(db.Integer, unique=True, nullable=False)
    status = db.Column(db.String(20), default='stopped')
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    config_path = db.Column(db.String(255))
    pid = db.Column(db.Integer)
    max_players = db.Column(db.Integer, default=8)
    server_name = db.Column(db.String(100), default='ETS2 Server')
    password = db.Column(db.String(100))
    welcome_message = db.Column(db.Text)
    
    # Relationship
    owner = db.relationship('User', backref=db.backref('servers', lazy=True))
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'port': self.port,
            'status': self.status,
            'owner_id': self.owner_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'config_path': self.config_path,
            'pid': self.pid,
            'max_players': self.max_players,
            'server_name': self.server_name,
            'password': self.password,
            'welcome_message': self.welcome_message,
            'owner': self.owner.username if self.owner else None
        }

class ServerLog(db.Model):
    __tablename__ = 'server_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    server_id = db.Column(db.Integer, db.ForeignKey('servers.id'), nullable=False)
    level = db.Column(db.String(10), default='INFO')
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    server = db.relationship('Server', backref=db.backref('logs', lazy=True))
    
    def to_dict(self):
        return {
            'id': self.id,
            'server_id': self.server_id,
            'level': self.level,
            'message': self.message,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None
        }

