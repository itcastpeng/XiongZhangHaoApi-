from xiongzhanghao import models
from xiongzhanghao.publicFunc import Response
from xiongzhanghao.publicFunc import account
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from xiongzhanghao.publicFunc.condition_com import conditionCom
from baiduxiaochengxu.forms.program import AddForm, UpdateForm, SelectForm
import json, datetime, requests, os
from django.db.models import Q


# cerf  token验证 用户展示模块
@csrf_exempt
# @account.is_token(models.xcx_userprofile)
def program(request):
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
                'create_date': '',
                'program_name': '__contains',
                'program_type': '',
                'program_text': '',
                'belongToUser_id': '',
            }
            q = conditionCom(request, field_dict)

            print('q -->', q)
            objs = models.xcx_program_management.objects.select_related('belongUser').filter(q).order_by(order)
            count = objs.count()

            if length != 0:
                start_line = (current_page - 1) * length
                stop_line = start_line + length
                objs = objs[start_line: stop_line]

            # 返回的数据
            ret_data = []
            num = 0
            for obj in objs:

                print('obj.id--------------> ',obj.id)
                #  将查询出来的数据 加入列表
                ret_data.append({
                    'id': obj.id,
                    'program_name':obj.program_name,
                    'belongUser_id':obj.belongUser_id,
                    'belongUser':obj.belongUser.username,
                    'program_type_id':obj.program_type,
                    # 'suoluetu':json.loads(obj.suoluetu),
                    'suoluetu':obj.suoluetu,
                    'program_type':obj.get_program_type_display(),
                    'create_date':obj.create_date.strftime('%Y-%m-%d %H:%M:%S'),
                })
                if int(obj.program_type) == 2:
                    ret_data[num]['program_text'] = obj.program_text
                num += 1
            #  查询成功 返回200 状态码
            response.code = 200
            response.msg = '查询成功'
            response.data = {
                'ret_data': ret_data,
                'type_list': models.xcx_program_management.program_type_choices
            }
        else:
            response.code = 402
            response.msg = "请求异常"
            response.data = json.loads(forms_obj.errors.as_json())
    return JsonResponse(response.__dict__)


#  增删改
#  csrf  token验证
@csrf_exempt
# @account.is_token(models.xcx_userprofile)
def program_oper(request, oper_type, o_id):
    response = Response.ResponseObj()
    if request.method == "POST":
        form_data = {
            # 'belongUser_id': request.GET.get('user_id'),
            'belongUser_id': 4,
            'program_name': request.POST.get('program_name'),     # 栏目名称
            'program_type': request.POST.get('program_type'),     # 栏目类型
            'suoluetu': request.POST.get('suoluetu'),             # 缩略图
            'program_text': request.POST.get('program_text', '')  # 单页设置内容
        }
        program_type = form_data.get('program_type')
        program_text = form_data.get('program_text')
        if program_type and program_text and int(program_type) == 1:
            response.code = 301
            response.msg = '栏目类型为单页是, 可添加单页内容'
        else:
            print('form_data===============> ',form_data)
            if oper_type == "add":
                #  创建 form验证 实例（参数默认转成字典）
                forms_obj = AddForm(form_data)
                if forms_obj.is_valid():
                    models.xcx_program_management.objects.create(**forms_obj.cleaned_data)
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
                    objs = models.xcx_program_management.objects.filter(
                        id=o_id
                    )
                    #  更新 数据
                    print(forms_obj.cleaned_data)
                    if objs:
                        objs.update(**forms_obj.cleaned_data)
                        response.code = 200
                        response.msg = "修改成功"
                    else:
                        response.code = 301
                        response.msg = '无此栏目'
                else:
                    print("验证不通过")
                    # print(forms_obj.errors)
                    response.code = 301
                    # print(forms_obj.errors.as_json())
                    #  字符串转换 json 字符串
                    response.msg = json.loads(forms_obj.errors.as_json())

            elif oper_type == "delete":
                # 删除 ID
                objs = models.xcx_program_management.objects.filter(id=o_id)
                if objs:
                    articleObj = models.xcx_article.objects.filter(article_program_id=o_id)
                    if not articleObj:
                        objs.delete()
                        response.code = 200
                        response.msg = "删除成功"
                    else:
                        response.code = 301
                        response.msg = '该栏目含有文章, 不可删除'
                else:
                    response.code = 302
                    response.msg = '删除ID不存在'

    else:
        response.code = 402
        response.msg = "请求异常"
    return JsonResponse(response.__dict__)

