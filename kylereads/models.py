from flask_sqlalchemy import SQLAlchemy
from kylereads import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(80), unique = True)
    email = db.Column(db.String(120), unique = True)
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

class ReadingSession(db.Model):
    __tablename__ = 'readingsession'
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.String(80), db.ForeignKey('user.id'))
    user = db.relationship('User', backref = db.backref('users', lazy = 'dynamic'))
    title_id = db.Column(db.Integer, db.ForeignKey('title.id'))
    title = db.relationship('Title', backref = db.backref('readingsessions', lazy =  'dynamic'))
    pp = db.Column(db.Integer, unique = False)
    date = db.Column(db.Date)

    def __repr__(self):
        return '<ReadingSession {0}: {1}, {2}, {3} pages. {4}.>'.format(
            self.id, self.user, self.title, self.pp, self.date)

class Title(db.Model):
    __tablename__ = 'title'
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String, unique = False)
    author = db.Column(db.String, unique = False)
    genre = db.Column(db.String, unique = False)

    def __repr__(self):
        return '<Title {0} - {1}>'.format(self.title, self.author)
