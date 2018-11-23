from backend.articlePublish import DeDe
import json, requests, datetime
from urllib.parse import urlparse
from api.public.token import start


# 判断是否审核
def refreshAudit():
    params = start()
    print(params)
    # url = 'http://127.0.0.1:8003/api/articleScriptOper/refreshAudit?user_id=17&timestamp=123&rand_str=4297f44b13955235245b2497399d7a93'
    url = 'http://xiongzhanghao.zhugeyingxiao.com:8003/api/articleScriptOper/refreshAudit'
    ret = requests.get(url, params=params)
    result = json.loads(ret.text).get('data')
    print('==================', result)
    if result:
        website_backstage_url = result.get('website_backstage_url').strip()
        if 'http' in website_backstage_url:
            url = urlparse(website_backstage_url)
            domain = 'http://' + url.hostname + '/'
            home_path = website_backstage_url.split(domain)[1].replace('/', '')
        else:
            web_url = website_backstage_url.split('/')[0] + '/'
            domain = 'http://' + web_url
            home_path = website_backstage_url.split(web_url)[1].replace('/', '')

        userid = result.get('website_backstage_username')
        pwd = result.get('website_backstage_password')
        if website_backstage_url[-1] != '/':
            website_backstage_url = website_backstage_url + '/'
        if 'http' not in website_backstage_url:
            website_backstage_url = 'http://' + website_backstage_url
        indexUrl = website_backstage_url + 'content_list.php?channelid=1'
        o_id = result.get('o_id')
        aid = result.get('aid')
        userType = result.get('userType')
        cookie = ''
        if result.get('cookies'):
            cookie = eval(result.get('cookies'))
        DeDeObj = DeDe(domain, home_path, userid, pwd, cookie)
        cookies = DeDeObj.login()
        o_id, status = DeDeObj.getArticleAudit(indexUrl, o_id, aid)
        result_data = {
            'o_id': o_id,
            'status': status,
            'userType': userType
        }
        print('vresult_data--00000000000000------------000000000--------> ',result_data)
        # url = 'http://127.0.0.1:8003/api/articleScriptOper/refreshAuditModel?user_id=17&timestamp=123&rand_str=4297f44b13955235245b2497399d7a93'
        url = 'http://xiongzhanghao.zhugeyingxiao.com:8003/api/articleScriptOper/refreshAuditModel?user_id=44&timestamp=1542788198850&rand_str=86b24054d91240d9559e369296af06cd'
        ret = requests.post(url, data=result_data)

# if __name__ == '__main__':
#     whetherTheAudit()