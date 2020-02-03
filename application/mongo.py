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
import csv
from concurrent.futures import ThreadPoolExecutor
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
            csv_path = '/tmp/aidata/'+self.collection_name+'.csv'
            self.col.delete_many({})
            with open(csv_path,'r') as fp:
                reader = csv.DictReader(fp)
                counts = 0
                for each in reader:
                    counts+=1
                    self.col.insert_one(each)
                    print(each)
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
