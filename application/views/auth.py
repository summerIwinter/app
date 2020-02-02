#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2020 frey <summeriwiner@gmail.com>
#
# Distributed under terms of the MIT license.

"""

"""
from flask import Blueprint, request, jsonify, g
from ..models import User
from ..database import db_session
from .. import login_manager

auth = Blueprint('auth',__name__)

@login_manager.verify_token
def verify_token(token):
    # first try to authenticate by token
    g.user = None
    user = User.verify_auth_token(token)
    if not user:
        return False
    g.user = user
    return True

@auth.route('/',methods = ['POST'])
def new_user():
    # 用户注册
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        # missing arguments
        return jsonify({'code':00000,'message':'missing arguments'})
    if User.query.filter_by(username=username).first() is not None:
        # existing user
        return jsonify({'code':00000,'message':'existing user'})
    user = User(username=username)
    user.hash_password(password)
    db_session.add(user)
    db_session.commit()
    return jsonify({'code':20000,'message':'sucess'})

@auth.route('/login',methods = ['POST'])
def get_auth_token():
    # 登录，返回token
    username = request.json.get('username')
    password = request.json.get('password')
    user = User.query.filter_by(username=username).first()
    if user is not None and user.verify_password(password):
        g.user = user
        token = g.user.generate_auth_token(3600)
        return jsonify({'code':20000, 'data':{'token': token.decode('ascii'), 'duration': 600}})
    return jsonify({'code':60204,'message':'Account and password are incorrect.'})

@auth.route('/info')
@login_manager.login_required
def get_user_info():
    # 用户信息
    data = {
        'roles': ['admin'],
        'introduction': 'I am a super administrator',
        'avatar': 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif',
        'name': g.user.username
    }
    return jsonify({'code':20000,'data':data})

@auth.route('/logout',methods = ['POST'])
def logout():
    return jsonify({'code':20000,'message':'success'})
