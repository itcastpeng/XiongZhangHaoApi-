from backend.articlePublish import DeDe
import json, requests, datetime
from urllib.parse import urlparse
from api.public.token import start



def userGetCookieOper():
    params = start()
    # url = 'http://127.0.0.1:8003/api/userGetCookieOper/getTheDebugUser?user_id=17&timestamp=123&rand_str=4297f44b13955235245b2497399d7a93'
    url = 'http://xiongzhanghao.zhugeyingxiao.com:8003/api/userGetCookieOper/getTheDebugUser'
    ret = requests.get(url, params=params)
    if ret:
        print(ret.text)
        result = ret.json().get('data')
        website_backstage_url = result.get('website_backstage_url')
        url = urlparse(website_backstage_url)
        if url.hostname:
            domain = 'http://' + url.hostname + '/'
            home_path = website_backstage_url.split(domain)[1].replace('/', '')
        else:
            domain = 'http://' + website_backstage_url.split('/')[0] + '/'
            home_path = website_backstage_url.split('/')[1]
        userid = result.get('userid')
        cookie = result.get('cookie')
        pwd = result.get('pwd')
        print('home_path--------------->? ', domain, home_path, userid, pwd, cookie)
        DeDeObj = DeDe(domain, home_path, userid, pwd, cookie)
        cookie = DeDeObj.login()
        retData = DeDeObj.getClassInfo()
        print("result.get('o_id'=====================> ",result.get('o_id'))
        result_data = {
            'cookie':str(cookie),
            'retData':json.dumps(retData),
            'oid':result.get('o_id')
        }
        # url = 'http://127.0.0.1:8003/api/userGetCookieOper/updateModel?user_id=17&timestamp=123&rand_str=4297f44b13955235245b2497399d7a93'
        url = 'http://xiongzhanghao.zhugeyingxiao.com:8003/api/userGetCookieOper/updateModel?user_id=44&timestamp=1542788198850&rand_str=86b24054d91240d9559e369296af06cd'
        ret = requests.post(url, data=result_data)

# if __name__ == '__main__':
#     start()
#























