from xiongzhanghao import models
from xiongzhanghao.publicFunc import Response
from backend.articlePublish import DeDe
from urllib.parse import urlparse
import json, requests, datetime

# Dede 登录
def objLogin(obj, flag_num):
    website_backstage_url = obj.website_backstage_url.strip()
    url = urlparse(website_backstage_url)
    domain = 'http://' + url.hostname + '/'
    home_path = website_backstage_url.split(domain)[1].replace('/', '')
    print('domain-------------> ', domain, home_path)
    DeDeObj = DeDe(domain=domain, home_path=home_path)
    if flag_num <= 5:
        cookies = DeDeObj.login(obj.website_backstage_username, obj.website_backstage_password)
        if len(cookies) > 1:
            print('cookies----------------> ',cookies)
            retDate = DeDeObj.getClassInfo(cookies)
            print('retDate=======> ',retDate)
            models.xzh_userprofile.objects.filter(id=obj.id).update(
                cookies=cookies,
                column_all=json.dumps(retDate)
            )
        else:
            flag_num += 1
            objLogin(obj, flag_num)
    else:   # 如果登录超过五次 则登录失败
        print('===========登录失败')
        return 500


# 获取cookie 和 登录
def getCookies(userObj):
    def is_token_decorator(func):
        def inner(request, *args, **kwargs):
            userLoginId = request.GET.get('userLoginId')
            response = Response.ResponseObj()
            print('userLoginId========>', userLoginId)
            flag_num = 1
            if userLoginId:
                objs = models.xzh_userprofile.objects.get(id=userLoginId)
                if objs:
                    if objs.website_backstage == 1:
                        objLogin(objs, flag_num)
                else:
                    response.code = 200
                    response.msg = '无该用户'
            else:
                objs = models.xzh_userprofile.objects.filter(status=1, is_debug=0)
                for obj in objs:
                    if obj.website_backstage == 1:
                        objLogin(obj, flag_num)
                response.code = 200
            return func(request, *args, **kwargs)
        return inner
    return is_token_decorator



# 查看发布的文章 是否审核通过
def getWhetherApproved(request):
    response = Response.ResponseObj()
    objs = models.xzh_article.objects.filter(article_status=2, is_audit=False)
    for obj in objs:
        pass





