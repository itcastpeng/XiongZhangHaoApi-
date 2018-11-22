from xiongzhanghao import models
from xiongzhanghao.publicFunc import Response
from django.http import JsonResponse
from api.public.token import start
from urllib.parse import urlparse
from backend.articlePublish import DeDe


# 判断客户页面 该文章是否删除
def deleteQuery(request):
    params = start()  # 获取token
    response = Response.ResponseObj()
    objs = models.xzh_article.objects.filter(article_status__in=[2, 4, 5])
    for obj in objs:
        website_backstage_url = obj.user.website_backstage_url
        url = urlparse(website_backstage_url)
        if url.hostname:
            domain = 'http://' + url.hostname + '/'
            home_path = website_backstage_url.split(domain)[1].replace('/', '')
        else:
            domain = 'http://' + website_backstage_url.split('/')[0] + '/'
            home_path = website_backstage_url.split('/')[1]

        cookie = ''
        if obj.user.cookies:
            cookie = eval(obj.user.cookies)
        userid = obj.user.website_backstage_username
        pwd = obj.user.website_backstage_password

        print('home_path--------------->? ', domain, home_path, userid, pwd, cookie)
        DeDeObj = DeDe(domain, home_path, userid, pwd, cookie)
        cookie = DeDeObj.login()


    return JsonResponse(response.__dict__)
















