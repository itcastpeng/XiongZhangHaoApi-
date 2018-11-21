from __future__ import absolute_import, unicode_literals
from .celery import app
import requests, datetime, os, sys

import time
from xiongzhanghao.publicFunc.account import str_encrypt



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


# 初始化覆盖报表
@app.task
def init_fugai_baobiao():
    token = 'a66b1a82b4ba3ca9d444322c8524e844'
    timestamp = str(int(time.time() * 1000))
    user_id = 44
    params = {
        'user_id': user_id,
        'rand_str': str_encrypt(timestamp + token),
        'timestamp': timestamp,
    }
    url = 'http://xiongzhanghao.zhugeyingxiao.com:8003/api/init_fugai_baobiao'
    requests.get(url, params=params)