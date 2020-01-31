#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2020 frey <summeriwiner@gmail.com>
#
# Distributed under terms of the MIT license.

"""

"""
from flask import Blueprint, request, session 
from ..models import User
from ..database import db_session
from .. import login_manager
from flask_login import login_user, logout_user, current_user, login_required

auth = Blueprint('auth',__name__)

SUCCESS = {"state":0,"message":"success"}
FAIL = {"state":1,"message":"fail"}

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()

@auth.route("/")
def index():
    return "hello world"

@auth.route("/is_login")
@login_required
def is_login():
    return SUCCESS

@auth.route("/login",methods=["POST"])
def login():
    try:
        # json是否含有字段
        name = request.json["name"]
        password = request.json["password"]
    except:
        return FAIL
    user = User.query.filter_by(name=name).first()
    if user != None and user.verify_password(password):
        login_user(user)
        return SUCCESS
    return FAIL

@auth.route("/logout")
def logout():
    logout_user()
    return SUCCESS

@auth.route("/register",methods=["POST"])
def register():
    try:
        # 请求是否包含json字段
        # 数据库插入是否成功
        name = request.json["name"]
        password = request.json["password"]
        email = request.json["email"]
        user = User(name=name,password=password,email=email)
        db_session.add(user)
        db_session.commit()
    except:
        return FAIL
    return SUCCESS
