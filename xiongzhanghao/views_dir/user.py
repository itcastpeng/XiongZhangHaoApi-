from django.shortcuts import render, HttpResponse
from xiongzhanghao import models
from xiongzhanghao.publicFunc import Response
from xiongzhanghao.publicFunc import account
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from xiongzhanghao.publicFunc.condition_com import conditionCom
from xiongzhanghao.forms.user import AddForm, UpdateForm, SelectForm
from django.db.models import Q
from backend.articlePublish import DeDe
import json



def init_data(request):
    response = Response.ResponseObj()
    forms_obj = SelectForm(request.GET)
    if forms_obj.is_valid():
        current_page = forms_obj.cleaned_data['current_page']
        length = forms_obj.cleaned_data['length']
        print('forms_obj.cleaned_data -->', forms_obj.cleaned_data)
        order = request.GET.get('order', '-create_date')
        field_dict = {
            'id': '',
            'role_id': '',
            'name': '__contains',
            'create_date': '',
            'oper_user__username': '__contains',
            'is_debug': '',
        }
        q = conditionCom(request, field_dict)

        print('q -->', q)
        objs = models.xzh_userprofile.objects.select_related('role').filter(q).order_by(order)
        count = objs.count()

        if length != 0:
            start_line = (current_page - 1) * length
            stop_line = start_line + length
            objs = objs[start_line: stop_line]

        # 返回的数据
        ret_data = []

        for obj in objs:
            #  如果有oper_user字段 等于本身名字
            if obj.oper_user:
                oper_user_username = obj.oper_user.username
            else:
                oper_user_username = ''
            # print('oper_user_username -->', oper_user_username)
            role_name = ''
            role_id = ''
            if obj.role:
                role_id = obj.role_id
                role_name = obj.role.name

            #  将查询出来的数据 加入列表
            ret_data.append({
                'id': obj.id,
                'username': obj.username,
                'get_status_display': obj.get_status_display(),
                'status': obj.status,
                'role_id': role_id,
                'role_name': role_name,
                'website_backstage_id': obj.website_backstage,
                'website_backstage_name': obj.get_website_backstage_display(),
                'website_backstage_username': obj.website_backstage_username,
                'website_backstage_password': obj.website_backstage_password,
                'create_date': obj.create_date.strftime('%Y-%m-%d %H:%M:%S'),
                'oper_user__username': oper_user_username,
                'website_backstage_url':obj.website_backstage_url
            })
        #  查询成功 返回200 状态码
        response.code = 200
        response.msg = '查询成功'
        response.data = {
            'ret_data': ret_data,
            'data_count': count,
            'website_backstage_choices': models.xzh_userprofile.website_backstage_choices,
        }
    else:
        response.code = 301
        response.data = json.loads(forms_obj.errors.as_json())
    return response

# cerf  token验证 用户展示模块
@csrf_exempt
@account.is_token(models.xzh_userprofile)
def user(request):
    response = Response.ResponseObj()
    if request.method == "GET":
        response = init_data(request)
    else:
        response.code = 402
        response.msg = '请求异常'
    return JsonResponse(response.__dict__)


