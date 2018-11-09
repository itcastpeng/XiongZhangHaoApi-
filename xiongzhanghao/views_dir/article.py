from xiongzhanghao import models
from xiongzhanghao.publicFunc import Response
from xiongzhanghao.publicFunc import account
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from xiongzhanghao.publicFunc.condition_com import conditionCom
from xiongzhanghao.forms.article import AddForm, UpdateForm, SelectForm
import json, datetime
from django.db.models import Q
from backend.articlePublish import DeDe

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
                back_url = obj.back_url if obj.back_url else ''
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
                    'back_url':back_url
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
                    objForm = forms_obj.cleaned_data
                    objs.update(
                        user_id =objForm.get('user_id'),
                        title = objForm.get('title'),
                        summary = objForm.get('summary'),
                        content = objForm.get('content'),
                        belongToUser_id = objForm.get('belongToUser_id'),
                        column_id = objForm.get('column_id')
                    )

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
            company_id = request.GET.get('company_id')
            objs = models.xzh_article.objects.filter(id=o_id)
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




# 更改状态和备注
def models_article(class_data, user_id):
    code = class_data.get('code')
    huilian = class_data.get('huilian')
    objs = models.xzh_article.objects.filter(id=user_id)
    if code == 200:                 # 发布成功
        objs.update(
            article_status=2,
            back_url=huilian
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
    else:                           # 发布失败
        objs.update(
            article_status=3,
            note_content='发布失败'
        )


#  登录用户名 密码 发送文章
def send_article(data_dict, userid=None, pwd=None):
    flag_num = data_dict.get('flag_num')
    DeDeObj = data_dict.get('DeDeObj')
    article_data = data_dict.get('article_data')
    user_id = data_dict.get('user_id')
    if flag_num <= 5:
        cookies = DeDeObj.login(userid=userid, pwd=pwd)
        if len(cookies) > 1:
            class_data = DeDeObj.sendArticle(article_data)
            models_article(class_data, user_id)
        else:
            print('重新登录---------------重新登录')
            flag_num += 1
            send_article(data_dict, userid=userid, pwd=pwd)
    else:  # 如果登录超过五次 则登录失败
        print('===========登录失败')
        class_data = {
                    'huilian':'',
                     'code':302
                    }
        models_article(class_data, user_id)

# 判断 是否有 cookie  没有则 用户名 密码登录
def login_website_backstage(result_dict, userid=None, pwd=None, objCookies=None):
    domain = result_dict.get('domain')
    home_path = result_dict.get('home_path')
    user_id = result_dict.get('user_id')
    flag_num = result_dict.get('flag_num')
    article_data = result_dict.get('article_data')

    # 创建dede 实例及 登录
    DeDeObj = DeDe(domain, home_path)
    data_dict = {
        'DeDeObj':DeDeObj,
        'user_id':user_id,
        'flag_num':flag_num,
        'article_data':article_data,
    }
    if objCookies: # 有cookies 请求
        class_data = DeDeObj.sendArticle(article_data, objCookies=objCookies)
        models_article(class_data, user_id)
    else: # 用户名密码登录
        send_article(data_dict, userid=userid, pwd=pwd)


# 脚本运行 查询未发布文章发布 修改文章状态
@csrf_exempt
def script_oper(request):
    response = Response.ResponseObj()
    retData = []
    objs = models.xzh_article.objects.select_related('belongToUser').filter(
        article_status=1,
        belongToUser__status=1,
        belongToUser__is_debug=1
    ).order_by('create_date')
    for obj in objs:
        print('obj.id----------------> ',obj.id)
        if obj.belongToUser:
            website_backstage_url = obj.belongToUser.website_backstage_url
            website_backstage = obj.belongToUser.status
            userid = obj.belongToUser.website_backstage_username
            pwd = obj.belongToUser.website_backstage_password
            home_path = website_backstage_url.split('/')[-1]
            domain = website_backstage_url.split(website_backstage_url.split('/')[-1])[0]

            if obj.title and obj.column_id and obj.summary and obj.content:
                article_data = {
                    "channelid": "1",  # 表示普通文章
                    "dopost": "save",  # 隐藏写死属性
                    "title": obj.title,  # 文章标题
                    "weight": "1033",  # 权重
                    "typeid": obj.column_id,  # 栏目id
                    "autokey": "1",  # 关键字自动获取
                    "description": obj.summary,  # 描述
                    "remote": "1",  # 下载远程图片和资源
                    "autolitpic": "1",  # 提取第一个图片为缩略图
                    "sptype": "hand",  # 分页方式 手动
                    "spsize": "5",
                    "body": obj.content,
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
                flag_num = 1
                result_dict = {
                    'user_id':obj.id,
                    'flag_num':flag_num,
                    'article_data':article_data,
                    'domain':domain,
                    'home_path':home_path,
                }

                if obj.belongToUser.cookies:
                    objCookies = obj.belongToUser.cookies
                    print('objCookies--> ',objCookies)
                    try:
                        login_website_backstage(result_dict, objCookies=eval(objCookies))
                    except Exception as e:
                        print('报错-------------', e )
                        login_website_backstage(result_dict, userid=userid, pwd=pwd)
                else:
                    print('登录用户名')
                    login_website_backstage(result_dict, userid=userid, pwd=pwd)
            else:
                pass

    response.code = 200
    response.msg = '查询成功'
    response.data = retData
    return JsonResponse(response.__dict__)