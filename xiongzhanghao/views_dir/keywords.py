from django.shortcuts import render, HttpResponse
from xiongzhanghao import models
from xiongzhanghao.publicFunc import Response
from xiongzhanghao.publicFunc import account
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from xiongzhanghao.publicFunc.condition_com import conditionCom
from xiongzhanghao.forms.keywords import AddForm, SelectForm, BatchDeleteForm
from django.db.models import Q
from backend.articlePublish import DeDe
from XiongZhangHaoApi_celery.tasks import celeryGetDebugUser
from urllib.parse import urlparse
import json, requests, datetime


# cerf  token验证 用户展示模块
@csrf_exempt
# @account.is_token(models.xzh_userprofile)
def keywords(request):
    response = Response.ResponseObj()
    if request.method == "GET":
        response = Response.ResponseObj()

        forms_obj = SelectForm(request.GET)
        if forms_obj.is_valid():
            current_page = forms_obj.cleaned_data['current_page']
            length = forms_obj.cleaned_data['length']
            uid = forms_obj.cleaned_data['uid']
            print('forms_obj.cleaned_data -->', forms_obj.cleaned_data)
            order = request.GET.get('order', '-create_date')
            field_dict = {
                'id': '',
                'create_date': '',
            }
            q = conditionCom(request, field_dict)
            q.add(Q(user_id=uid), Q.AND)

            print('q -->', q)
            objs = models.xzh_keywords.objects.filter(q).order_by(order)
            count = objs.count()

            if length != 0:
                start_line = (current_page - 1) * length
                stop_line = start_line + length
                objs = objs[start_line: stop_line]

            # 返回的数据
            ret_data = []

            for obj in objs:

                #  将查询出来的数据 加入列表
                ret_data.append({
                    'id': obj.id,
                    'keywords': obj.keywords,
                    'create_date': obj.create_date.strftime('%Y-%m-%d %H:%M:%S')
                })
            #  查询成功 返回200 状态码
            response.code = 200
            response.msg = '查询成功'
            response.data = {
                'ret_data': ret_data,
                'data_count': count,
            }
        else:
            response.code = 301
            response.data = json.loads(forms_obj.errors.as_json())
    else:
        response.code = 402
        response.msg = '请求异常'
    return JsonResponse(response.__dict__)


#  增删改
#  csrf  token验证
@csrf_exempt
# @account.is_token(models.xzh_userprofile)
def keywords_oper(request, oper_type, o_id):
    response = Response.ResponseObj()

    response.code = 402
    response.msg = "请求异常"

    if request.method == "POST":
        if oper_type == "add":
            form_data = {
                'user_id': request.POST.get('uid'),
                'keywords': request.POST.get('keywords')
            }
            print('form_data----->', form_data)
            #  创建 form验证 实例（参数默认转成字典）

            forms_obj = AddForm(form_data)
            if forms_obj.is_valid():
                print("验证通过")
                query_list = []
                user_id = forms_obj.cleaned_data.get('user_id')
                keywords_list = forms_obj.cleaned_data.get('keywords')
                for keywords in keywords_list:
                    if not models.xzh_keywords.objects.filter(user_id=user_id, keywords=keywords):
                        query_list.append(models.xzh_keywords(
                            user_id=user_id,
                            keywords=keywords
                        ))

                models.xzh_keywords.objects.bulk_create(query_list)

                response.code = 200
                response.msg = "添加成功"
            else:
                print("验证不通过")
                response.code = 301
                response.msg = json.loads(forms_obj.errors.as_json())

        elif oper_type == "delete":
            # 删除 ID

            objs = models.xzh_keywords.objects.get(id=o_id)
            if objs:
                objs.delete()
                response.code = 200
                response.msg = "删除成功"
            else:
                response.code = 302
                response.msg = '删除ID不存在'
            response.data = {}

        # 批量删除
        elif oper_type == "batch_delete":
            form_data = {
                'user_id': o_id,
            }
            forms_obj = BatchDeleteForm(form_data)
            if forms_obj.is_valid():
                user_id = forms_obj.cleaned_data.get('user_id')
                models.xzh_keywords.objects.filter(user_id=user_id).delete()

                response.code = 200
                response.msg = "批量删除成功"
            else:
                response.code = 301
                response.msg = json.loads(forms_obj.errors.as_json())
    return JsonResponse(response.__dict__)











