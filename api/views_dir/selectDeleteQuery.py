from xiongzhanghao import models
from xiongzhanghao.publicFunc import Response
from django.http import JsonResponse
from django.db.models import Q, Count
import datetime, time
from bs4 import BeautifulSoup


# 判断客户页面 该文章是否删除
def deleteQuery(request):
    response = Response.ResponseObj()
    objs = models.xzh_article.objects.filter(article_status__in=[2, 4, 5])
    for obj in objs:
        obj.user



    return JsonResponse(response.__dict__)
















