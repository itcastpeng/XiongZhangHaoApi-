from xiongzhanghao import models
from xiongzhanghao.publicFunc import Response
from django.http import JsonResponse
# from api.public.token import start
import datetime
from django.db.models import Q

# 判断客户页面 该文章是否删除
def deleteQuery(request):
    # params = start()  # 获取token
    response = Response.ResponseObj()
    now = datetime.datetime.now()
    deletionTime = (now - datetime.timedelta(hours=5)).strftime('%Y-%m-%d %H:%M:%S')
    deletionTime = datetime.datetime.strptime(deletionTime, '%Y-%m-%d %H:%M:%S')

    q = Q(Q(deletionTime__isnull=True) | Q(deletionTime__lte=deletionTime))
    q.add(Q(role_id=61), Q.AND)

    print('q-----> ',q)
    # 查询据上次查询时间 超过xx小时
    objs = models.xzh_userprofile.objects.filter(q)
    obj = objs[0]

    response.code = 200
    response.msg = '查询成功'
    response.data = {
        'website_backstage_url': obj.website_backstage_url,

    }
    return JsonResponse(response.__dict__)