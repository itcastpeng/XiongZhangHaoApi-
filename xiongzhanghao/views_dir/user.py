from django.shortcuts import render, HttpResponse
from xiongzhanghao import models
from xiongzhanghao.publicFunc import Response
from xiongzhanghao.publicFunc import account
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from xiongzhanghao.publicFunc.condition_com import conditionCom
from xiongzhanghao.forms.user import AddForm, UpdateForm, SelectForm, AdminAddForm, AdminUpdateForm
from django.db.models import Q
from backend.articlePublish import DeDe
from urllib.parse import urlparse
import json, requests, datetime, time


# cerf  token验证 用户展示模块
@csrf_exempt
@account.is_token(models.xzh_userprofile)
def user(request):
    response = Response.ResponseObj()
    forms_obj = SelectForm(request.GET)
    if forms_obj.is_valid():
        user_id = request.GET.get('user_id')
        userObj = models.xzh_userprofile.objects.get(id=user_id)
        current_page = forms_obj.cleaned_data['current_page']
        length = forms_obj.cleaned_data['length']
        print('forms_obj.cleaned_data -->', forms_obj.cleaned_data)
        order = request.GET.get('order', '-create_date')
        field_dict = {
            'id': '',
            'role_id': '',
            # 'username': '__contains',
            'create_date': '',
            'oper_user__username': '__contains',
            'is_debug': 'bool',
        }
        user_id = request.GET.get('user_id')
        print('user_id-------------------> ', user_id)
        userObjs = models.xzh_userprofile.objects.filter(id=user_id)
        if userObjs:
            userObj = userObjs[0]
            userObjRole = userObj.role_id


            q = conditionCom(request, field_dict)
            role_id = request.GET.get('role_id')
            if role_id:
                q.add(Q(role_id=role_id), Q.AND)
            print('q -->', q)
            username = request.GET.get('username')
            if username:
                q.add(Q(username__contains=username), Q.AND)
            if int(userObjRole) == 61:
                q.add(Q(id=user_id), Q.AND)

            user_objs = models.xzh_userprofile.objects.select_related('role').filter(q)
            if userObj.role_id == 64:
                objs = user_objs.order_by(order)
            elif userObj.role_id == 66:
                objs = user_objs.order_by(order).exclude(role_id=64)
            else:
                objs = user_objs.order_by(order).exclude(role_id__in=[64,66])
            count = objs.count()

            if length != 0:
                start_line = (current_page - 1) * length
                stop_line = start_line + length
                objs = objs[start_line: stop_line]

            # 返回的数据
            ret_data = []
            index = 0

            now = datetime.date.today()
            print('now-----------> ',now)
            for obj in objs:
                billingObjs = obj.user_biling_belong_user.order_by('-stop_time')[:1]
                dueTime = '~'
                if billingObjs:
                    stop_time = billingObjs[0].stop_time  # 用户到期时间
                    if stop_time > now:
                        dueTime = (stop_time - now).days
                    elif stop_time == now:
                        dueTime = 0     # 今天到期

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

                is_debug = '已调试' if obj.is_debug else '未调试'

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
                    'website_backstage_url': obj.website_backstage_url,
                    'is_debug': is_debug,
                    'website_backstage_token': obj.website_backstage_token,
                    'website_backstage_appid': obj.website_backstage_appid,
                    'xiongZhangHaoIndex': obj.xiongZhangHaoIndex,
                    'secondaryDomainName': obj.secondaryDomainName,
                    'xiong_zhang_hao_user': obj.xiong_zhang_hao_user,
                    'xiong_zhang_hao_pwd': obj.xiong_zhang_hao_pwd,
                    'fans_search_keyword': obj.fans_search_keyword,
                    'index':index,
                    'dueTime':dueTime,
                })
                index += 1

            #  查询成功 返回200 状态码
            response.code = 200
            response.msg = '查询成功'
            response.data = {
                'ret_data': ret_data,
                'data_count': count,
                'website_backstage_choices': models.xzh_userprofile.website_backstage_choices,
                'billing_cycle_choices': models.user_billing.billing_cycle_choices,
            }
        else:
            response.code = 500
            response.msg = '非法用户'
    else:
        response.code = 301
        response.msg = json.loads(forms_obj.errors.as_json())
    return JsonResponse(response.__dict__)


