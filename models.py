from enum import unique
from logging import exception
import bcrypt
from app import db
from flask_jwt_extended import create_access_token
from datetime import timedelta
from passlib.hash import bcrypt


class Task(db.Model):
        
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    text = db.Column(db.String(250), nullable=False)
    status = db.Column(db.Boolean(), nullable=False, default=False)
    admin_edit = db.Column(db.Boolean(), nullable=False, default=False)

    
class AdminUserTask(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    
    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.password = bcrypt.hash(kwargs.get('password'))

    def get_token(self, expire_time=24):
        expire_delta = timedelta(expire_time)
        token = create_access_token(
            identity=self.id, expires_delta=expire_delta  
        )
        return token
    
    @classmethod
    def authenticate(cls, name, password):
        
        user = cls.query.filter(cls.name == name).one()
        
        if not bcrypt.verify(password, user.password):
            raise Exception('No user width this password')
        
        return user


class TokenBlocklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, index=True)
    created_at = db.Column(db.DateTime, nullable=False)