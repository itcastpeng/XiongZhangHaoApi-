from __future__ import absolute_import, unicode_literals
from .celery import app
import requests, datetime, os, sys






# 获取cookie 以及栏目
@app.task
def celeryGetDebugUser(userLoginId=None):
    # url = '127.0.0.1:8003/getTheDebugUser'
    if userLoginId:
        url = 'http://xiongzhanghao.zhugeyingxiao.com:8003/getTheDebugUser?user_id={}'.format(userLoginId)
    else:
        url = 'http://xiongzhanghao.zhugeyingxiao.com:8003/getTheDebugUser'
    requests.get(url)


# 定时发布文章(5分钟一次)
@app.task
def celeryPublishedArticles():
    url = 'http://xiongzhanghao.zhugeyingxiao.com:8003/script_oper'
    requests.get(url)


