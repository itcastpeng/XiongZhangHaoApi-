from xiongzhanghao.publicFunc import Response
from django.http import JsonResponse, HttpResponse
from api.public.token import start
from urllib.parse import urlparse
from backend.articlePublish import DeDe, PcV9
import requests, json



# 客户页面爬取数据 存入数据库 判断文章是否删除
def electDeleteQuery():
    params = start()  # 获取token
    response = Response.ResponseObj()
    # url = 'http://127.0.0.1:8003/api/selectDeleteQuery/deleteQuery?user_id=17&timestamp=123&rand_str=4297f44b13955235245b2497399d7a93'
    # ret = requests.get(url)
    url = 'http://xiongzhanghao.zhugeyingxiao.com:8003/api/selectDeleteQuery/deleteQuery'
    ret = requests.get(url, params=params)
    if ret:
        print('ret.text=================> ',ret.text)
        result = json.loads(ret.text).get('data')
        website_backstage = result.get('website_backstage')
        userid = result.get('website_backstage_username')
        pwd = result.get('website_backstage_password')
        maxtime = result.get('maxtime')
        column_all = result.get('column_all')
        cookie = ''
        if result.get('cookie'):
            cookie = eval(result.get('cookie'))
        o_id = result.get('o_id')
        print('website_backstage=============> ',website_backstage)
        if int(website_backstage) == 1:           # 织梦后台
            website_backstage_url = result.get('website_backstage_url')
            if website_backstage_url:
                url = urlparse(website_backstage_url)
                if url.hostname:
                    domain = 'http://' + url.hostname + '/'
                    home_path = website_backstage_url.split(domain)[1].replace('/', '')
                else:
                    domain = 'http://' + website_backstage_url.split('/')[0] + '/'
                    home_path = website_backstage_url.split('/')[1]
                print('===============================> ',o_id)
                # print('home_path--------------->? ', domain, home_path, userid, pwd, cookie)
                DeDeObj = DeDe(domain, home_path, userid, pwd, cookie)
                cookie = DeDeObj.login()
                if website_backstage_url[-1] == '/':
                    website_backstage_url = website_backstage_url + 'content_list.php?channelid=1'
                else:
                    website_backstage_url = website_backstage_url + '/content_list.php?channelid=1'

                if 'http' not in website_backstage_url:
                    website_backstage_url = 'http://' + website_backstage_url
                page = 0
                flag, yema, data_list = DeDeObj.deleteQuery(website_backstage_url + '&pageno={}'.format(1), maxtime)
                result_data = []
                print('查询中.........', maxtime)
                while True:
                    try:
                        page +=1
                        flag, yema, data_list = DeDeObj.deleteQuery(website_backstage_url + '&pageno={}'.format(page), maxtime)
                        if data_list:
                            for i in data_list:
                                if i not in result_data:
                                    # print('i====> ',i)
                                    result_data.append(i)
                            # print('flag=========================> ',yema, flag, page, data_list)

                        if page >= int(yema) + 1:
                            break
                        if int(flag) == 1:
                            break
                    except Exception:
                        continue
                data = {
                    'result_data':str(result_data),
                    'o_id':o_id
                }
                print('data================================> ', data)
                # url = 'http://127.0.0.1:8003/api/selectDeleteQuery/deleteQueryModel?user_id=17&timestamp=123&rand_str=4297f44b13955235245b2497399d7a93'
                url = 'http://xiongzhanghao.zhugeyingxiao.com:8003/api/selectDeleteQuery/deleteQueryModel?user_id=44&timestamp=1542788198850&rand_str=86b24054d91240d9559e369296af06cd'
                requests.post(url, data=data)

        elif int(website_backstage) == 2:    # PcV9后台
            PcV9Obj = PcV9(userid, pwd, cookie)
            cookies, pc_hash = PcV9Obj.login()
            result_list = []
            for i in column_all:
                data_list = []
                url = 'http://m.evercarebj.com/index.php?m=content&c=content&a=init&menuid=822&catid={catid}&pc_hash={pc_hash}'.format(
                    catid=i[0], pc_hash=pc_hash)
                data_list = PcV9Obj.deleteQuery(url, data_list, maxtime)
                for data in data_list:
                    if data:
                        result_list.append(data)
            data = {
                'result_data': str(result_list),
                'o_id': o_id
            }

            # url = 'http://127.0.0.1:8003/api/selectDeleteQuery/deleteQueryModel?user_id=17&timestamp=123&rand_str=4297f44b13955235245b2497399d7a93'
            url = 'http://xiongzhanghao.zhugeyingxiao.com:8003/api/selectDeleteQuery/deleteQueryModel?user_id=44&timestamp=1542788198850&rand_str=86b24054d91240d9559e369296af06cd'
            requests.post(url, data=data)





