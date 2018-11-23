""" 调度器 """
from django.shortcuts import render
from xiongzhanghao import models
from xiongzhanghao.publicFunc import Response
from xiongzhanghao.publicFunc import account
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
import time
import datetime
from django.db.models import Q


def theScheduler(request):
    response = Response.ResponseObj()
    userObjs = models.xzh_userprofile.objects
    articleObjs = models.xzh_article.objects

    resule_data = {
        'task_id': None,
        'flag': False
    }


    if not resule_data['flag']:
        getCookieObjs = userObjs.filter(is_debug=False, role_id=61, userType=1)  # 获取栏目 及 cookie
        if getCookieObjs:
            resule_data['flag'] = True
            resule_data['task_id'] = 1
            print('获取栏目')

    if not resule_data['flag']:
        now_date = datetime.datetime.now()
        q = Q()
        q.add(Q(send_time__lte=now_date) | Q(send_time__isnull=True), Q.AND)
        sendArticleObjs = articleObjs.select_related('belongToUser').filter(article_status=1,belongToUser__is_debug=1).filter(q)
        if sendArticleObjs:
            resule_data['flag'] = True
            resule_data['task_id'] = 2
            print('发布文章')

    if not resule_data['flag']:
        timedRefreshAuditObjs = articleObjs.filter(article_status=2, is_audit=0, aid__isnull=False)
        if timedRefreshAuditObjs:
            resule_data['flag'] = True
            resule_data['task_id'] = 3
            print('判断是否审核')

    if not resule_data['flag']:
        now = datetime.datetime.now()
        deletionTime = (now - datetime.timedelta(hours=2)).strftime('%Y-%m-%d %H:%M:%S')
        deletionTime = datetime.datetime.strptime(deletionTime, '%Y-%m-%d %H:%M:%S')
        q = Q(Q(deletionTime__isnull=True) | Q(deletionTime__lte=deletionTime))
        q.add(Q(role_id=61) & Q(userType=1), Q.AND)

        deleteQuery = userObjs.filter(q)
        if deleteQuery:
            resule_data['flag'] = True
            resule_data['task_id'] = 4
            print('判断是否审核')



    response.code = 200
    response.msg = '查询成功'
    response.data = resule_data
    return JsonResponse(response.__dict__)

