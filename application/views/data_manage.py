#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2020 frey <summeriwiner@gmail.com>
#
# Distributed under terms of the MIT license.

"""

"""
from flask import Blueprint, request, jsonify, g, abort
from ..models import Data
from ..database import db_session
from .. import login_manager
from ..mongo import Mongodb

data_manage = Blueprint('data_manage',__name__)


@data_manage.route('/items')
@login_manager.login_required
def get_items():
    # 获取所有数据
    data = { 'items': []}
    for item in g.user.datas:
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
    # 数据导入mongo
    col = Mongodb(fileId)
    col.addCollection()
    # 在数据库建立数据存储信息
    data = Data(name,describe,fileId)
    g.user.datas.append(data)
    db_session.add(data)
    db_session.commit()
    return jsonify({'code':20000, 'data':{'item_id': data.id}})

@data_manage.route('/item',methods=['DELETE'])
@login_manager.login_required
def del_item():
    item_id = request.json.get('id')
    # 判断请求参数
    item = Data.query.filter_by(id=item_id).first()
    g.user.datas.remove(item)
    db_session.commit()
    return jsonify({ 'code':20000, 'message': '删除成功' })

@data_manage.route('/item',methods=['GET'])
@login_manager.login_required
def get_item():
    # 检查传入参数
    item_id = request.args.get('id')
    if item_id is None:
        abort(400)
    item = Data.query.filter_by(id=int(item_id)).first()
    # 从mongo查询数据
    col = Mongodb(item.data_path)
    items = col.getCollection()
    data = {
        'items': items
    }
    return jsonify({ 'code':20000, 'data':data })

@data_manage.route('/item/row',methods=['DELETE'])
@login_manager.login_required
def del_item_row():
    item_id = request.json.get('item_id')
    row_id = request.json.get('row_id')
    if item_id is None or row_id is None:
        abort(400)
    item = Data.query.filter_by(id=int(item_id)).first()
    col = Mongodb(item.data_path)
    col.delRow(row_id)
    return jsonify({ 'code':20000, 'message':"success" })


@data_manage.route('/item/row',methods=['PUT'])
@login_manager.login_required
def update_item_row():
    item_id = request.json.get('item_id')
    row = request.json.get('row')
    if item_id is None or row is None:
        abort(400)
    item = Data.query.filter_by(id=int(item_id)).first()
    col = Mongodb(item.data_path)
    col.updateRow(row)
    return jsonify({ 'code':20000, 'message':"success" })