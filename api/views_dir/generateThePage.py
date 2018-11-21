from xiongzhanghao import models
from xiongzhanghao.publicFunc import Response
from xiongzhanghao.publicFunc import account
from django.http import JsonResponse
from django.shortcuts import render, render_to_response
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from xiongzhanghao.publicFunc.condition_com import conditionCom
from xiongzhanghao.forms.article import AddForm, UpdateForm, SelectForm
import json, datetime, requests, os


# 特殊用户 生成页面
@csrf_exempt
@account.is_token(models.xzh_userprofile)
def specialUserGenerateThePage(request):
    response = Response.ResponseObj()
    objs = models.xzh_article.objects.filter(article_status=6)
    for obj in objs:
        back_url = obj.back_url
        ret = requests.get(back_url)
        encode_ret = ret.apparent_encoding
        if encode_ret == 'GB2312':
            ret.encoding = 'gbk'
        else:
            ret.encoding = 'utf-8'
        domain = obj.belongToUser.secondaryDomainName
        back_url = domain + 'article/{}.html'.format(obj.id)
        obj.back_url = back_url
        obj.DomainNameText = ret.text
        obj.article_status = 4
        obj.save()
    response.code = 200
    response.msg = '生成完成'
    return JsonResponse(response.__dict__)

# 查询二级域名
@csrf_exempt
@account.is_token(models.xzh_userprofile)
def SearchSecondaryDomainName(request, article_id):
    response = Response.ResponseObj()
    print('article_id============> ',article_id)
    objs = models.xzh_article.objects.get(id=article_id)
    if objs:
        return render(request, 'index.html',{
            'my_message':objs.DomainNameText
        })
    else:
        response.code = 301
        response.msg = '无此id'
        return JsonResponse(response.__dict__)











