#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : qiang.hu
# @Time: 2024-10-20

from ComDecorator.ComDeco import getRunTime
import pymongo

class CacheMonHelp():
    def __init__(self):
        self.connect = pymongo.MongoClient(
            'mongodb://127.xx/'
        )
        self.cdb = self.connect['playPythonCache']
        self.usr = self.cdb['user']

    @getRunTime
    def addCache(self,dict):
        oldObj = self.srhCache(dict)
        if not oldObj:
            obj = self.usr.insert_one(dict)
            return obj.inserted_id

    @getRunTime
    def updateCache(self, dict):
        oldObj = self.srhCache( dict )
        if  oldObj:
            obj = self.usr.update_one(id,dict)
            return obj.modified_count

    @getRunTime
    def delCache(self, dict):
        oldObj = self.srhCache( dict )
        if oldObj:
            obj = self.usr.delete_one(dict )
            return obj.deleted_count


    @getRunTime
    def srhCache(self,dict):
        '''查询缓存'''
        obj = self.usr.find(dict)
        if obj:
            for o in obj: return o['_id']

    @getRunTime
    def isExistCache(self,cacheTableName):
        '''查找某个缓存库是否存在'''
        for name in self.cdb.list_collection_names():
            if cacheTableName == name: return True

    def close(self):
        self.connect.close()