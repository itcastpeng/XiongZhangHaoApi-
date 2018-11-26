from backend.articlePublish import DeDe
import json, requests, datetime
from urllib.parse import urlparse
from api.public.token import start
from random import randint
# 发布文章
def publishedArticles():
    params = start()
    # url = 'http://127.0.0.1:8003/api/articleScriptOper/sendArticle?user_id=17&timestamp=123&rand_str=4297f44b13955235245b2497399d7a93'
    # ret = requests.get(url)
    url = 'http://xiongzhanghao.zhugeyingxiao.com:8003/api/articleScriptOper/sendArticle'
    ret = requests.get(url, params=params)
    # print('=ret.text=========> ',ret.text)
    resultData = json.loads(ret.text).get('data')
    if resultData:
        o_id =  resultData.get('o_id')
        website_backstage_url = resultData.get('website_backstage_url').strip()
        print('====================================website_backstage_url', website_backstage_url)
        if 'http' in website_backstage_url:
            url = urlparse(website_backstage_url)
            domain = 'http://' + url.hostname + '/'
            home_path = website_backstage_url.split(domain)[1].replace('/', '')
        else:
            web_url =  website_backstage_url.split('/')[0] + '/'
            domain = 'http://' + web_url
            home_path = website_backstage_url.split(web_url)[1].replace('/', '')
        userid = resultData.get('website_backstage_username')
        pwd = resultData.get('website_backstage_password')
        typeid = resultData.get('typeid')
        cookie = ''
        if resultData.get('cookies'):
            cookie = eval(resultData.get('cookies'))
        title = resultData.get('title')
        picname = resultData.get('picname')
        summary = resultData.get('summary')
        content =  resultData.get('content')
        print('00000000000000000000000000website_backstage_url00000000000000000000000>',website_backstage_url)
        if 'http://m.chyy120.com/netadmin' in website_backstage_url or 'http://wap.tysgmr.com/dede' in website_backstage_url or 'http://m.oy120.com/@qz120_@' in website_backstage_url:  # 判断utf8 还是 gbk
            print('------==========----------------------GBK')
            title =  resultData.get('title').encode('gbk')
            summary =  resultData.get('summary').encode('gbk')
            content =  resultData.get('content').encode('gbk')

        article_data = {
            "channelid": "1",  # 表示普通文章
            "dopost": "save",  # 隐藏写死属性
            "title": title,  # 文章标题
            "weight": "1033",  # 权重
            "typeid": typeid,  # 栏目id
            "autokey": "1",  # 关键字自动获取
            "description": summary,  # 描述
            "remote": "1",  # 下载远程图片和资源
            "autolitpic": "1",  # 提取第一个图片为缩略图
            "sptype": "hand",  # 分页方式 手动
            "spsize": "5",
            "body": content,
            "notpost": "0",
            "click": randint(100, 200),
            "sortup": "0",
            "arcrank": "0",
            "money": "0",
            "pubdate": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "ishtml": 1,
            "imageField.x": "30",
            "imageField.y": "12"
        }
        article_data['picname'] = ''   # 缩略图
        if picname:
            article_data['picname'] = picname
        if 'http://m.oy120.com/@qz120_@' in website_backstage_url:
            article_data['litpic'] = '(binary)'
            article_data['color'] = ''
            article_data['keywords'] = ''
            article_data['filename'] = ''
            article_data['redirecturl'] = ''
            article_data['voteid'] = ''
            article_data['redirecturl'] = ''
            article_data['tags'] = ''
            article_data['shorttitle'] = ''
        print('domain, home_path, userid, pwd, cookie-----------------> ',domain, home_path, userid, pwd, cookie)
        DeDeObj = DeDe(domain, home_path, userid, pwd, cookie)
        cookie = DeDeObj.login()
        print("===============-----9999999999999999999999999999999999900-----------> ",resultData.get('title'))
        resultData = DeDeObj.sendArticle(article_data, resultData.get('title'))

        result_data = {
            'resultData': json.dumps(resultData),
            'o_id': o_id
        }
        print('result_data==============================> ',resultData)
        # url = 'http://127.0.0.1:8003/api/articleScriptOper/sendArticleModels?user_id=17&timestamp=123&rand_str=4297f44b13955235245b2497399d7a93'
        url = 'http://xiongzhanghao.zhugeyingxiao.com:8003/api/articleScriptOper/sendArticleModels?user_id=44&timestamp=1542788198850&rand_str=86b24054d91240d9559e369296af06cd'
        # print('==============url.> ',url)
        requests.post(url, data=result_data)


# if __name__ == '__main__':
#     publishedArticles()



