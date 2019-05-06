from flask_sqlalchemy import SQLAlchemy
import bcrypt
import datetime
import hashlib
import os

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password_digest = db.Column(db.String, nullable=False)

    # Session info
    session_token = db.Column(db.String,nullable=False, unique=True)
    session_expiration = db.Column(db.DateTime, nullable = False)
    update_token = db.Column(db.String, nullable=False, unique=True)

    def __init__(self, **kwargs):
        self.email = kwargs.get('email')
        self.password_digest = bcrypt.hashpw(kwargs.get('password').encode('utf8'),
            bcrypt.gensalt(rounds=13))
        self.renew_session()

    # Randomly generates session/update tokens
    def _urlsafe_base_64(self):
        return hashlib.sha1(os.urandom(64)).hexdigest()

    # Generates new tokens and resets expiration time
    def renew_session(self):
        self.session_token = self._urlsafe_base_64()
        self.session_expiration = datetime.datetime.now() + datetime.timedelta(days=1)
        self.update_token = self._urlsafe_base_64()

    def verify_password(self, password):
        return bcrypt.checkpw(password.encode('utf8'), self.password_digest)

    def verify_session_token(self, session_token):
        return session_token == self.session_token and \
        datetime.datetime.now() < self.session_expiration

    def verify_update_token(self, update_token):
        return update_token == self.update_token

class Teams(db.Model):
    __tablename__ = 'teams'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable = False)
    away_team = db.relationship('Away', cascade = 'delete')
    home_team = db.relationship('Home', cascade = 'delete')
    team_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, **kwargs):
        self.name = kwargs.get('name', '')
        self.team_id = kwargs.get('team_id')

    def serialize(self):
        return {
            'id' : self.id,
            'name' : self.name
        }

class Away(db.Model):
    __tablename__ = 'away'
    id = db.Column(db.Integer, primary_key = True)
    away_score = db.Column(db.Integer, nullable = False)
    away_id = db.Column(db.Integer, db.ForeignKey('teams.id'))

    def __init__(self, **kwargs):
        self.away_score = kwargs.get('away_score', 0)
        self.away_id = kwargs.get('away_id')

    def serialize(self):
        return {
            'id' : self.id,
            'away_score' : self.away_score
        }

class Home(db.Model):
    __tablename__ = 'home'
    id = db.Column(db.Integer, primary_key = True)
    home_score = db.Column(db.Integer, nullable = False)
    home_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable = False)

    def __init__(self, **kwargs):
        self.home_score = kwargs.get('home_score', 0)
        self.home_id = kwargs.get('home_id')

    def serialize(self):
        return {
            'id' : self.id,
            'away_score' : self.home_score
        }
