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
from .. import login_manager

data_manage = Blueprint('data_manage',__name__)


@data_manage.route('/items')
@login_manager.login_required
def new_user():
    # 获取所有数据
    data = {
        'items':[
            { 'id': '001', 'name': '数据集名', 'create_time': '2018-12-05 15:59' },
            { 'id': '002', 'name': '数据集名', 'create_time': '2018-12-05 15:59' },
            { 'id': '003', 'name': '数据集名', 'create_time': '2018-12-05 15:59' },
            { 'id': '004', 'name': '数据集名', 'create_time': '2018-12-05 15:59' },
            { 'id': '005', 'name': '数据集名', 'create_time': '2018-12-05 15:59' },
            { 'id': '006', 'name': '数据集名', 'create_time': '2018-12-05 15:59' },
            { 'id': '007', 'name': '数据集名', 'create_time': '2018-12-05 15:59' }
        ]
    }
    return jsonify({'code':20000, 'data':data})

