from backend.articlePublish import DeDe, PcV9
import json, requests, datetime
from urllib.parse import urlparse
from api.public.token import start



def userGetCookieOper():
    params = start()
    # url = 'http://127.0.0.1:8003/api/userGetCookieOper/getTheDebugUser?user_id=17&timestamp=123&rand_str=4297f44b13955235245b2497399d7a93'
    # ret = requests.get(url)
    url = 'http://xiongzhanghao.zhugeyingxiao.com:8003/api/userGetCookieOper/getTheDebugUser'
    ret = requests.get(url, params=params)
    if ret:
        result_data = {}
        print(ret.text)
        result = ret.json().get('data')
        website_backstage = result.get('website_backstage')
        if website_backstage and int(website_backstage) == 1:  # 织梦后台
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
            if website_backstage_url in 'http://www.bjwletyy.com/wladmin':
                retData = [[26, '眼科'], [27, '小儿保健科'], [28, '生长发育科'], [24, '耳鼻喉科'], [22, '小儿内科'], [29, '呼吸哮喘科'], [25, '皮肤科']]  #  该网站固定栏目
            result_data = {
                'cookie':str(cookie),
                'retData':json.dumps(retData),
                'oid':result.get('o_id')
            }

        elif website_backstage and int(website_backstage) == 2: # pcv9后台
            userid = result.get('userid')
            cookie = result.get('cookie')
            pwd = result.get('pwd')
            PcV9Obj = PcV9(userid, pwd, cookie)
            cookies, pc_hash = PcV9Obj.login()
            retData = PcV9Obj.getClassInfo(pc_hash)  # 获取栏目
            result_data = {
                'cookie': str(cookie),
                'retData': json.dumps(retData),
                'oid': result.get('o_id')
            }
        else:
            print('====================获取栏目后台类型错误====================获取栏目后台类型错误==========================获取栏目后台类型错误----------------------获取栏目后台类型错误')

        # url = 'http://127.0.0.1:8003/api/userGetCookieOper/updateModel?user_id=17&timestamp=123&rand_str=4297f44b13955235245b2497399d7a93'
        url = 'http://xiongzhanghao.zhugeyingxiao.com:8003/api/userGetCookieOper/updateModel?user_id=44&timestamp=1542788198850&rand_str=86b24054d91240d9559e369296af06cd'
        ret = requests.post(url, data=result_data)



# if __name__ == '__main__':
#     start()
#























