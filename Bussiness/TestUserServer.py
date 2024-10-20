#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : qiang.hu
# @Time: 2024-10-20

from HttpHelp.MyGrequest import rRequests
from DBHelp.DBMysql import DBMysql
from CacheHelp.CachMongo import CacheMonHelp
from ComDecorator.ComDeco import chkRespStatus
from Tools.PwdManage import Md5Help as Md5
from conf import HOST
import pytest,allure


@chkRespStatus()
@allure.step
def r_login(username,password):
    '''请求业务的处理'''
    response = rRequests('POST',f'{HOST}/login',json={"userName":username,"passWord":password})
    return response


@chkRespStatus()
@allure.step
def r_register(username,password):
    response = rRequests( 'POST', f'{HOST}/user/register', json={"userName": username, "passWord": password} )
    return response


@allure.step
def chk_exitDB(username):
    '''去数据库进行检查'''
    results = DBMysql().selectData(f"SELECT * FROM user t WHERE t.username='{username}' ")
    return results


@allure.step
def chk_exitCacheMon(username):
    '''去缓存检查'''
    return CacheMonHelp().srhCache({'username':username})


@pytest.mark.parametrize('username,password',[
    pytest.param('qwensf','12345',id=u'不存在的用户名和密码登录'),
    pytest.param('13713762959','tony137',id=u'存在的用户名和密码登录')
]
)
def test_login(username,password):
    resp = r_login(username,password)
    assert resp[0]==True
    # for r in chk_exitDB(username):
    #     assert r['username']==username
    # assert chk_exitCacheMon(username)!=None


@pytest.mark.parametrize( 'username,password', [
    pytest.param( 'qwen', '12345', id=u'注册成功' ),
    pytest.param( '13713762959', 'tony137', id=u'存在的用户名和密码登录,注册失败' )
]
)
def test_register(username, password):
    resp = r_register( username, password )
    assert resp[0] == True
    for r in chk_exitDB( username ):
        assert r['username'] == username
    assert chk_exitCacheMon( username ) != None
