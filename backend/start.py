from backend.userGetCookieOper import index as userGetCookieOper
from backend.publishedArticles import index as publishedArticles
from backend.refreshAudit import index as refreshAudit
from backend.selectDeleteQuery import index as selectDeleteQuery

import requests
import os
from time import sleep
if __name__ == '__main__':
    while True:
        try:
            print('===================*************************===================================')
            # ret = requests.get('http://127.0.0.1:8003/api/theScheduler/theScheduler')
            ret = requests.get('http://xiongzhanghao.zhugeyingxiao.com:8003/api/theScheduler/theScheduler')
            result_data = ret.json()
            print('result_data--> ',result_data)
            if ret and result_data.get('data').get('flag'):
                task_id = result_data['data']['task_id']
                if task_id == 1:      # 查询老问答覆盖
                    print("--> 获取栏目")
                    userGetCookieOper.userGetCookieOper()

                elif task_id == 2:
                    print("-> 发布文章")
                    publishedArticles.publishedArticles()

                elif task_id == 3:
                    print("--> 判断是否审核")
                    refreshAudit.refreshAudit()

                elif task_id == 4:
                    print("--> 爬取客户后台 判断文章是否删除")
                    selectDeleteQuery.electDeleteQuery()
            else:
                print('=================休息5分钟')
                sleep(300)
        except Exception:
            continue















