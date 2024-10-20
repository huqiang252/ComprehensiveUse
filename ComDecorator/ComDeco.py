#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : qiang.hu
# @Time: 2024-10-20


import time
from Mlogbook import log
import allure


def getRunTime(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        response = func( *args, **kwargs)
        end_time = time.time()
        log.info([end_time - start_time, args, kwargs, response])
        return response

    return wrapper


def chkRespStatus(status_code=200):
    '''检查返回的状态码，默认200，接受gRequests返回的list对象中的结果'''

    def chkRsp_func(func):
        def wrapper(*args, **kwargs):
            responses = func(*args, **kwargs)
            if type(responses) == type([]):
                OK = [True for res in responses if res.status_code == status_code]
                log.info([args, [res.status_code for res in responses], kwargs])
                if (len(responses) == len(OK)):
                    log.info([args, 'return True'])
                    return (True, responses)
                log.info([args, 'return False'])
                return (False,responses)

        return wrapper
    return chkRsp_func
