from django.shortcuts import render, HttpResponse
from xiongzhanghao import models
from xiongzhanghao.publicFunc import Response
from xiongzhanghao.publicFunc import account
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from xiongzhanghao.publicFunc.condition_com import conditionCom
from xiongzhanghao.forms.add_fans import AddForm, UpdateForm, SelectForm
from django.db.models import Q
from backend.articlePublish import DeDe
from urllib.parse import urlparse
import json, requests, datetime


# cerf  token验证 用户展示模块
@csrf_exempt
@account.is_token(models.xzh_userprofile)
def fans(request):
    response = Response.ResponseObj()
    forms_obj = SelectForm(request.GET)
    if forms_obj.is_valid():
        current_page = forms_obj.cleaned_data['current_page']
        length = forms_obj.cleaned_data['length']
        print('forms_obj.cleaned_data -->', forms_obj.cleaned_data)
        order = request.GET.get('order', '-create_date')
        field_dict = {
            'id': '',
            'role_id': '',
            'username': '__contains',
            'create_date': '',
            'oper_user__username': '__contains',
            'is_debug': 'bool',
        }
        q = conditionCom(request, field_dict)


        print('q -->', q)
        objs = models.xzh_add_fans.objects.select_related('belong_user').filter(q).order_by(order)
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
                'belong_user_id':obj.belong_user_id,    # 归属人ID
                'belong_user':obj.belong_user.username, # 归属人名字
                'befor_add_fans':obj.befor_add_fans,    # 加粉前 粉丝数量
                'after_add_fans':obj.after_add_fans,    # 加分后 粉丝数量
                'add_fans_num':obj.add_fans_num,        # 添加的粉丝数量
                'xiongzhanghaoID':obj.xiongzhanghaoID,  # 熊掌号ID
                'search_keyword':obj.search_keyword,    # 熊掌号搜索关键词
                'status':obj.get_status_display(),
                'status_id':obj.status,
                'create_date':obj.create_date.strftime('%Y-%m-%d %H:%M:%S'),
                'errorText':obj.errorText ,              # 错误日志

            })
        #  查询成功 返回200 状态码
        response.code = 200
        response.msg = '查询成功'
        response.data = {
            'ret_data': ret_data,
        }
    else:
        response.code = 301
        response.data = json.loads(forms_obj.errors.as_json())
    return JsonResponse(response.__dict__)


#  增删改
#  csrf  token验证
@csrf_exempt
@account.is_token(models.xzh_userprofile)
def fans_oper(request, oper_type, o_id):
    response = Response.ResponseObj()
    user_id = request.GET.get('user_id')
    if request.method == "POST":
        form_data = {
            'o_id':o_id,
            'oper_user_id': request.GET.get('user_id'),
            'belong_user_id': request.POST.get('belong_user_id'),
            'add_fans_num': request.POST.get('add_fans_num'),
            'xiongzhanghaoID': request.POST.get('xiongzhanghaoID'),
            'search_keyword': request.POST.get('search_keyword'),
        }
        if oper_type == "add":
            print('form_data----->',form_data)
            #  创建 form验证 实例（参数默认转成字典）

            forms_obj = AddForm(form_data)
            if forms_obj.is_valid():
                models.xzh_add_fans.objects.create(**forms_obj.cleaned_data)
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
                models.xzh_add_fans.objects.filter(id=o_id).update(
                    belong_user_id=formObjs.get('belong_user_id'),
                    add_fans_num=formObjs.get('add_fans_num'),
                    xiongzhanghaoID=formObjs.get('xiongzhanghaoID'),
                    search_keyword=formObjs.get('search_keyword'),
                )
                response.code = 200
                response.msg = "修改成功"
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
                objs = models.xzh_add_fans.objects.filter(id=o_id)
                if objs:
                    obj = objs[0]
                    obj.delete()
                    response.code = 200
                    response.msg = "删除成功"
                else:
                    response.code = 302
                    response.msg = '删除ID不存在'
            response.data = {}

    else:
        response.code = 402
        response.msg = "请求异常"

    return JsonResponse(response.__dict__)














