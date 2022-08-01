from enum import unique
import bcrypt
# from sqlalchemy import ForeignKey, Integer
from app import db
from sqlalchemy.orm import relationship
from flask_jwt_extended import create_access_token
from datetime import timedelta
from passlib.hash import bcrypt



class Task(db.Model):
        
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    text = db.Column(db.String(250), nullable=False)
    status = db.Column(db.Boolean(), nullable=False, default=False)
    

# class Role(Base):

#     __tablename__ = 'role'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(250), nullable=False, unique=True)


# class User(Base):

#     __tablename__ = 'user'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(250), nullable=False)
#     password = db.Column(db.String(100), nullable=False)
    # task = relationship('Task', back_populates="user")
    # tasks = relationship('Task', backref='user', lazy=True, nullable=True)
    # role = relationship('Role', backref='user', lazy=True)

    # def __init__(self, **kwargs):
    #     self.name = kwargs.get('name')
    #     self.email = kwargs.get('email')
    #     self.password = bcrypt.hash(kwargs.get('password'))

    # def get_token(self, expire_time=24):
    #     expire_delta = timedelta(expire_time)
    #     token = create_access_token(
    #         identity=self.id, expires_delta=expire_delta  
    #     )
    #     return token

    # def authenticate(cls, email, password):
    #     user = cls.query.filter(cls.email == email).one()
    #     if not bcrypt.verify(password, user.password):
    #         raise Exception('No user width this password')
        
    #     return user
