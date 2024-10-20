#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : qiang.hu
# @Time: 2024-10-20

from ComDecorator.ComDeco import getRunTime
import pymysql.cursors

class DBMysql():
    def __init__(self):
        self.connect = pymysql.connect( host='192.168.1.100',
                                        port=3306,
                                        user='root',
                                        password='123456',
                                        database='playpython',
                                        cursorclass=pymysql.cursors.DictCursor )


    @getRunTime
    def selectData(self,sqlCommand,args=None):
        '''执行sql语句进行查询'''
        with self.connect.cursor() as cursor:
            cursor.execute(sqlCommand,args=args)
            result = cursor.fetchall()
            return result


    @getRunTime
    def insertData(self,sqlCommand,args=None):
        '''获取更新，插入的id'''
        with self.connect.cursor() as cursor:
            try:
                cursor.execute(sqlCommand,args=args)
                result = cursor.lastrowid()
                self.connect.commit()
                return result
            except:
                self.connect.rollback()
            finally:
                self.close()

    @getRunTime
    def updateData(self,sqlCommand,args=None):
        with self.connect.cursor() as cursor:
            try:
                cursor.execute(sqlCommand,args=args)
                result = cursor.rowcount
                self.connect.commit()
                return result
            except:
                self.connect.rollback()
            finally:
                self.close()

    def close(self):
        self.connect.close()