# 修改密码
@csrf_exempt
@account.is_token(models.xzh_userprofile)
def updatePwd(request):
    response = Response.ResponseObj()
    user_id = request.GET.get('user_id')
    user_objs = models.xzh_userprofile.objects.filter(id=user_id)
    if user_objs:
        user_obj = user_objs[0]
        user_obj_role = user_obj.role_id

        oldPwd = request.POST.get('oldPwd')
        newPwd = request.POST.get('newPwd')
        if newPwd and oldPwd:
            print('oldPwd-------> ',oldPwd)
            oldPwd = account.str_encrypt(oldPwd) # 加密 密码
            if oldPwd == user_obj.password:
                newPwd = account.str_encrypt(newPwd)
                token = account.get_token(newPwd + str(int(time.time()) * 1000)) #  token
                user_objs.update(password=newPwd, token=token)
                response.code = 200
                response.msg = '修改成功'
            else:
                response.code = 301
                response.msg = '旧密码验证错误'
        else:
            response.code = 301
            response.msg = '参数错误'
    else:
        response.code = 500
        response.msg = '非法请求'

    return JsonResponse(response.__dict__)
#  增删改
#  csrf  token验证
@csrf_exempt
@account.is_token(models.xzh_userprofile)
def user_oper(request, oper_type, o_id):
    response = Response.ResponseObj()
    user_id = request.GET.get('user_id')
    user_objs = models.xzh_userprofile.objects.filter(id=user_id)
    if user_objs:
        user_obj = user_objs[0]
        user_obj_role = user_obj.role_id
        if request.method == "POST":
            if int(user_obj_role) == 61:
                response.code = 301
                response.msg = '权限不足'
            else:
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
                        'website_backstage_token': request.POST.get('website_backstage_token'),
                        'website_backstage_appid': request.POST.get('website_backstage_appid'),
                        'xiongZhangHaoIndex': request.POST.get('xiongZhangHaoIndex'),
                        'secondaryDomainName': request.POST.get('secondaryDomainName'),
                        'xiong_zhang_hao_user': request.POST.get('xiong_zhang_hao_user'),
                        'xiong_zhang_hao_pwd': request.POST.get('xiong_zhang_hao_pwd'),
                        'fans_search_keyword': request.POST.get('fans_search_keyword'),
                    }
                    print('form_data----->',form_data)
                    #  创建 form验证 实例（参数默认转成字典）

                    if int(form_data.get('role_id')) == 64 or int(form_data.get('role_id')) == 66:
                        forms_obj = AdminAddForm(form_data)
                    else:
                        forms_obj = AddForm(form_data)
                    if forms_obj.is_valid():
                        print("验证通过")
                        models.xzh_userprofile.objects.create(**forms_obj.cleaned_data)
                        # print(forms_obj.cleaned_data)
                        #  添加数据库

                        # url = 'http://xiongzhanghao.zhugeyingxiao.com:8003/getTheDebugUser'
                        # requests.get(url)

                        # celeryGetDebugUser.delay()  # 异步调用
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
                        'website_backstage': request.POST.get('website_backstage'),
                        'website_backstage_url': request.POST.get('website_backstage_url'),
                        'website_backstage_username': request.POST.get('website_backstage_username'),
                        'website_backstage_password': request.POST.get('website_backstage_password'),
                        'website_backstage_token': request.POST.get('website_backstage_token'),
                        'website_backstage_appid': request.POST.get('website_backstage_appid'),
                        'xiongZhangHaoIndex': request.POST.get('xiongZhangHaoIndex'),
                        'xiong_zhang_hao_user': request.POST.get('xiong_zhang_hao_user'),
                        'xiong_zhang_hao_pwd': request.POST.get('xiong_zhang_hao_pwd'),
                        'fans_search_keyword': request.POST.get('fans_search_keyword'),
                    }
                    flag = False
                    if int(form_data.get('role_id')) == 64 or int(form_data.get('role_id')) ==  66:
                        forms_obj = AdminUpdateForm(form_data)
                    else:
                        flag = True
                        forms_obj = UpdateForm(form_data)
                    if forms_obj.is_valid():
                        print("验证通过")
                        print(forms_obj.cleaned_data)
                        o_id = forms_obj.cleaned_data['o_id']
                        username = forms_obj.cleaned_data['username']
                        role_id = forms_obj.cleaned_data['role_id']
                        objs = models.xzh_userprofile.objects.filter(
                            id=o_id
                        )
                        #  更新 数据
                        if objs:
                            print('===========================================')
                            if flag:
                                website_backstage = forms_obj.cleaned_data['website_backstage']
                                website_backstage_url = forms_obj.cleaned_data['website_backstage_url']
                                website_backstage_username = forms_obj.cleaned_data['website_backstage_username']
                                website_backstage_password = forms_obj.cleaned_data['website_backstage_password']
                                website_backstage_token = forms_obj.cleaned_data['website_backstage_token']
                                website_backstage_appid = forms_obj.cleaned_data['website_backstage_appid']
                                xiongZhangHaoIndex = forms_obj.cleaned_data['xiongZhangHaoIndex']
                                xiong_zhang_hao_pwd = forms_obj.cleaned_data['xiong_zhang_hao_pwd']
                                xiong_zhang_hao_user = forms_obj.cleaned_data['xiong_zhang_hao_user']
                                fans_search_keyword = forms_obj.cleaned_data['fans_search_keyword']
                                print('website_backstage_token, website_backstage_appid---------------> ',website_backstage_token, website_backstage_appid)
                                #  查询数据库  用户id
                                objs.update(
                                    username=username,
                                    role_id=role_id,
                                    website_backstage=website_backstage,
                                    website_backstage_url=website_backstage_url,
                                    website_backstage_username=website_backstage_username,
                                    website_backstage_password=website_backstage_password,
                                    website_backstage_appid=website_backstage_appid,
                                    website_backstage_token=website_backstage_token,
                                    xiongZhangHaoIndex=xiongZhangHaoIndex,
                                    xiong_zhang_hao_user=xiong_zhang_hao_user,
                                    xiong_zhang_hao_pwd=xiong_zhang_hao_pwd,
                                    fans_search_keyword=fans_search_keyword,
                                )
                            else:
                                objs.update(
                                    username=username,
                                    role_id=role_id,
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

                # 删除 用户
                elif oper_type == "delete":
                    if o_id == user_id:
                        response.code = 301
                        response.msg = '不能删除自己'
                    elif int(o_id) == 54:
                        response.code = 301
                        response.msg = '不能删除该用户'
                    else:
                        objs = models.xzh_userprofile.objects.get(id=o_id)
                        if objs:
                            userObjs = models.xzh_article.objects.filter(belongToUser_id=o_id)
                            if userObjs:
                                response.code = 301
                                response.msg = '含有文章子级,请先删除该用户文章'
                            else:
                                if objs.id == user_id:
                                    response.code = 301
                                    response.msg = '不可删除自己'
                                else:
                                    objs.delete()
                                    response.code = 200
                                    response.msg = "删除成功"
                        else:
                            response.code = 302
                            response.msg = '删除ID不存在'
                    response.data = {}

                # 启用 用户  ×
                elif oper_type == "update_status":
                    status = request.POST.get('status')
                    print('status -->', status)
                    objs = models.xzh_userprofile.objects.filter(id=o_id)
                    if objs:
                        objs.update(status=status)
                        response.code = 200
                        response.msg = "状态修改成功"
                    else:
                        response.code = 301
                        response.msg = "用户ID不存在"

                # 启用 用户
                elif oper_type == 'updateStatus':
                    userObj = models.xzh_userprofile.objects
                    objs = userObj.filter(id=user_id)
                    if objs and int(objs[0].role_id) in [64, 66]:
                        obj = userObj.filter(id=o_id)
                        print('obj.status==============> ',obj[0].status)
                        if int(obj[0].status) == 1:
                            status = 2
                        else:
                            status = 1
                        obj.update(status=status)
                        response.code = 200
                        response.msg = '修改成功'
                    else:
                        response.code = 301
                        response.msg = '该角色不可修改状态'


        else:
            # 查询该用户所有栏目
            if oper_type == 'getColumn':
                Id = request.GET.get('Id')
                obj = models.xzh_userprofile.objects.get(id=Id)
                response.code = 200
                response.msg = '查询成功'
                response.data = obj.column_all
                if not response.data:
                    response.data = json.dumps([])


            else:
                response.code = 402
                response.msg = "请求异常"
    else:
        response.code = 500
        response.msg = '非法用户'

    return JsonResponse(response.__dict__)














