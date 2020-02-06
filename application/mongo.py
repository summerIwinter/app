#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2020 frey <summeriwiner@gmail.com>
#
# Distributed under terms of the MIT license.

"""

"""
from pymongo import MongoClient 
from bson import ObjectId
import csv
from concurrent.futures import ThreadPoolExecutor
from . import app
class Mongodb:
    client = MongoClient('localhost', 27017)
    db = client['aidata']
    executor = ThreadPoolExecutor(2)
    def __init__(self,collection_name):
        self.collection_name = collection_name
        self.col = Mongodb.db[collection_name]

    def addCollection(self):
        # 从csv文件导入数据
        def _addCollection():
            csv_path = app.config["FILE_UPDATE_PATH"]+self.collection_name+'.csv'
            self.col.delete_many({})
            with open(csv_path,'r') as fp:
                reader = csv.DictReader(fp)
                counts = 0
                for each in reader:
                    counts+=1
                    self.col.insert_one(each)
                return counts
        # _addCollection()
        Mongodb.executor.submit(_addCollection)

    def getCollection(self,skip=0,limit=50):
        # 查询数据
        data = []
        for d in self.col.find().skip(0).limit(50):
            d['_id'] = str(d['_id'])
            data.append(d)
        return data

    def delRow(self,_id):
        print(_id)
        print("删除一条数据")
        pass
    
    def updateRow(self,row):
        _id = ObjectId(row.pop('_id'))
        
        self.col.update_one({'_id':_id},{'$set':row})