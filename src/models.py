import os
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    salt = db.Column(db.String(40), nullable=False)
    hashed_password = db.Column(db.String(240), nullable=False)
    is_active = db.Column(db.Boolean(), default=True, nullable=False)

    def __init__(self, **kwargs):
        print(kwargs)
        self.email = kwargs.get('email')
        self.salt = os.urandom(16).hex()
        self.set_password(kwargs.get('password'))

    @classmethod
    def create(cls, **kwargs):
        user = cls(**kwargs)
        db.session.add(user)
        try: 
            db.session.commit()
        except Exception as error:
            print(error.args)
            db.session.rollback()
            return False
        return user

    def set_password(self, password):
        print(generate_password_hash(
            f"{password}{self.salt}"
        ))
        self.hashed_password = generate_password_hash(
            f"{password}{self.salt}"
        )

    def check_password(self, password):
        return check_password_hash(
            self.hashed_password,
            f"{password}{self.salt}"
        )

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }