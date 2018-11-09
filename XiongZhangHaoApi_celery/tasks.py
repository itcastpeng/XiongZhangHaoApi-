from __future__ import absolute_import, unicode_literals
from .celery import app
import requests, datetime

# 获取cookie 以及栏目
@app.task
def celeryGetDebugUser():
    # url = '127.0.0.1:8003/getTheDebugUser'
    url = 'http://xiongzhanghao.zhugeyingxiao.com:8003/getTheDebugUser'
    requests.get(url)


# 定时发布文章(5分钟一次)
@app.task
def celeryPublishedArticles():
    url = 'http://xiongzhanghao.zhugeyingxiao.com:8003/script_oper'
    requests.get(url)


