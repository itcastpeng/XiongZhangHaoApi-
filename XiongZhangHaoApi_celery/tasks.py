from __future__ import absolute_import, unicode_literals
from .celery import app
import requests, datetime, os, sys






# 生成二级域名
@app.task
def specialUserGenerateThePage():
    url = 'http://xiongzhanghao.zhugeyingxiao.com:8003/api/specialUserGenerateThePage'
    print('url -->', url)
    requests.get(url)


# 提交到熊掌号
@app.task
def celerySubmitXiongZhangHao():
    url = 'http://xiongzhanghao.zhugeyingxiao.com:8003/api/script_oper/articleScriptOper/submitXiongZhangHao'
    requests.get(url)