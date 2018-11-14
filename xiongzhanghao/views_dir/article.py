from xiongzhanghao import models
from xiongzhanghao.publicFunc import Response
from xiongzhanghao.publicFunc import account
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from xiongzhanghao.publicFunc.condition_com import conditionCom
from xiongzhanghao.forms.article import AddForm, UpdateForm, SelectForm
import json, datetime, requests
from urllib.parse import urlparse
from backend.articlePublish import DeDe
from XiongZhangHaoApi_celery.tasks import celeryGetDebugUser


# from xiongzhanghao.views_dir.user import objLogin


# cerf  token验证 用户展示模块
@csrf_exempt
@account.is_token(models.xzh_userprofile)
def article(request):
    response = Response.ResponseObj()
    if request.method == "GET":
        forms_obj = SelectForm(request.GET)
        if forms_obj.is_valid():
            current_page = forms_obj.cleaned_data['current_page']
            length = forms_obj.cleaned_data['length']
            print('forms_obj.cleaned_data -->', forms_obj.cleaned_data)
            order = request.GET.get('order', '-create_date')
            user_id = request.GET.get('user_id')
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
            objs = models.xzh_article.objects.select_related('user').filter(q).order_by(order)
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
                column = eval(obj.column_id) if obj.column_id else {}
                print('column============> ', column)
                back_url = obj.back_url if obj.back_url else ''

                send_time = obj.send_time.strftime('%Y-%m-%d %H:%M:%S') if obj.send_time else ''
                ret_data.append({
                    'id': obj.id,
                    'title':obj.title,
                    'summary':obj.summary,
                    'content':obj.content,
                    'column_id':column.get('Id'),
                    'column_name':column.get('name'),
                    'create_date':obj.create_date.strftime('%Y-%m-%d %H:%M:%S'),
                    'user_id':obj.user.id,
                    'user_name':obj.user.username,
                    'belongToUser_id':obj.belongToUser_id,
                    'belongToUser_name': obj.belongToUser.username,
                    'article_status': obj.get_article_status_display(),
                    'note_content':obj.note_content,
                    'back_url':back_url,
                    'send_time':send_time,
                    'is_audit':obj.is_audit
                })
            #  查询成功 返回200 状态码
            response.code = 200
            response.msg = '查询成功'
            response.data = {
                'ret_data': ret_data,
                'data_count': count,
                'article_status':models.xzh_article.article_status_choices,
            }
        else:
            response.code = 402
            response.msg = "请求异常"
            response.data = json.loads(forms_obj.errors.as_json())
    return JsonResponse(response.__dict__)


#  增删改
#  csrf  token验证
@csrf_exempt
@account.is_token(models.xzh_userprofile)
def article_oper(request, oper_type, o_id):
    response = Response.ResponseObj()
    if request.method == "POST":
        form_data = {
            'user_id': request.GET.get('user_id'),
            'title': request.POST.get('title'),
            'summary': request.POST.get('summary'),
            'content': request.POST.get('content'),
            'column_id': request.POST.get('column_id'),
            'create_date': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'belongToUser_id':request.POST.get('belongToUser_id'),
            'send_time': request.POST.get('send_time')
        }
        if oper_type == "add":
            #  创建 form验证 实例（参数默认转成字典）
            forms_obj = AddForm(form_data)
            if forms_obj.is_valid():
                print("验证通过")
                print("forms_obj.data.get('column_id')========> ",forms_obj.cleaned_data.get('column_id'))
                models.xzh_article.objects.create(**forms_obj.cleaned_data)
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
                objs = models.xzh_article.objects.filter(
                    id=o_id
                )
                #  更新 数据
                if objs:
                    print('objs[0].article_status===============> ',objs[0].article_status)
                    if objs[0].article_status != 2:
                        objForm = forms_obj.cleaned_data
                        send_time = objForm.get('send_time')
                        objs.update(
                            user_id =objForm.get('user_id'),
                            title = objForm.get('title'),
                            summary = objForm.get('summary'),
                            content = objForm.get('content'),
                            belongToUser_id = objForm.get('belongToUser_id'),
                            column_id = objForm.get('column_id')
                        )
                        if send_time:
                            objs.update(send_time=send_time)

                        response.code = 200
                        response.msg = "修改成功"
                    else:
                        response.code = 301
                        response.msg = '发布成功, 不可修改'
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
            company_id = request.GET.get('company_id')
            objs = models.xzh_article.objects.filter(id=o_id)
            if objs:
                objs.delete()
                response.code = 200
                response.msg = "删除成功"
            else:
                response.code = 302
                response.msg = '删除ID不存在'

        elif oper_type == 'redistribution':
            objs = models.xzh_article.objects.filter(id=o_id)
            if objs[0].article_status != 2:
                objs.update(article_status=1)
            response.code = 200
            response.msg = '重新发布成功'

    else:
        response.code = 402
        response.msg = "请求异常"

    return JsonResponse(response.__dict__)



