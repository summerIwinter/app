#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2020 frey <summeriwiner@gmail.com>
#
# Distributed under terms of the MIT license.

"""

"""

from application import app
from application.database import db_session
from application.database import init_db

from application.models import User
import os
if not os.path.exists('/tmp/aidata/test.db'):
    init_db()
    user =User(username='admin')
    user.hash_password('password')
    db_session.add(user)
    db_session.commit()
app.run(debug=True)
