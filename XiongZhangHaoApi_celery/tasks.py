from __future__ import absolute_import, unicode_literals
from .celery import app
import requests, datetime, os, sys






# 获取cookie 以及栏目
@app.task
def celeryGetDebugUser(userLoginId=None):
    # url = '127.0.0.1:8003/getTheDebugUser'
    if userLoginId:
        url = 'http://xiongzhanghao.zhugeyingxiao.com:8003/userGetCookieOper/getTheDebugUser?userLoginId={}'.format(userLoginId)
    else:
        url = 'http://xiongzhanghao.zhugeyingxiao.com:8003/userGetCookieOper/getTheDebugUser'
    print('url -->', url)
    requests.get(url)


# 定时发布文章(1分钟一次)
@app.task
def celeryPublishedArticles():
    # url = 'http://127.0.0.1:8003/celeryTimed'
    urlAudit = 'http://xiongzhanghao.zhugeyingxiao.com:8003/script_oper/celeryTimedRefreshAudit'  # 查询审核
    url = 'http://xiongzhanghao.zhugeyingxiao.com:8003/script_oper/sendArticle'
    requests.get(url)
    requests.get(urlAudit)

# 提交到熊掌号
@app.task
def celerySubmitXiongZhangHao():
    url = 'http://xiongzhanghao.zhugeyingxiao.com:8003/script_oper/submitXiongZhangHao'
    requests.get(url)