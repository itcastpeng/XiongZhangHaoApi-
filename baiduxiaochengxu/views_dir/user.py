from django.shortcuts import render, HttpResponse
from xiongzhanghao import models
from xiongzhanghao.publicFunc import Response
from xiongzhanghao.publicFunc import account
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from xiongzhanghao.publicFunc.condition_com import conditionCom
from baiduxiaochengxu.forms.user import AddForm, UpdateForm, SelectForm
from django.db.models import Q
import json, requests, datetime, re


# cerf  token验证 用户展示模块
@csrf_exempt
# @account.is_token(models.xcx_userprofile)
def user(request):
    response = Response.ResponseObj()
    forms_obj = SelectForm(request.GET)
    if forms_obj.is_valid():
        current_page = forms_obj.cleaned_data['current_page']
        length = forms_obj.cleaned_data['length']
        print('forms_obj.cleaned_data -->', forms_obj.cleaned_data)
        order = request.GET.get('order', '-create_date')
        field_dict = {
            'id': '',
            # 'role_id': '',
            'username': '__contains',
            'create_date': '',
            'oper_user__username': '__contains',
            'is_debug': 'bool',
        }
        q = conditionCom(request, field_dict)
        print('q -->', q)
        objs = models.xcx_userprofile.objects.filter(q).order_by(order)
        count = objs.count()

        if length != 0:
            start_line = (current_page - 1) * length
            stop_line = start_line + length
            objs = objs[start_line: stop_line]

        # 返回的数据
        ret_data = []

        for obj in objs:
            username = ''
            oper_user_id = ''
            if obj.oper_user_id:
                oper_user_id = obj.oper_user_id
                username = obj.oper_user.username
            #  将查询出来的数据 加入列表
            ret_data.append({
                'id': obj.id,
                'username': obj.username,
                'oper_user_id': oper_user_id,
                'oper_user': username,                # 操作人
                # 'lunbotu': json.loads(obj.lunbotu),                 # 轮播图
                'lunbotu': obj.lunbotu,                 # 轮播图
                'hospital_logoImg': obj.hospital_logoImg,           # logo图片
                'hospital_phone': obj.hospital_phone,               # 医院电话
                'hospital_introduction': obj.hospital_introduction, # 医院简介
                'hospital_address': obj.hospital_address,           # 医院地址
                'hospital_menzhen': obj.hospital_menzhen,           # 门诊时间
            })

        #  查询成功 返回200 状态码
        response.code = 200
        response.msg = '查询成功'
        response.data = {
            'ret_data': ret_data
        }
    else:
        response.code = 301
        response.data = json.loads(forms_obj.errors.as_json())
    return JsonResponse(response.__dict__)


#  增删改
#  csrf  token验证
@csrf_exempt
# @account.is_token(models.xcx_userprofile)
def user_oper(request, oper_type, o_id):
    response = Response.ResponseObj()
    user_id = request.GET.get('user_id')
    if request.method == "POST":
        form_data = {
            'o_id':o_id,
            'oper_user_id': request.GET.get('user_id'),
            'password': request.POST.get('password'),
            'username': request.POST.get('username'),
            'lunbotu': request.POST.get('lunbotu'),                             # 轮播图
            'hospital_logoImg': request.POST.get('hospital_logoImg'),           # logo图片
            'hospital_phone': request.POST.get('hospital_phone'),               # 医院电话
            'hospital_introduction': request.POST.get('hospital_introduction'), # 医院简介
            'hospital_address': request.POST.get('hospital_address'),       # 医院地址
            'hospital_menzhen': request.POST.get('hospital_menzhen'),       # 门诊时间
        }
        if oper_type == "add":
            print('form_data----->',form_data)
            #  创建 form验证 实例（参数默认转成字典）
            forms_obj = AddForm(form_data)
            if forms_obj.is_valid():
                print("验证通过")
                print('forms_obj.cleaned_data==> ',forms_obj.cleaned_data)
                models.xcx_userprofile.objects.create(**forms_obj.cleaned_data)
                response.code = 200
                response.msg = "添加成功"
            else:
                print("验证不通过")
                # print(forms_obj.errors)
                response.code = 301
                # print(forms_obj.errors.as_json())
                response.msg = json.loads(forms_obj.errors.as_json())

        elif oper_type == "update":
            # 获取需要修改的信息
            forms_obj = UpdateForm(form_data)
            if forms_obj.is_valid():
                print("验证通过")
                formObjs = forms_obj.cleaned_data
                objs = models.xcx_userprofile.objects.filter(id=o_id)
                if objs:
                    #  更新 数据
                    response.code = 200
                    response.msg = "修改成功"
                    objs.update(**formObjs)
                else:
                    response.code = 301
                    response.msg = '无此ID'
            else:
                print("验证不通过")
                # print(forms_obj.errors)
                response.code = 301
                # print(forms_obj.errors.as_json())
                #  字符串转换 json 字符串
                response.msg = json.loads(forms_obj.errors.as_json())

        elif oper_type == "delete":
            # 删除 ID
            if o_id == user_id:
                response.code = 301
                response.msg = '不能删除自己'
            else:
                objs = models.xcx_userprofile.objects.get(id=o_id)
                if objs:
                    objs.delete()
                    response.code = 200
                    response.msg = "删除成功"
                else:
                    response.code = 302
                    response.msg = '删除ID不存在'
            response.data = {}

    else:
        # 查询该用户所有栏目
        response.code = 402
        response.msg = "请求异常"

    return JsonResponse(response.__dict__)