# 更改状态和备注
def models_article(class_data, user_id):
    code = class_data.get('code')
    huilian = class_data.get('huilian')
    objs = models.xzh_article.objects.filter(id=user_id)
    if code == 200:                 # 发布成功
        objs.update(
            article_status=2,
            back_url=huilian,
            note_content='无',

        )
    elif code == 300:               # 标题重复
        objs.update(
            article_status=3,
            note_content='标题重复'
        )
    elif code == 302:               # 登录失败
        objs.update(
            article_status=3,
            note_content='登录失败'
        )
    elif code == 305:  # 登录失败
        objs.update(
            article_status=3,
            note_content='模板文件不存在, 请选择子级菜单'
        )
    else:                           # 发布失败
        objs.update(
            article_status=3,
            note_content='发布失败'
        )



def send_article(obj, article_data):
    website_backstage_url = obj.belongToUser.website_backstage_url.strip()
    url = urlparse(website_backstage_url)
    domain = 'http://' + url.hostname + '/'
    home_path = website_backstage_url.split(domain)[1].replace('/', '')
    DeDeObj = DeDe(domain=domain, home_path=home_path)
    if obj.belongToUser.cookies:
        try:
            print('-=========================================================cookie', obj.belongToUser.cookies)
            class_data = DeDeObj.sendArticle(article_data, objCookies=eval(obj.belongToUser.cookies))
            models_article(class_data, obj.id)
        except Exception as e:
            print('错误-----------错误--------------------> ', e)
            celeryGetDebugUser.delay(obj.belongToUser_id)
            # url = 'http://127.0.0.1:8003/getTheDebugUser?userLoginId={}'.format(obj.belongToUser_id)
            # requests.get(url)
            class_data = DeDeObj.sendArticle(article_data)
            models_article(class_data, obj.id)
    else:
        celeryGetDebugUser.delay(obj.belongToUser_id)
        # url = 'http://127.0.0.1:8003/getTheDebugUser?userLoginId={}'.format(obj.belongToUser_id)
        # requests.get(url)
        class_data = DeDeObj.sendArticle(article_data)
        models_article(class_data, obj.id)

# 脚本运行 查询未发布文章发布 修改文章状态
@csrf_exempt
def script_oper(request):
    response = Response.ResponseObj()
    objs = models.xzh_article.objects.select_related('belongToUser').filter(
        article_status=1,
        belongToUser__is_debug=1
    ).order_by('create_date')
    for obj in objs:
        title = obj.title.encode('utf8')
        summary = obj.summary.encode('utf8')
        content = obj.content.encode('utf8')
        if 'http://m.chyy120.com/netadmin' in obj.belongToUser.website_backstage_url:
            title = obj.title.encode('gbk')
            summary = obj.summary.encode('gbk')
            content = obj.content.encode('gbk')
        if obj.title and obj.column_id and obj.summary and obj.content:
            article_data = {
                "channelid": "1",  # 表示普通文章
                "dopost": "save",  # 隐藏写死属性
                "title": title,  # 文章标题
                "weight": "1033",  # 权重
                "typeid": eval(obj.column_id).get('Id'),  # 栏目id
                "autokey": "1",  # 关键字自动获取
                "description": summary,  # 描述
                "remote": "1",  # 下载远程图片和资源
                "autolitpic": "1",  # 提取第一个图片为缩略图
                "sptype": "hand",  # 分页方式 手动
                "spsize": "5",
                "body": content,
                "notpost": "0",
                "click": "63",
                "sortup": "0",
                "arcrank": "0",
                "money": "0",
                "pubdate": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "ishtml": 1,
                "imageField.x": "30",
                "imageField.y": "12"
            }
            if obj.send_time:  # 如果有定时
                now_date = datetime.datetime.now()
                if obj.send_time <= now_date:
                    print('=================定时发送文章 ----------- ', obj.send_time)
                    send_article(obj, article_data)
            else:               # 没有定时
                send_article(obj, article_data)
    response.code = 200
    return JsonResponse(response.__dict__)