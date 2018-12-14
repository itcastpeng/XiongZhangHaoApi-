from xiongzhanghao import models
from xiongzhanghao.publicFunc import Response
from xiongzhanghao.publicFunc import account
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from xiongzhanghao.publicFunc.condition_com import conditionCom
from xiongzhanghao.forms.user_billing import SelectForm, AddForm
import json, requests, datetime, time

# cerf  token验证 用户展示模块
@csrf_exempt
@account.is_token(models.xzh_userprofile)
def user_billing(request):
    response = Response.ResponseObj()
    forms_obj = SelectForm(request.GET)
    if forms_obj.is_valid():
        current_page = forms_obj.cleaned_data['current_page']
        length = forms_obj.cleaned_data['length']
        print('forms_obj.cleaned_data -->', forms_obj.cleaned_data)
        order = request.GET.get('order', '-create_date')
        field_dict = {
            'id': '',
            'username': '__contains',
            'create_date': '__contains',
            'belong_user_id': '',
        }
        q = conditionCom(request, field_dict)
        print('q -->', q)
        objs = models.user_billing.objects.select_related('belong_user').filter(q).order_by(order)
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
                'belong_user':obj.belong_user.username,
                'create_date': obj.create_date.strftime('%Y-%m-%d'),
                'create_user_id': obj.create_user_id,
                'create_user': obj.create_user.username,
                'start_time': obj.start_time,
                'stop_time': obj.stop_time,
                'billing_cycle_id': obj.billing_cycle,
                'billing_cycle': obj.get_billing_cycle_display(),
                'note_text': obj.note_text,
            })
        #  查询成功 返回200 状态码
        response.code = 200
        response.msg = '查询成功'
        response.data = {
            'ret_data': ret_data,
            'count':count,
        }

    else:
        response.code = 301
        response.data = json.loads(forms_obj.errors.as_json())

    return JsonResponse(response.__dict__)


#  增删改
#  csrf  token验证
@csrf_exempt
@account.is_token(models.xzh_userprofile)
def user_billing_oper(request, oper_type, o_id):
    response = Response.ResponseObj()
    user_id = request.GET.get('user_id')
    if request.method == 'POST':
        user_id = request.GET.get('user_id')
        form_data = {
            'create_user': user_id,
            'belong_user_id': request.POST.get('belong_user_id'),
            'start_time': request.POST.get('start_time'),
            'stop_time': request.POST.get('stop_time'),
            'billing_cycle': request.POST.get('billing_cycle_id'),
            'note_text': request.POST.get('note_text')
        }
        if form_data.get('start_time') and form_data.get('billing_cycle'):
            response.code = 301
            response.msg = '周期不可全选'
            return JsonResponse(response.__dict__)

        # 添加
        if oper_type == 'add':
            forms_obj = AddForm(form_data)
            if forms_obj.is_valid():
                print('验证成功')
                objForm = forms_obj.cleaned_data

                billing_cycle = objForm.get('billing_cycle')
                start_time = objForm.get('start_time')
                stop_time = objForm.get('stop_time')
                belong_user_id = objForm.get('belong_user_id')
                note_text = objForm.get('note_text')

                start_date_time = start_time
                billing_cycle_id = billing_cycle
                if billing_cycle:
                    billing_cycle_id = billing_cycle[0]
                    start_date_time = billing_cycle[1]
                    stop_time = billing_cycle[2]

                if start_time:
                    start_date_time = start_time[0]
                    stop_time = start_time[1]
                    billing_cycle_id = start_time[2]

                if billing_cycle_id or (start_time and stop_time):

                    if oper_type == 'add':
                        models.user_billing.objects.create(
                            belong_user_id=belong_user_id,
                            billing_cycle=billing_cycle_id,
                            start_time=start_date_time,
                            stop_time=stop_time,
                            create_user_id=user_id,
                            note_text=note_text
                        )
                        response.code = 200
                        response.msg = '创建成功'


                else:
                    response.code = 301
                    response.msg = '请选择一项周期'
            else:
                response.code = 301
                response.msg = json.loads(forms_obj.errors.as_json())

        if oper_type == 'update':
            if request.POST.get('note_text'):
                models.user_billing.objects.filter(id=o_id).update(
                    note_text=request.POST.get('note_text'),
                )
                response.code = 200
                response.msg = '修改成功'
            else:
                response.code = 301
                response.msg = '修改失败'
        # 删除
        elif oper_type == 'delete':
            userObj = models.xzh_userprofile.objects.filter(id=user_id)
            if userObj[0].role_id != 61:
                models.user_billing.objects.filter(id=o_id).delete()
                response.code = 200
                response.msg = '删除成功'
            else:
                response.code = 301
                response.msg = '该用户角色不可删除'
    else:
        response.code = 402
        response.msg = '请求错误'
    return JsonResponse(response.__dict__)














