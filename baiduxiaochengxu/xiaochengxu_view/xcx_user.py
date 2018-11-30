
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






