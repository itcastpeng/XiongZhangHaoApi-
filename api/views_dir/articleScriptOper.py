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
from urllib import parse
from django.db.models import Q


@csrf_exempt
@account.is_token(models.xzh_userprofile)
def articleScriptOper(request, oper_type):
    response = Response.ResponseObj()
    # 发送文章
    if oper_type == 'sendArticle':
        print('==============================sendArticle==sendArticle')
        now_date = datetime.datetime.now()
        q = Q()
        q.add(Q(send_time__lte=now_date) | Q(send_time__isnull=True), Q.AND)
        objs = models.xzh_article.objects.select_related('belongToUser').filter(q).filter(
            article_status=1,
            belongToUser__is_debug=1
        ).order_by('create_date')
        print('objs========================> ',objs)
        if objs:
            obj = objs[0]
            if obj.title and obj.column_id and obj.summary and obj.content:
                # models.xzh_article.objects.filter(id=obj.id).update(
                #     articlePublishedDate=datetime.datetime.now()
                # )
                result_data = {
                    'website_backstage':objs[0].belongToUser.website_backstage,
                    'website_backstage_url': objs[0].belongToUser.website_backstage_url.strip(),
                    'website_backstage_username': objs[0].belongToUser.website_backstage_username,
                    'website_backstage_password': objs[0].belongToUser.website_backstage_password,
                    'cookies':objs[0].belongToUser.cookies,
                    'title': objs[0].title,
                    'summary': objs[0].summary,
                    'content': objs[0].content,
                    'typeid': eval(objs[0].column_id).get('Id'), # 此处I 为大写请勿更改
                    'o_id':objs[0].id
                }
                if obj.articlePicName:
                    result_data['picname'] = obj.articlePicName

                response.data = result_data
        response.code = 200


    # 更改状态和备注
    elif oper_type == 'sendArticleModels':
        resultData = request.POST.get('resultData')
        o_id = request.POST.get('o_id')
        print('====================', resultData)
        print(request.POST)
        print(request.GET)
        if resultData:
            resultData = eval(resultData)
            code = int(resultData.get('code'))
            objs = models.xzh_article.objects.filter(id=o_id)
            website_backstage = objs[0].belongToUser.website_backstage
            print('code==========> ',code)
            print("=============resultData.get('huilian')=======> ",resultData.get('huilian'))
            print("=============resultData.get('aid')=======> ",resultData.get('aid'))
            article_status = 3
            note_content = ''
            huilian = ''
            aid = 0
            is_audit = False
            if code == 200:  # 发布成功
                article_status = 2
                if int(website_backstage) == 2 or int(website_backstage) == 3:
                    article_status = 4        # 如果是 pcv9 或 FTP 不需要审核
                    is_audit=1

                huilian = resultData.get('huilian')
                aid = resultData.get('aid')

            elif code == 300:  # 标题重复
                note_content='标题重复'

            elif code == 305:  # 登录失败
                note_content='模板文件不存在, 请选择子级菜单'

            elif code == 301:
                note_content = '客户网站标题未查到, 请验证'

            else:  # 发布失败
                note_content = '发布失败'
            print('note_content============> ', note_content)
            objs.update(
                article_status=article_status,
                back_url=huilian,
                aid=aid,
                note_content=note_content,
                is_audit=is_audit
            )

    # 判断文章是否审核
    elif oper_type == 'refreshAudit':
        objs = models.xzh_article.objects.filter(article_status=2, is_audit=0, aid__isnull=False, belongToUser__website_backstage=1)
        if objs:
            obj = objs[0]
            print('定时刷新文章是否审核----------------->', obj.id)
            result_data = {
                'website_backstage_url': obj.belongToUser.website_backstage_url,
                'website_backstage_username': obj.belongToUser.website_backstage_username,
                'website_backstage_password': obj.belongToUser.website_backstage_password,
                'cookies': obj.belongToUser.cookies,
                'o_id': obj.id,
                'aid': obj.aid,
                'userType': obj.belongToUser.userType,
            }
            response.data = result_data
        response.code = 200


    # 文章审核更新数据库
    elif oper_type == 'refreshAuditModel':
        o_id = request.POST.get('o_id')
        status = request.POST.get('status')
        userType = request.POST.get('userType')
        article_status = 2
        if userType and o_id:
            if status == 'True':
                print('=================')
                article_status = 4
                if int(userType) == 2:  # 判断是否为特殊用户
                    article_status = 6
        print('status, o_id============> ', status, o_id, 'userType:', userType , 'article_status: ', article_status)
        models.xzh_article.objects.filter(id=o_id).update(
            is_audit=status,
            article_status=article_status
        )
        response.code = 200


    # 提交文章到熊掌号
    elif oper_type == 'submitXiongZhangHao':
        print('===')
        objs = models.xzh_article.objects.filter(is_audit=True, article_status=4)
        note_content = ''
        id_list = []
        for obj in objs:
            id_list.append(obj.id) if obj.id not in id_list else id_list

            appid = obj.belongToUser.website_backstage_appid
            token = obj.belongToUser.website_backstage_token
            print('appid, token------------------> ',appid, token)
            if obj.back_url:
                if token and appid:
                    submitUrl = 'http://data.zz.baidu.com/urls?appid={appid}&token={token}&type=realtime'.format(
                        appid=appid, token=token)
                    ret = requests.post(submitUrl, data=obj.back_url)
                    print('ret.text------------------->', ret.text)
                    if json.loads(ret.text).get('error'):
                        note_content = json.loads(ret.text).get('message')
                    elif json.loads(ret.text).get('not_same_site'):
                        print('======================================不是本站url或未处理的url============================')
                        note_content = '不是本站url或未处理的url'
                    elif json.loads(ret.text).get('not_valid'):
                        print('==---------------------------不合法的url=-----------------------------')
                        note_content = '不合法的url'
                    else:
                        note_content = ''
                        obj.article_status = 5
                else:
                    note_content = 'appid 或 token 有问题, 建议重新获取token'
                obj.note_content = note_content
                obj.save()
                continue
        response.code = 200


    else:
        response.code = 402
        response.msg = '请求失败'

    return JsonResponse(response.__dict__)
