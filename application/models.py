#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2020 frey <summeriwiner@gmail.com>
#
# Distributed under terms of the MIT license.

"""

"""
from sqlalchemy import Column, Integer, String
from .database import Base
from passlib.apps import custom_app_context as pwd_context

from flask_login import UserMixin

class User(Base,UserMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), index=True, unique=True)
    password_hash = Column(String(32), unique=False)
    email = Column(String(120), unique=True)

    def __init__(self, name=None, password=None, email=None):
        self.name = name
        self.password_hash = pwd_context.encrypt(password)
        self.email = email

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def __repr__(self):
        return '<User %r>' % (self.name)

