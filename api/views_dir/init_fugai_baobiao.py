

from django.shortcuts import render, HttpResponse
from xiongzhanghao import models
from xiongzhanghao.publicFunc import Response
from xiongzhanghao.publicFunc import account
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from xiongzhanghao.publicFunc.condition_com import conditionCom
from xiongzhanghao.forms.keywords import AddForm, SelectForm, BatchDeleteForm
from django.db.models import Q
from backend.articlePublish import DeDe
from urllib.parse import urlparse
import json, requests, datetime


# cerf  token验证 用户展示模块
@csrf_exempt
@account.is_token(models.xzh_userprofile)
def init_fugai_baobiao(request):
    response = Response.ResponseObj()

    user_objs = models.xzh_userprofile.objects.filter(role_id=61)
    for user_obj in user_objs:
        user_id = user_obj.id

        data = {
            'user_id': user_id,
            'keywords_num': 0,
            'status': 1,
            'today_cover': 0,
            'total_cover': 0,
            'publish_num': 0,
        }
        xzh_keywords_objs = models.xzh_keywords.objects.filter(user_id=user_id)
        data['keywords_num'] = xzh_keywords_objs.count()  # 关键词数

        if data['keywords_num'] > 0:
            now_date = datetime.datetime.now().strftime("%Y-%m-%d")

            if xzh_keywords_objs.filter(select_date__lt=now_date).count() == 0:
                data['status'] = 2  # 查询完成

            xzh_fugai_baobiao_detail_objs = models.xzh_fugai_baobiao_detail.objects.filter(
                xzh_fugai_baobiao__user_id=user_id)
            data['today_cover'] = xzh_fugai_baobiao_detail_objs.filter(create_date=now_date).count()  # 今日覆盖
            data['total_cover'] = xzh_fugai_baobiao_detail_objs.count()  # 总覆盖

        data['publish_num'] = models.xzh_article.objects.filter(user_id=user_id).count()  # 总发布篇数

        xzh_fugai_baobiao_objs = models.xzh_fugai_baobiao.objects.filter(user_id=user_id)
        if xzh_fugai_baobiao_objs:  # 已经存在信息
            xzh_fugai_baobiao_objs.update(**data)
        else:
            models.xzh_fugai_baobiao.objects.create(**data)

    response.code = 200
    response.msg = "初始化完成"
    return JsonResponse(response.__dict__)
