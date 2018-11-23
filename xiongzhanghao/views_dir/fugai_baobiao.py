from django.shortcuts import render, HttpResponse
from xiongzhanghao import models
from xiongzhanghao.publicFunc import Response
from xiongzhanghao.publicFunc import account
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from xiongzhanghao.publicFunc.condition_com import conditionCom
from xiongzhanghao.forms.fugai_baobiao import SelectForm, AddForm, UpdateForm, AdminAddForm, AdminUpdateForm

import json
import datetime


# cerf  token验证 用户展示模块
@csrf_exempt
@account.is_token(models.xzh_userprofile)
def fugai_baobiao(request):
    print('fugai_baobiao --->', fugai_baobiao)
    response = Response.ResponseObj()
    if request.method == "GET":
        response = Response.ResponseObj()

        forms_obj = SelectForm(request.GET)
        if forms_obj.is_valid():
            current_page = forms_obj.cleaned_data['current_page']
            length = forms_obj.cleaned_data['length']
            print('forms_obj.cleaned_data -->', forms_obj.cleaned_data)
            order = request.GET.get('order', '-create_date')
            field_dict = {
                'id': '',
                'status': '',
                'create_date': '',
            }
            # request_obj = {
            #     'GET': {
            #         'id': request.GET.get('id'),
            #         'create_date': request.GET.get('create_date'),
            #         'user_id': request.GET.get('uid'),
            #     }
            # }
            q = conditionCom(request, field_dict)



            print('q -->', q)
            objs = models.xzh_fugai_baobiao.objects.select_related('user').filter(q).filter(user__role_id=61).order_by(order)
            uid = request.GET.get('uid')
            print('uid -->', uid)
            if uid:
                objs = objs.filter(user_id=uid)
            count = objs.count()

            if length != 0:
                start_line = (current_page - 1) * length
                stop_line = start_line + length
                objs = objs[start_line: stop_line]

            # 返回的数据
            ret_data = []
            index = 0
            for obj in objs:
                index += 1

                #  将查询出来的数据 加入列表
                ret_data.append({
                    'id': obj.id,
                    'user_id': obj.user_id,
                    'username': obj.user.username,
                    'keywords_num': obj.keywords_num,
                    'today_cover': obj.today_cover,
                    'total_cover': obj.total_cover,
                    'publish_num': obj.publish_num,
                    'status': obj.get_status_display(),
                    'create_date': obj.create_date.strftime('%Y-%m-%d %H:%M:%S'),
                    'keywordIndex': index
                })
            #  查询成功 返回200 状态码
            response.code = 200
            response.msg = '查询成功'
            response.data = {
                'ret_data': ret_data,
                'data_count': count,
                'status_choices': models.xzh_fugai_baobiao.status_choices,
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
@account.is_token(models.xzh_userprofile)
def fugai_baobiao_oper(request, oper_type, o_id):
    response = Response.ResponseObj()
    if request.method == "POST":
        pass
    else:
        # 覆盖报表展开详情
        if oper_type == 'detail':
            objs = models.xzh_fugai_baobiao_detail.objects.filter(xzh_fugai_baobiao_id=o_id).order_by('-create_date')

            # 返回的数据
            ret_data = []

            for obj in objs:
                #  将查询出来的数据 加入列表
                ret_data.append({
                    'id': obj.id,
                    'link_num': obj.link_num,
                    'cover_num': obj.cover_num,
                    'baobiao_url': obj.baobiao_url,
                    'create_date': obj.create_date.strftime('%Y-%m-%d')
                })
            #  查询成功 返回200 状态码
            response.code = 200
            response.msg = '查询成功'
            response.data = {
                'ret_data': ret_data,
            }

        else:
            response.code = 402
            response.msg = "请求异常"

    return JsonResponse(response.__dict__)











