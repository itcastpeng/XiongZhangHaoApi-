from backend.articlePublish import DeDe
import json, requests, datetime
from urllib.parse import urlparse



def publishedArticles():
    # url = 'http://127.0.0.1:8003/api/script_oper/articleScriptOper/sendArticle'
    url = 'http://xiongzhanghao.zhugeyingxiao.com:8003//api/script_oper/articleScriptOper/sendArticle'
    ret = requests.get(url)
    resultData = json.loads(ret.text).get('data')
    if resultData:
        o_id =  resultData.get('o_id')
        website_backstage_url = resultData.get('website_backstage_url').strip()
        url = urlparse(website_backstage_url)
        domain = 'http://' + url.hostname + '/'
        home_path = website_backstage_url.split(domain)[1].replace('/', '')
        userid = resultData.get('website_backstage_username')
        pwd = resultData.get('website_backstage_password')
        typeid = resultData.get('typeid')
        cookie = ''
        if resultData.get('cookies'):
            cookie = eval(resultData.get('cookies'))
        title = resultData.get('title')
        summary = resultData.get('summary')
        content =  resultData.get('content')
        if 'http://m.chyy120.com/netadmin' in website_backstage_url:
            title =  resultData.get('title').encode('gbk')
            summary =  resultData.get('summary').encode('gbk')
            content =  resultData.get('content').encode('gbk')
        article_data = {
            "channelid": "1",  # 表示普通文章
            "dopost": "save",  # 隐藏写死属性
            "title": str(title),  # 文章标题
            "weight": "1033",  # 权重
            "typeid": typeid,  # 栏目id
            "autokey": "1",  # 关键字自动获取
            "description": str(summary),  # 描述
            "remote": "1",  # 下载远程图片和资源
            "autolitpic": "1",  # 提取第一个图片为缩略图
            "sptype": "hand",  # 分页方式 手动
            "spsize": "5",
            "body": str(content),
            "notpost": "0",
            "click": "63",
            "sortup": "0",
            "arcrank": "0",
            "money": "0",
            "pubdate": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "ishtml": 1,
            "imageField.x": "30",
            "imageField.y": "12"
        }
        DeDeObj = DeDe(domain, home_path, userid, pwd, cookie)
        cookie = DeDeObj.login()
        resultData = DeDeObj.sendArticle(article_data, article_data.get('title'))
        result_data = {
            'resultData': str(resultData),
            'o_id': o_id
        }
        print(result_data)
        # url = 'http://127.0.0.1:8003/api/script_oper/articleScriptOper/models_article'
        url = 'http://xiongzhanghao.zhugeyingxiao.com:8003//api/script_oper/articleScriptOper/models_article'
        requests.post(url, data=result_data)


# if __name__ == '__main__':
#     publishedArticles()



