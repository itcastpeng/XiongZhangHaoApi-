from django.shortcuts import render
from xiongzhanghao import models
from xiongzhanghao.publicFunc import Response
from xiongzhanghao.publicFunc import account
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
import time
import datetime

from django.db.models import Q

from api.forms.select_keywords_cover import AddForm


# cerf  token验证
# 公司查询
@csrf_exempt
@account.is_token(models.xzh_userprofile)
def select_keywords_cover(request):
    response = Response.ResponseObj()
    if request.method == "GET":     # 获取查覆盖的关键词
        start_time = time.time()
        print('start_time --->', start_time)
        dtime = datetime.datetime.now() - datetime.timedelta(minutes=10)
        now_date = datetime.datetime.now().strftime("%Y-%m-%d")

        q = Q(select_date__lt=now_date) | Q(select_date__isnull=True) & Q(get_date__lt=dtime) | Q(get_date__isnull=True)

        print('q -->', q)
        objs = models.xzh_keywords.objects.select_related('user').filter(q).order_by('?')[:10]
        print(objs.query)
        ret_data = []
        if objs:
            obj = objs[0]
            ret_data = {
                'keywords_id': obj.id,
                'keywords': obj.keywords,
                'xiongZhangHaoIndex': obj.user.xiongZhangHaoIndex
            }
            obj.get_date = datetime.datetime.now()
            obj.save()

        stop_time = time.time()
        print('stop_time --->', stop_time, stop_time - start_time)
        response.code = 200
        response.data = ret_data
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
