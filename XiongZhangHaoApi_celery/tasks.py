from __future__ import absolute_import, unicode_literals
from .celery import app
import requests

import time
from xiongzhanghao.publicFunc.account import str_encrypt

token = 'a66b1a82b4ba3ca9d444322c8524e844'
user_id = 44
timestamp = str(int(time.time() * 1000))
params = {
    'user_id': user_id,
    'rand_str': str_encrypt(timestamp + token),
    'timestamp': timestamp,
}
print('params----------------> ',params)
# 生成二级域名
@app.task
def specialUserGenerateThePage():
    url = 'http://xiongzhanghao.zhugeyingxiao.com:8003/api/specialUserGenerateThePage'
    print('url -->', url)
    requests.get(url, params=params)


# 提交到熊掌号
@app.task
def celerySubmitXiongZhangHao():
    print('===========================提交到熊掌号===================')
    url = 'http://xiongzhanghao.zhugeyingxiao.com:8003/api/articleScriptOper/submitXiongZhangHao'
    requests.get(url, params=params)


# 初始化覆盖报表
@app.task
def init_fugai_baobiao():
    url = 'http://xiongzhanghao.zhugeyingxiao.com:8003/api/init_fugai_baobiao'
    requests.get(url, params=params)

# 更新覆盖报表详情
@app.task
def update_fugai_baobiao_detail():
    print('======================更新覆盖报表详情=====================')
    url = 'http://xiongzhanghao.zhugeyingxiao.com:8003/api/statisticalReports'
    requests.get(url, params=params)