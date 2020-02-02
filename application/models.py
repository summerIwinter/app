#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2020 frey <summeriwiner@gmail.com>
#
# Distributed under terms of the MIT license.

"""

"""
from sqlalchemy import Column, Integer, String, Table, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .database import Base
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from . import app
import datetime

user_data = Table('users_datas',Base.metadata,
    Column('users_id',Integer,ForeignKey('users.id')),
    Column('datas_id',Integer,ForeignKey('datas.id'))
)
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(32), index=True, unique=True)
    password_hash = Column(String(64))
    datas = relationship("Data",secondary=user_data)

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=600):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})
    
    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None    # valid token, but expired
        except BadSignature:
            return None    # invalid token
        user = User.query.get(data['id'])
        return user

class Data(Base):
    __tablename__ = 'datas'
    id = Column(Integer,primary_key=True)
    name = Column(String(32))
    describe = Column(String(200))
    create_time = Column(DateTime, default=datetime.datetime.now)
    data_type = Column(Integer)
    data_path = Column(String(32))
    def __init__(self,name,describe,data_path,data_type=0):
        self.name =name
        self.describe=describe
        self.data_path = data_path
        self.data_type = data_type



