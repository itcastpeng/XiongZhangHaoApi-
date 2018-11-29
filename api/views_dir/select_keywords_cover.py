from django.shortcuts import render
from xiongzhanghao import models
from xiongzhanghao.publicFunc import Response
from xiongzhanghao.publicFunc import account
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
import time, redis
import datetime, json

from django.db.models import Q
from XiongZhangHaoApi_celery.tasks import get_keyword_task
from api.forms.select_keywords_cover import AddForm
import random



@csrf_exempt
@account.is_token(models.xzh_userprofile)
def get_keyword_task(request):
    response = Response.ResponseObj()
    redis_rc = redis.Redis(host='redis://redis_host', port=6379, db=4, decode_responses=True)
    # redis_rc = redis.Redis(host='127.0.0.1', port=6379, db=4, decode_responses=True)

    start_time = time.time()
    print('start_time --->', start_time)
    dtime = datetime.datetime.now() - datetime.timedelta(minutes=10)
    now_date = datetime.datetime.now().strftime("%Y-%m-%d")

    q = Q(select_date__lt=now_date) | Q(select_date__isnull=True) & Q(get_date__lt=dtime) | Q(get_date__isnull=True)

    print('q -->', q)
    objs = models.xzh_keywords.objects.select_related('user').filter(q)[:1000]
    # print(objs.query)
    retData = []
    for obj in objs:

        # obj = objs[random.randint(0, objs.count())]
        ret_data = {
            'keywords_id': obj.id,
            'keywords': obj.keywords,
            'xiongZhangHaoIndex': obj.user.xiongZhangHaoIndex
        }
        obj.get_date = datetime.datetime.now()
        obj.save()
        # retData.append(ret_data)
        redis_rc.lpush('keyword', ret_data)
    stop_time = time.time()
    print('stop_time --->', stop_time, stop_time - start_time)
    # print('retData=============> ',retData)
    response.code = 200
    response.msg = '查询成功'
    return JsonResponse(response.__dict__)




@csrf_exempt
@account.is_token(models.xzh_userprofile)
def select_keywords_cover(request):
    response = Response.ResponseObj()
    if request.method == "GET":     # 获取查覆盖的关键词
        redis_rc = redis.Redis(host='redis://redis_host', port=6379, db=4, decode_responses=True)
        # redis_rc = redis.Redis(host='127.0.0.1', port=6379, db=4, decode_responses=True)
        task_keyword = redis_rc.lpop('keyword')
        if task_keyword:
            task_keyword = eval(task_keyword)
            keywords_id = task_keyword.get('keywords_id')
            print('keywords_id=========> ',keywords_id)
            objs = models.xzh_keywords.objects.filter(id=keywords_id)
            obj = objs[0]
            obj.get_date = datetime.datetime.now()
            obj.save()
            response.data = task_keyword
            response.code = 200
        else:
            get_keyword_task.delay()

    else:   # 提交查询关键词覆盖的结果
        # {'url': 'http://author.baidu.com/home/1611292686377463', 'keywords': '四川肛肠医院', 'rank': 4, 'keywords_id': 834}
        print('保存查覆盖结果')
        form_obj = AddForm(request.POST)
        if form_obj.is_valid():
            rank = form_obj.cleaned_data.get('rank')
            keywords_id = form_obj.cleaned_data.get('keywords_id')
            models.xzh_keywords.objects.filter(id=keywords_id).update(select_date=datetime.datetime.now())
            print('rank -->', rank, type(rank))
            if rank > 0:
                models.xzh_keywords_detail.objects.create(
                    xzh_keywords_id=form_obj.cleaned_data.get('keywords_id'),
                    url=form_obj.cleaned_data.get('url'),
                    rank=form_obj.cleaned_data.get('rank'),
                )
        else:
            print('form_obj.errors.as_json() -->', form_obj.errors.as_json())
    return JsonResponse(response.__dict__)