#  增删改
#  csrf  token验证
@csrf_exempt
@account.is_token(models.xzh_userprofile)
def user_oper(request, oper_type, o_id):
    response = Response.ResponseObj()
    if request.method == "POST":
        if oper_type == "add":
            form_data = {
                'oper_user_id': request.GET.get('user_id'),
                'username': request.POST.get('username'),
                'role_id': request.POST.get('role_id'),
                'password': request.POST.get('password'),
                'website_backstage': request.POST.get('website_backstage'),
                'website_backstage_username': request.POST.get('website_backstage_username'),
                'website_backstage_url': request.POST.get('website_backstage_url'),
                'website_backstage_password': request.POST.get('website_backstage_password'),
            }

            print('form_data----->',form_data)
            #  创建 form验证 实例（参数默认转成字典）
            forms_obj = AddForm(form_data)
            if forms_obj.is_valid():
                print("验证通过")
                # print(forms_obj.cleaned_data)
                #  添加数据库
                # print('forms_obj.cleaned_data-->',forms_obj.cleaned_data)
                models.xzh_userprofile.objects.create(**forms_obj.cleaned_data)
                response.code = 200
                response.msg = "添加成功"
            else:
                print("验证不通过")
                # print(forms_obj.errors)
                response.code = 301
                # print(forms_obj.errors.as_json())
                response.msg = json.loads(forms_obj.errors.as_json())

        elif oper_type == "update":
            # 获取需要修改的信息
            form_data = {
                'o_id': o_id,
                'username': request.POST.get('username'),
                'role_id': request.POST.get('role_id'),
                # 'company_id': request.POST.get('company_id'),
                'website_backstage': request.POST.get('website_backstage'),
                'website_backstage_url': request.POST.get('website_backstage_url'),
                'website_backstage_username': request.POST.get('website_backstage_username'),
                'website_backstage_password': request.POST.get('website_backstage_password'),
            }

            forms_obj = UpdateForm(form_data)
            if forms_obj.is_valid():
                print("验证通过")
                print(forms_obj.cleaned_data)
                o_id = forms_obj.cleaned_data['o_id']
                username = forms_obj.cleaned_data['username']
                role_id = forms_obj.cleaned_data['role_id']
                # company_id = forms_obj.cleaned_data['company_id']
                #  查询数据库  用户id
                objs = models.xzh_userprofile.objects.filter(
                    id=o_id
                )
                #  更新 数据
                if objs:
                    objs.update(
                        username=username,
                        role_id=role_id,
                        # company_id=company_id
                    )

                    response.code = 200
                    response.msg = "修改成功"
                else:
                    response.code = 303
                    response.msg = '修改ID不存在'

            else:
                print("验证不通过")
                # print(forms_obj.errors)
                response.code = 301
                # print(forms_obj.errors.as_json())
                #  字符串转换 json 字符串
                response.msg = json.loads(forms_obj.errors.as_json())

        elif oper_type == "delete":
            # 删除 ID
            # company_id = request.GET.get('company_id')
            objs = models.xzh_userprofile.objects.filter(id=o_id)
            if objs:
                objs.delete()
                response.code = 200
                response.msg = "删除成功"
            else:
                response.code = 302
                response.msg = '删除ID不存在'

        elif oper_type == "update_status":
            status = request.POST.get('status')
            company_id = request.GET.get('company_id')
            print('status -->', status)
            objs = models.xzh_userprofile.objects.filter(id=o_id, company_id=company_id)
            if objs:
                objs.update(status=status)
                response.code = 200
                response.msg = "状态修改成功"
            else:
                response.code = 301
                response.msg = "用户ID不存在"

    else:
        response.code = 402
        response.msg = "请求异常"

    return JsonResponse(response.__dict__)

# 供脚本查询 用户
@csrf_exempt
def script_user(request):
    response = Response.ResponseObj()
    if request.method == "GET":
        response = init_data(request)
    else:
        response.code = 402
        response.msg = '请求异常'
    return JsonResponse(response.__dict__)

# 登录
def login_website_backstage(user_id, domain, home_path, userid, pwd, flag_num):
    # 创建dede 实例及 登录
    DeDeObj = DeDe(domain=domain, home_path=home_path)
    cookies = DeDeObj.login(userid, pwd)
    if flag_num <= 5:
        print('cookies--------> ', cookies, len(cookies), type(cookies))
        if len(cookies) > 1:
            class_data = DeDeObj.getClassInfo()
            models.xzh_userprofile.objects.filter(id=user_id).update(
                column_all=str(class_data),
                is_debug=1,
                cookies=cookies
            )
            print('class_data-------> ', class_data)
            return 200
        else:
            flag_num += 1
            login_website_backstage(user_id, domain, home_path, userid, pwd, flag_num)
    else:   # 如果登录超过五次 则登录失败
        print('===========登录失败')
        return 500

# 定时刷新 调试用户 获取cookies和所有栏目
@csrf_exempt
def getTheDebugUser(request):
    response = Response.ResponseObj()
    objs = models.xzh_userprofile.objects.filter(status=1, is_debug=0)
    if objs:
        for obj in objs:
            website_backstage_url = obj.website_backstage_url
            home_path = website_backstage_url.split('/')[-1]
            domain = website_backstage_url.split(website_backstage_url.split('/')[-1])[0]
            userid = obj.website_backstage_username
            pwd = obj.website_backstage_password
            flag_num = 1# 判断登录几次 大于五次不登录
            login_website_backstage(obj.id, domain, home_path, userid, pwd, flag_num)
        response.code = 200
    else:
        response.code = 200
        response.msg = '无数据'
    return JsonResponse(response.__dict__)
