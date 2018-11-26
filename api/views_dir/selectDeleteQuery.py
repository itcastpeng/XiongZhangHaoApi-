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


# 获取页面标题及aid
@csrf_exempt
@account.is_token(models.xzh_userprofile)
def selectDeleteQuery(request, oper_type):
    response = Response.ResponseObj()

    # 爬取发时时间 大于最小发布时间 的客户后台数据
    if oper_type == 'deleteQuery':   # 判断上次读取时间超过5小时的 吐出数据
        # params = start()  # 获取token
        now = datetime.datetime.now()
        deletionTime = (now - datetime.timedelta(hours=2)).strftime('%Y-%m-%d %H:%M:%S')
        deletionTime = datetime.datetime.strptime(deletionTime, '%Y-%m-%d %H:%M:%S')

        q = Q(Q(deletionTime__isnull=True) | Q(deletionTime__lte=deletionTime))
        q.add(Q(role_id=61) & Q(userType=1) & Q(website_backstage_url__isnull=False), Q.AND)

        print('q-----> ',q)
        # 查询据上次查询时间 超过xx小时
        timeObjs = models.xzh_article.objects.order_by('create_date')
        # objs = models.xzh_userprofile.objects.filter(q)
        objs = models.xzh_userprofile.objects.select_related('role').filter(q)
        if objs:
            obj = objs[0]
            obj.user_article_result = ''
            response.code = 200
            response.msg = '查询成功'
            response.data = {
                'o_id': obj.id,
                'website_backstage_url': obj.website_backstage_url,
                'cookie': obj.cookies,
                'website_backstage_password': obj.website_backstage_password,
                'website_backstage_username': obj.website_backstage_username,
                'maxtime':timeObjs[0].create_date.strftime('%Y-%m-%d %H:%M:%S')
            }
            obj.deletionTime = now
            obj.save()

    # 插入数据库
    elif oper_type == 'deleteQueryModel':
        # print('=-=====================存入数据库')
        result_data = request.POST.get('result_data')
        o_id = request.POST.get('o_id')
        if result_data and o_id:
            objs = models.xzh_userprofile.objects.filter(id=o_id)
            obj = objs[0]
            obj.user_article_result = result_data
            obj.save()

    # 定时器判断是否删除
    elif oper_type == 'judgeToDelete':
        objs = models.xzh_article.objects.filter(
            article_status=5,
            belongToUser__userType=1
        )
        for obj in objs:
            user_article_result = obj.belongToUser.user_article_result
            note_content = ''
            if str(obj.aid) in user_article_result and obj.title.strip() in user_article_result:
                print(obj.aid, obj.title, 'user_article_result========>',user_article_result)
                is_delete = False
            else:
                is_delete = True
                note_content = '客户后台可能被删除,请管理员查看'
            obj.is_delete = is_delete
            obj.note_content = note_content
            obj.save()
    return JsonResponse(response.__dict__)

