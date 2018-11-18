from xiongzhanghao import models
from xiongzhanghao.publicFunc import Response
from backend.articlePublish import DeDe
from urllib.parse import urlparse
import json, requests, datetime
from django.http import HttpResponse

# Dede 登录
def objLogin(resultData, flag_num):
    website_backstage_url = resultData.get('website_backstage_url').strip()
    url = urlparse(website_backstage_url)
    domain = 'http://' + url.hostname + '/'
    home_path = website_backstage_url.split(domain)[1].replace('/', '')
    # print('domain-------------> ', domain, home_path)
    DeDeObj = DeDe(domain=domain, home_path=home_path)
    if resultData.get('cookies'):
        retDate = DeDeObj.getClassInfo(eval(resultData.get('cookies')))
        models.xzh_userprofile.objects.filter(id=resultData.get('id')).update(
            column_all=json.dumps(retDate),
            is_debug=1
        )
        return resultData.get('cookies'), DeDeObj
    else:
        if flag_num <= 5:
            cookies = DeDeObj.login(resultData.get('website_backstage_username'), resultData.get('website_backstage_password'))
            if len(cookies) > 1:
                # print('cookies----------------> ',cookies)
                retDate = DeDeObj.getClassInfo(cookies)
                # print('retDate=======> ',retDate)
                models.xzh_userprofile.objects.filter(id=resultData.get('id')).update(
                    cookies=cookies,
                    column_all=json.dumps(retDate),
                    is_debug=1
                )
                return cookies, DeDeObj
            else:
                flag_num += 1
                objLogin(resultData, flag_num)
        else:   # 如果登录超过五次 则登录失败
            # print('===========登录失败')
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
                        resultData = {
                            'website_backstage_url':objs.website_backstage_url,
                            'website_backstage_username':objs.website_backstage_username,
                            'website_backstage_password':objs.website_backstage_password,
                            'cookies':objs.cookies,
                            'id':objs.id,
                        }

                        objLogin(resultData, flag_num)
                else:
                    response.code = 200
                    response.msg = '无该用户'
            else:
                # print('=====================')
                objs = models.xzh_userprofile.objects.filter(status=1, is_debug=False)
                for obj in objs:
                    resultData = {
                        'website_backstage_url': obj.website_backstage_url,
                        'website_backstage_username': obj.website_backstage_username,
                        'website_backstage_password': obj.website_backstage_password,
                        'cookies': obj.cookies,
                        'id': obj.id,
                    }
                    if obj.website_backstage == 1:
                        objLogin(resultData, flag_num)
            response.code = 200
            return func(request, *args, **kwargs)
        return inner
    return is_token_decorator


# 定时刷新文章是否审核
def celeryTimedRefreshAudit(request):
    objs = models.xzh_article.objects.filter(article_status=2, is_audit=0, aid__isnull=False)
    for obj in objs:
        website_backstage_url = obj.belongToUser.website_backstage_url.strip()
        indexUrl = website_backstage_url + 'content_list.php?channelid=1'
        if obj.belongToUser.cookies:
            url = urlparse(website_backstage_url)
            domain = 'http://' + url.hostname + '/'
            home_path = website_backstage_url.split(domain)[1].replace('/', '')
            print('indexUrl---------> ',indexUrl)
            DeDeObj = DeDe(domain=domain, home_path=home_path)
            DeDeObj.getArticleAudit(indexUrl, obj.id, obj.aid, eval(obj.belongToUser.cookies))
        else:
            resultData = {
                'website_backstage_url': obj.belongToUser.website_backstage_url,
                'website_backstage_username': obj.belongToUser.website_backstage_username,
                'website_backstage_password': obj.belongToUser.website_backstage_password,
                'cookies': obj.belongToUser.cookies,
                'id': obj.belongToUser_id,
            }
            flag_num = 1
            cookies, DeDeObj= objLogin(resultData, flag_num)
            DeDeObj.getArticleAudit(indexUrl, obj.id, obj.aid, cookies)
    return HttpResponse('--------')








