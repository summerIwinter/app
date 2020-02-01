#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2020 frey <summeriwiner@gmail.com>
#
# Distributed under terms of the MIT license.

"""

"""
from flask import Flask
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(24)

# 登录
from flask_httpauth import HTTPTokenAuth
login_manager = HTTPTokenAuth(scheme='token')

# 蓝图
from .views.auth import auth
app.register_blueprint(auth,url_prefix='/api/user')

# 数据库接口
from .database import db_session
@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()

