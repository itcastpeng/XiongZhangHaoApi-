from xiongzhanghao import models
from xiongzhanghao.publicFunc import Response
from xiongzhanghao.publicFunc import account
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from xiongzhanghao.publicFunc.condition_com import conditionCom
from baiduxiaochengxu.forms.program import SelectForm
import json, datetime, requests, os
from django.db.models import Q


# cerf  token验证 用户展示模块
@csrf_exempt
@account.is_token(models.xcx_userprofile)
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

