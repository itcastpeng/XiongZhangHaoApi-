from django.http import JsonResponse, HttpResponse
import datetime
from django.db.models import Q
from backend.selectDeleteQuery import index
from xiongzhanghao import models
from xiongzhanghao.publicFunc import Response
from xiongzhanghao.publicFunc import account
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.db.models.query import QuerySet


@csrf_exempt
@account.is_token(models.xzh_userprofile)
def user_statistical(request, oper_type):
    response = Response.ResponseObj()
    if request.method == 'POST':
        user_objs = models.xzh_userprofile.objects
        article_objs = models.xzh_article.objects
        datetime_now = datetime.datetime.now()

        now = datetime_now.strftime('%Y-%m-%d')
        start_now = datetime_now.strftime('%Y-%m-%d 00:00:00')
        stop_now = datetime_now.strftime('%Y-%m-%d %H:%M:%S')

        print('now---> ',start_now, stop_now)
        if oper_type == 'user_statistical':
            userObjs = user_objs.filter(userType=1, role_id=61)
            for userObj in userObjs:
                data = {
                    'public_num': '',
                    'belong_user_id': '',
                    'shoulu':0,
                    'zhishu':0,
                    'index_show':0,
                    'zhanxianliang':0,
                    'dianjiliang':0,
                    'fans_num':0
                }

                articleObjs = article_objs.filter(
                    belongToUser_id=userObj.id
                ).filter(
                    create_date__gte=start_now,
                    create_date__lte=stop_now
                )
                data['belong_user_id'] = userObj.id      # 归属用户
                data['public_num'] = articleObjs.count() # 该用户今日发布总数



                statisticsObjs = models.user_statistics.objects.filter(belong_user_id=userObj.id, create_date=now)
                if statisticsObjs:
                    statisticsObjs.update()
                else:
                    statisticsObjs.create()
        else:
            response.code = 301
            response.msg = '请求异常'
    else:
        pass

    return JsonResponse(response.__dict__)









