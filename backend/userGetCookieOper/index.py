from backend.articlePublish import DeDe
import json, requests, datetime
from urllib.parse import urlparse




def userGetCookieOper():
    # url = 'http://127.0.0.1:8003/api/userGetCookieOper/getTheDebugUser?user_id=44&timestamp=123&rand_str=a66b1a82b4ba3ca9d444322c8524e844'
    url = 'http://xiongzhanghao.zhugeyingxiao.com:8003//api/userGetCookieOper/getTheDebugUser?user_id=44&timestamp=123&rand_str=a66b1a82b4ba3ca9d444322c8524e844'
    ret = requests.get(url)
    result = ret.json().get('data')
    if result:
        website_backstage_url = result.get('website_backstage_url')
        url = urlparse(website_backstage_url)
        if url.hostname:
            domain = 'http://' + url.hostname + '/'
            home_path = website_backstage_url.split(domain)[1].replace('/', '')
        else:
            domain = 'http://' + website_backstage_url.split('/')[0] + '/'
            home_path = website_backstage_url.split('/')[1]
        print('home_path--------------->? ', domain, home_path)
        userid = result.get('userid')
        cookie = result.get('cookie')
        pwd = result.get('pwd')
        DeDeObj = DeDe(domain, home_path, userid, pwd, cookie)
        cookie = DeDeObj.login()
        retData = DeDeObj.getClassInfo()
        print('===========================> ',cookie)
        result_data = {
            'cookie':str(cookie),
            'retData':retData,
            'oid':result.get('o_id')
        }
        # url = 'http://127.0.0.1:8003/api/userGetCookieOper/updateModel'
        url = 'http://xiongzhanghao.zhugeyingxiao.com:8003//api/userGetCookieOper/updateModel?user_id=44&timestamp=123&rand_str=a66b1a82b4ba3ca9d444322c8524e844'
        ret = requests.post(url, data=result_data)

# if __name__ == '__main__':
#     start()
#























