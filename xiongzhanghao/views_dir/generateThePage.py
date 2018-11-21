from xiongzhanghao import models
from xiongzhanghao.publicFunc import Response
from xiongzhanghao.publicFunc import account
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from xiongzhanghao.publicFunc.condition_com import conditionCom
from xiongzhanghao.forms.article import AddForm, UpdateForm, SelectForm
import json, datetime, requests, os
from urllib.parse import urlparse
from backend.articlePublish import DeDe


# 特殊用户 生成页面
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

        back_url = 'article/{}.html'.format(obj.id)
        obj.back_url = back_url
        obj.DomainNameText = ret.text
        obj.article_status = 4
        obj.save()


    response.code = 200
    response.msg = '生成完成'
    return JsonResponse(response.__dict__)



# 查询二级域名
def SearchSecondaryDomainName(request, article_id):
    response = Response.ResponseObj()
    objs = models.xzh_article.objects.get(id=article_id)
    if objs:
        response.data = objs.DomainNameText
    else:
        print('无此id')
    response.code = 200
    response.msg = '查询成功'
    return JsonResponse(response.__dict__)











