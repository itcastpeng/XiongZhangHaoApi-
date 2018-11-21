
from django.shortcuts import render, HttpResponse
from xiongzhanghao import models
from xiongzhanghao.publicFunc import Response
from xiongzhanghao.publicFunc import account
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from xiongzhanghao.publicFunc.condition_com import conditionCom
from xiongzhanghao.forms.user import AddForm, UpdateForm, SelectForm, AdminAddForm, AdminUpdateForm
from django.db.models import Q
from backend.articlePublish import DeDe
from urllib.parse import urlparse
import json, requests, datetime


# @csrf_exempt
# def userGetCookieOper(request, oper_type):
#     response = Response.ResponseObj()
#     # 进行获取cookie 和 栏目
#     if oper_type == 'getTheDebugUser':
#         userObjs = models.xzh_userprofile.objects
#         objs = userObjs.filter(status=1, is_debug=False)
#         for obj in objs:
#             if obj.website_backstage == 1:
#                 website_backstage_url = obj.website_backstage_url.strip()
#                 url = urlparse(website_backstage_url)
#                 if url.hostname:
#                     domain = 'http://' + url.hostname + '/'
#                     home_path = website_backstage_url.split(domain)[1].replace('/', '')
#                 else:
#                     domain = 'http://' + website_backstage_url.split('/')[0] + '/'
#                     home_path = website_backstage_url.split('/')[1]
#                 print('home_path--------------->? ',domain, home_path)
#                 userid = obj.website_backstage_username
#                 pwd = obj.website_backstage_password
#                 cookie = ''
#                 if obj.cookies:
#                     cookie = eval(obj.cookies)
#                 DeDeObj = DeDe(domain, home_path,  userid, pwd, cookie)
#                 cookie = DeDeObj.login()
#                 retData = DeDeObj.getClassInfo()
#                 models.xzh_userprofile.objects.filter(id=obj.id).update(
#                     column_all=json.dumps(retData),
#                     is_debug=1,
#                     cookies=cookie
#                 )
#         response.code = 200
#     else:
#         response.code = 402
#         response.msg = '请求失败'
#
#     return JsonResponse(response.__dict__)


@csrf_exempt
@account.is_token(models.xzh_userprofile)
def userGetCookieOper(request, oper_type):
    response = Response.ResponseObj()
    # 进行获取cookie 和 栏目
    if oper_type == 'getTheDebugUser':
        print('=======================进行获取cookie 和 栏目============================')
        objs = models.xzh_userprofile.objects.filter(is_debug=False, role_id=61).order_by('create_date')
        if objs:
            obj = objs[0]
            if obj.website_backstage == 1:
                website_backstage_url = obj.website_backstage_url.strip()
                userid = obj.website_backstage_username
                pwd = obj.website_backstage_password
                cookie = ''
                if obj.cookies:
                    cookie = eval(obj.cookies)
                response.data = {
                    'website_backstage_url':website_backstage_url,
                    'userid':userid,
                    'pwd':pwd,
                    'cookie':cookie,
                    'o_id':obj.id
                }
        response.msg = '查询成功'
        response.code = 200

    elif oper_type == 'updateModel':
        print('==============================登录cookie 与栏目 写入数据===============================')
        oid = request.POST.get('oid')
        retData = request.POST.get('retData')
        cookie = request.POST.get('cookie')
        print('cookie------cookie-------->',cookie)
        models.xzh_userprofile.objects.filter(id=oid).update(
            column_all=json.dumps(retData),
            is_debug=1,
            cookies=cookie
        )
        response.code = 200
    else:
        response.code = 402
        response.msg = '请求失败'

    return JsonResponse(response.__dict__)