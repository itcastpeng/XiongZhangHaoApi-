from backend.userGetCookieOper import index as userGetCookieOper
from backend.publishedArticles import index as publishedArticles
from backend.refreshAudit import index as refreshAudit
import requests
import os
from time import sleep
if __name__ == '__main__':
    while True:
        ret = requests.get('http://127.0.0.1:8003/api/script_oper/theScheduler/theScheduler')
        print(ret.url)
        result_data = ret.json()
        print(result_data)
        if result_data.get('data').get('flag'):
            task_id = result_data['data']['task_id']
            if task_id == 1:      # 查询老问答覆盖
                print("--> 获取栏目")
                userGetCookieOper.userGetCookieOper()

            elif task_id == 2:
                print("--> 发布文章")
                publishedArticles.publishedArticles()

            elif task_id == 3:
                print("--> 判断是否审核")
                refreshAudit.refreshAudit()

            # elif task_id == 4:
            #     print("--> 提交到熊掌号")
                # os.system('chcp 65001 && cd select_keywords_cover && python index.py')


        else:
            print('=================休息5分钟')
            sleep(300)















