from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_login import LoginManager
from flask_marshmallow import Marshmallow
import secrets

# set variables for class instantiation
login_manager = LoginManager()
ma = Marshmallow()
db = SQLAlchemy()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key=True)
    display_name = db.Column(db.String(150), nullable=False, default='')
    email = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String, nullable=True, default='')
    g_auth_verify = db.Column(db.Boolean, default=False)
    token = db.Column(db.String, default='', unique=True)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, email, display_name='', password='', token='', g_auth_verify=False):
        self.id = self.set_id()
        self.display_name = display_name
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token(24)
        self.g_auth_verify = g_auth_verify

    def set_token(self, length):
        return secrets.token_hex(length)

    def set_id(self):
        return str(uuid.uuid4())

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def __repr__(self):
        return f'User {self.display_name} has been added to the database'

class Game(db.Model):
    id = db.Column(db.String, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    system = db.Column(db.String(100))
    genre = db.Column(db.String(100))
    beaten = db.Column(db.Boolean, default=False)
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable=False)

    def __init__(self, title, system, genre, purchased, beaten, user_token, id=''):
        self.id = self.set_id()
        self.title = title
        self.system = system
        self.genre = genre
        self.beaten = beaten
        self.user_token = user_token

    def __repr__(self):
        return f'{self.title} has been added to your backlog.'

    def set_id(self):
        return (secrets.token_urlsafe())

class GameSchema(ma.Schema):
    class Meta:
        fields = ['id', 'title', 'system', 'genre', 'beaten']

game_schema = GameSchema()
games_schema = GameSchema(many=True)