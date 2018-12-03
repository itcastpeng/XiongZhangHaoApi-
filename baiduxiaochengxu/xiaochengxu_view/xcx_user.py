
from xiongzhanghao import models
from xiongzhanghao.publicFunc import Response
from xiongzhanghao.publicFunc import account
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from xiongzhanghao.publicFunc.condition_com import conditionCom
from baiduxiaochengxu.forms.article import  SelectForm
import json, datetime, requests, os
from django.db.models import Q

@csrf_exempt
# @account.is_token(models.xcx_userprofile)
def user(request):
    response = Response.ResponseObj()
    token = 'd7361566c366c19fabaa91c5f46c3086'
    timestamp = 123
    user_id=9
    response.code = 200
    response.msg = '查询成功'
    response.data = {
        'token':token,
        'timestamp':timestamp,
        'user_id':user_id
    }
    return JsonResponse(response.__dict__)

def user_oper(request, oper_type, o_id):
    response = Response.ResponseObj()
    if oper_type == 'select':
        objs = models.xcx_userprofile.objects.filter(id=o_id)
        count = objs.count()
        data_list = []
        for obj in objs:
            lunbotu = ''
            # if obj.lunbotu:
            #     lunbotu = json.loads(obj.lunbotu)
            data_list.append({
                'lunbotu':obj.lunbotu,
                'hospital_logoImg':obj.hospital_logoImg,
                'hospital_phone':obj.hospital_phone,
                'hospital_introduction':obj.hospital_introduction,
                'hospital_address':obj.hospital_address,
                'hospital_menzhen':obj.hospital_menzhen,
                'username':obj.username,
                'id':obj.id
            })
        response.code = 200
        response.msg = '查询成功'
        response.data = {
            'data_list':data_list,
            'count':count
        }
    else:
        response.code = 402
        response.msg = '请求异常'
    return JsonResponse(response.__dict__)



