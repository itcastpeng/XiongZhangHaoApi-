from __future__ import absolute_import, unicode_literals
from .celery import app
import requests

import time
from xiongzhanghao.publicFunc.account import str_encrypt

token = '87358e1e762b76cca29de2a14dd2a70f'
user_id = 54
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
    print('==========================生成二级域名===========================')
    timestamp = str(int(time.time() * 1000))
    params = {
        'user_id': user_id,
        'rand_str': str_encrypt(timestamp + token),
        'timestamp': timestamp,
    }
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
    print('================================初始化覆盖报表=============================')
    url = 'http://xiongzhanghao.zhugeyingxiao.com:8003/api/init_fugai_baobiao'
    requests.get(url, params=params)

# 更新覆盖报表详情
@app.task
def update_fugai_baobiao_detail():
    print('======================更新覆盖报表详情=====================')
    url = 'http://xiongzhanghao.zhugeyingxiao.com:8003/api/statisticalReports'
    requests.get(url, params=params)

# 判断文章是否被删除
@app.task
def selectDeleteQuery():
    print('======================判断文章是否被删除=====================')
    url = 'http://xiongzhanghao.zhugeyingxiao.com:8003/api/selectDeleteQuery/judgeToDelete'
    requests.get(url, params=params)


