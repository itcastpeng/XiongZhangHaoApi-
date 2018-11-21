
import requests
import os
if __name__ == '__main__':
    # while True:
    ret = requests.get('http://127.0.0.1:8003/api/script_oper/theScheduler/theScheduler')
    print(ret.url)
    result_data = ret.json()
    print(result_data)
    if result_data.get('data').get('flag'):
        task_id = result_data['data']['task_id']
        if task_id == 1:      # 查询老问答覆盖
            print("--> 获取栏目")
            os.system('chcp 65001 && cd userGetCookieOper && python index.py')


        elif task_id == 2:
            print("--> 发布文章")
            os.system('chcp 65001 && cd publishedArticles && python index.py')


        elif task_id == 3:
            print("--> 判断是否审核")
            # os.system('chcp 65001 && cd select_keywords_cover && python index.py')


        elif task_id == 4:
            print("--> 提交到熊掌号")
            # os.system('chcp 65001 && cd select_keywords_cover && python index.py')


        # elif task_id == 5:
        #     print("--> 生成二级域名")
            # os.system('chcp 65001 && cd select_keywords_cover && python index.py')





    else:
        print('休息---')















