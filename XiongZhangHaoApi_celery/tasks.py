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

# 定时刷新 粉丝量
@app.task
def queryFollowersNum():
    print('======================定时刷新 粉丝量=====================')
    url = 'http://xiongzhanghao.zhugeyingxiao.com:8003/api/addFansGetTask/queryFollowersNum'
    requests.get(url, params=params)

@app.task
def get_keyword_task():
    print('======================异步获取关键词任务=====================')
    url = 'http://xiongzhanghao.zhugeyingxiao.com:8003/api/SearchSecondary/get_keyword_task/insertTask'
    requests.get(url, params=params)


@app.task
def againInsertTask():
    print('======================定时刷新 判断redis覆盖任务小于二百执行一次=====================')
    url = 'http://xiongzhanghao.zhugeyingxiao.com:8003/api/SearchSecondary/get_keyword_task/againInsertTask'
    requests.get(url, params=params)

@app.task
def baidu_shoulu_situation():
    print('======================定时刷新 百度收录查询保存redis所有用户近七天的文章=====================')
    url = 'http://xiongzhanghao.zhugeyingxiao.com:8003/api/user_statistical/baidu_shoulu_situation'
    requests.get(url, params=params)

@app.task
def user_statistical():
    print('======================定时刷新 所有用户近七天数据=====================')
    url = 'http://xiongzhanghao.zhugeyingxiao.com:8003/api/user_statistical/user_statistical'
    requests.get(url, params=params)
# @app.task
# def export_excel(o_id, start, stop):
#     url = 'http://xiongzhanghao.zhugeyingxiao.com:8003/article/celeryExportExcel/0'
#     data = {
#         'o_id':o_id,
#         'start':start,
#         'stop':stop
#     }
#     requests.post(url, data=data, params=params)