from xiongzhanghao import models
from xiongzhanghao.publicFunc import Response
from xiongzhanghao.publicFunc import account
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from xiongzhanghao.publicFunc.condition_com import conditionCom
from xiongzhanghao.forms.article import AddForm, UpdateForm, SelectForm
import json, datetime, requests, os
from urllib.parse import urlparse
from backend.articlePublish import DeDe


# 特殊用户 生成页面

# def specialUserGenerateThePage(request):
#     if request.method == 'GET':
#         models
