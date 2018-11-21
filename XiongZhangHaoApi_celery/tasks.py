from __future__ import absolute_import, unicode_literals
from .celery import app
import requests, datetime, os, sys






# 生成二级域名
@app.task
def celeryGetDebugUser():
    url = 'http://xiongzhanghao.zhugeyingxiao.com:8003/api/specialUserGenerateThePage'
    print('url -->', url)
    requests.get(url)


# 定时发布文章(1分钟一次)
# @app.task
# def celeryPublishedArticles():
#     # url = 'http://127.0.0.1:8003/celeryTimed'
#     urlAudit = 'http://xiongzhanghao.zhugeyingxiao.com:8003/articleScriptOper/celeryTimedRefreshAudit'  # 查询审核
#     url = 'http://xiongzhanghao.zhugeyingxiao.com:8003/articleScriptOper/sendArticle'
#     requests.get(url)
#     requests.get(urlAudit)

# 提交到熊掌号
# @app.task
# def celerySubmitXiongZhangHao():
#     url = 'http://xiongzhanghao.zhugeyingxiao.com:8003/articleScriptOper/submitXiongZhangHao'
#     requests.get(url)