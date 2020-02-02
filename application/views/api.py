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
import uuid

api = Blueprint('api',__name__)


@api.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file and file.filename[-4:]=='.csv':
        file_id = str(uuid.uuid4())
        file.save('/tmp/aidata/'+file_id+'.csv')
        return jsonify({'code':20000,'data':{'file_id':file_id}})
    return jsonify({'code':00000,'message':'error'})
