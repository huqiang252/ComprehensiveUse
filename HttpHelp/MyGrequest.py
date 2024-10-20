#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : qiang.hu
# @Time: 2024-10-20

import gevent.monkey
gevent.monkey.patch_all(thread=False, select=False)  #grequest的猴子补丁

from ComDecorator.ComDeco import getRunTime
import grequests
import time,allure
from Mlogbook import log

@getRunTime
def gRequests(method,url,currentNum=1,**kwargs):
    '''处理并发请求'''
    rs = [grequests.request(method,url,**kwargs) for x in range(currentNum)]
    resp = grequests.map(rs,size=2)

    return resp


@allure.step
def rRequests(method,url,currentNum=1,totalTimes=1,gapTime=0.1,**kwargs):
    '''将并发请求保持多少次，默认0.1秒执行一次并发'''
    list = []
    for x in range(totalTimes):
        resp = gRequests(method,url,currentNum=currentNum,**kwargs)
        # log.info([r.json() for r in resp])  # 打印实际信息
        list.extend(resp)
        time.sleep(gapTime)
    return list
