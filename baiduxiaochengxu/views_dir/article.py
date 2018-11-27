from xiongzhanghao import models
from xiongzhanghao.publicFunc import Response
from xiongzhanghao.publicFunc import account
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from xiongzhanghao.publicFunc.condition_com import conditionCom
from baiduxiaochengxu.forms.article import AddForm, UpdateForm, SelectForm
import json, datetime, requests, os
from django.db.models import Q

# from xiongzhanghao.views_dir.user import objLogin


# cerf  token验证 用户展示模块
@csrf_exempt
@account.is_token(models.xcx_userprofile)
def article(request):
    response = Response.ResponseObj()
    if request.method == "GET":
        forms_obj = SelectForm(request.GET)
        if forms_obj.is_valid():
            current_page = forms_obj.cleaned_data['current_page']
            length = forms_obj.cleaned_data['length']
            print('forms_obj.cleaned_data -->', forms_obj.cleaned_data)
            order = request.GET.get('order', '-create_date')
            field_dict = {
                'id': '',
                'title': '__contains',
                'create_date': '',
                'summary': '__contains',
                'content': '__contains',
                'article_status': '',
                'belongToUser_id': '',
            }
            q = conditionCom(request, field_dict)

            print('q -->', q)
            objs = models.xcx_article.objects.select_related('belongToUser').filter(q).order_by(order)
            count = objs.count()

            if length != 0:
                start_line = (current_page - 1) * length
                stop_line = start_line + length
                objs = objs[start_line: stop_line]

            # 返回的数据
            ret_data = []

            for obj in objs:
                print('obj.id--------------> ',obj.id)
                #  将查询出来的数据 加入列表
                ret_data.append({
                    'id': obj.id,
                    'title':obj.title,
                    'summary':obj.summary,
                    'content':obj.content,
                    'create_date':obj.create_date.strftime('%Y-%m-%d %H:%M:%S'),
                    'user_id':obj.user.id,
                    'user_name':obj.user.username,
                    'belongToUser_id':obj.belongToUser_id,
                    'belongToUser_name': obj.belongToUser.username,
                })
            #  查询成功 返回200 状态码
            response.code = 200
            response.msg = '查询成功'
            response.data = {
                'ret_data': ret_data
            }
        else:
            response.code = 402
            response.msg = "请求异常"
            response.data = json.loads(forms_obj.errors.as_json())
    return JsonResponse(response.__dict__)


#  增删改
#  csrf  token验证
@csrf_exempt
@account.is_token(models.xcx_userprofile)
def article_oper(request, oper_type, o_id):
    response = Response.ResponseObj()
    if request.method == "POST":
        form_data = {
            'user_id': request.GET.get('user_id'),
            'title': request.POST.get('title'),     # 标题
            'summary': request.POST.get('summary'), # 摘要
            'content': request.POST.get('content'), # 内容
            'belongToUser_id': request.POST.get('belongToUser_id'),# 归属用户
            'article_program_id':request.POST.get('article_program_id')
        }

        print('form_data===============> ',form_data)
        if oper_type == "add":
            #  创建 form验证 实例（参数默认转成字典）
            forms_obj = AddForm(form_data)
            if forms_obj.is_valid():
                models.xcx_article.objects.create(**forms_obj.cleaned_data)
                response.code = 200
                response.msg = "添加成功"
            else:
                print("验证不通过")
                response.code = 301
                response.msg = json.loads(forms_obj.errors.as_json())

        elif oper_type == "update":
            # 获取需要修改的信息
            forms_obj = UpdateForm(form_data)
            if forms_obj.is_valid():
                print("验证通过")
                #  查询数据库  用户id
                objs = models.xcx_article.objects.filter(
                    id=o_id
                )
                #  更新 数据
                print(forms_obj.cleaned_data)
                if objs:
                    objs.update(**forms_obj.cleaned_data)
                    response.code = 200
                    response.msg = "修改成功"
                else:
                    response.code = 303
                    response.msg = json.loads(forms_obj.errors.as_json())
            else:
                print("验证不通过")
                # print(forms_obj.errors)
                response.code = 301
                # print(forms_obj.errors.as_json())
                #  字符串转换 json 字符串
                response.msg = json.loads(forms_obj.errors.as_json())

        elif oper_type == "delete":
            # 删除 ID
            objs = models.xcx_article.objects.filter(id=o_id)
            if objs:
                objs.delete()
                response.code = 200
                response.msg = "删除成功"
            else:
                response.code = 302
                response.msg = '删除ID不存在'

    else:
        response.code = 402
        response.msg = "请求异常"
    return JsonResponse(response.__dict__)

