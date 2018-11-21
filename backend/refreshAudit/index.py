from backend.articlePublish import DeDe
import json, requests, datetime
from urllib.parse import urlparse
from api.public.token import start



def refreshAudit():
    params = start()
    # url = 'http://127.0.0.1:8003/api/script_oper/articleScriptOper/refreshAudit'
    url = 'http://xiongzhanghao.zhugeyingxiao.com:8003/api/script_oper/articleScriptOper/refreshAudit'
    ret = requests.get(url, params=params)
    result = json.loads(ret.text).get('data')
    print('==================', result)
    if result:
        website_backstage_url = result.get('website_backstage_url').strip()
        url = urlparse(website_backstage_url)
        domain = 'http://' + url.hostname + '/'
        home_path = website_backstage_url.split(domain)[1].replace('/', '')

        userid = result.get('website_backstage_username')
        pwd = result.get('website_backstage_password')
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
        # url = 'http://127.0.0.1:8003/api/script_oper/articleScriptOper/refreshAuditModel'
        url = 'http://xiongzhanghao.zhugeyingxiao.com:8003/api/script_oper/articleScriptOper/refreshAuditModel?user_id=44&timestamp=1542788198850&rand_str=86b24054d91240d9559e369296af06cd'
        ret = requests.post(url, data=result_data)

# if __name__ == '__main__':
#     whetherTheAudit()