# cerf  token验证
# @csrf_exempt
# @account.is_token(models.xzh_userprofile)
# def select_keywords_cover(request):
#     response = Response.ResponseObj()
#     if request.method == "GET":     # 获取查覆盖的关键词
#         redis_rc = redis.Redis(host='192.168.100.20', port=6379, db=4, decode_responses=True)
#         start_time = time.time()
#         print('start_time --->', start_time)
#         dtime = datetime.datetime.now() - datetime.timedelta(minutes=10)
#         now_date = datetime.datetime.now().strftime("%Y-%m-%d")
#
#         q = Q(select_date__lt=now_date) | Q(select_date__isnull=True) & Q(get_date__lt=dtime) | Q(get_date__isnull=True)
#
#         print('q -->', q)
#         objs = models.xzh_keywords.objects.select_related('user').filter(q)[:10]
#         # print(objs.query)
#         ret_data = []
#         if objs:
#             obj = objs[random.randint(0, objs.count())]
#             ret_data = {
#                 'keywords_id': obj.id,
#                 'keywords': obj.keywords,
#                 'xiongZhangHaoIndex': obj.user.xiongZhangHaoIndex
#             }
#             obj.get_date = datetime.datetime.now()
#             obj.save()
#
#         stop_time = time.time()
#         print('stop_time --->', stop_time, stop_time - start_time)
#         response.code = 200
#         response.data = ret_data
#     else:   # 提交查询关键词覆盖的结果
#         # {'url': 'http://author.baidu.com/home/1611292686377463', 'keywords': '四川肛肠医院', 'rank': 4, 'keywords_id': 834}
#         print('保存查覆盖结果')
#         form_obj = AddForm(request.POST)
#         if form_obj.is_valid():
#             rank = form_obj.cleaned_data.get('rank')
#             keywords_id = form_obj.cleaned_data.get('keywords_id')
#             models.xzh_keywords.objects.filter(id=keywords_id).update(select_date=datetime.datetime.now())
#             print('rank -->', rank, type(rank))
#             if rank > 0:
#                 models.xzh_keywords_detail.objects.create(
#                     xzh_keywords_id=form_obj.cleaned_data.get('keywords_id'),
#                     url=form_obj.cleaned_data.get('url'),
#                     rank=form_obj.cleaned_data.get('rank'),
#                 )
#         else:
#             print('form_obj.errors.as_json() -->', form_obj.errors.as_json())
#     return JsonResponse(response.__dict__)

#
# #  csrf  token验证
# # 公司操作
# @csrf_exempt
# @account.is_token(models.xzh_userprofile)
# def company_oper(request, oper_type, o_id):
#     response = Response.ResponseObj()
#     if request.method == "POST":
#
#         # 添加公司
#         if oper_type == "add":
#             form_data = {
#                 'user_id': o_id,
#                 'oper_user_id': request.GET.get('user_id'),
#                 'name': request.POST.get('name'),
#             }
#             #  创建 form验证 实例（参数默认转成字典）
#             forms_obj = AddForm(form_data)
#             if forms_obj.is_valid():
#                 print("验证通过")
#                 # print(forms_obj.cleaned_data)
#                 #  添加数据库
#                 # print('forms_obj.cleaned_data-->',forms_obj.cleaned_data)
#                 models.xzh_company.objects.create(**forms_obj.cleaned_data)
#                 response.code = 200
#                 response.msg = "添加成功"
#             else:
#                 print("验证不通过")
#                 # print(forms_obj.errors)
#                 response.code = 301
#                 # print(forms_obj.errors.as_json())
#                 response.msg = json.loads(forms_obj.errors.as_json())
#
#         # 修改公司
#         elif oper_type == "update":
#             # 获取需要修改的信息
#             form_data = {
#                 'o_id': o_id,
#                 'name': request.POST.get('name'),
#             }
#
#             forms_obj = UpdateForm(form_data)
#             if forms_obj.is_valid():
#                 print("验证通过")
#                 print(forms_obj.cleaned_data)
#                 o_id = forms_obj.cleaned_data['o_id']
#                 name = forms_obj.cleaned_data['name']
#                 #  查询数据库  用户id
#                 objs = models.xzh_company.objects.filter(
#                     id=o_id
#                 )
#                 #  更新 数据
#                 if objs:
#                     objs.update(
#                         name=name
#                     )
#
#                     response.code = 200
#                     response.msg = "修改成功"
#                 else:
#                     response.code = 303
#                     response.msg = json.loads(forms_obj.errors.as_json())
#
#             else:
#                 print("验证不通过")
#                 # print(forms_obj.errors)
#                 response.code = 301
#                 # print(forms_obj.errors.as_json())
#                 #  字符串转换 json 字符串
#                 response.msg = json.loads(forms_obj.errors.as_json())
#
#         # 删除公司
#         elif oper_type == "delete":
#             # 删除 ID
#             objs = models.xzh_company.objects.filter(id=o_id)
#             if objs:
#                 objs.delete()
#                 response.code = 200
#                 response.msg = "删除成功"
#             else:
#                 response.code = 302
#                 response.msg = '删除ID不存在'
#
#     else:
#         response.code = 402
#         response.msg = "请求异常"
#
#     return JsonResponse(response.__dict__)
