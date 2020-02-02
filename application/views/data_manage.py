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
from ..models import Data
from ..database import db_session
from .. import login_manager

data_manage = Blueprint('data_manage',__name__)


@data_manage.route('/items')
@login_manager.login_required
def get_items():
    # 获取所有数据
    user = g.user
    print(user.datas)
    print(user.datas[0].id)
    print(user.datas[0].create_time.strftime('%Y-%m-%d %H:%M'))

    data = { 'items': []}
    for item in user.datas:
        data['items'].append({
            'id':item.id,
            'name':item.name,
            'create_time':item.create_time.strftime('%Y-%m-%d %H:%M')
        })
    return jsonify({'code':20000, 'data':data})

@data_manage.route('/item',methods=['POST'])
@login_manager.login_required
def new_item():
    # 数据库建立数据集信息
    # 把数据导入mongo
    # 返回数据集id，和数据集name
    name = request.json.get('name')
    describe = request.json.get('describe')
    fileId = request.json.get('fileId')
    if not name or not describe or not fileId:
        return jsonify({'code':00000, 'data':data})
    user = g.user
    data_path = name + fileId
    # 数据导入mongo

    # 在数据库建立数据存储信息
    data = Data(name,describe,data_path)
    user.datas.append(data)
    db_session.add(data)
    db_session.commit()
    data = {
        'item_id': data.id
    }
    return jsonify({'code':20000, 'data':data})

