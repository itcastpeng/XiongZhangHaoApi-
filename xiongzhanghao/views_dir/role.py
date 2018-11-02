from xiongzhanghao import models
from xiongzhanghao.publicFunc import Response
from xiongzhanghao.publicFunc import account
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from xiongzhanghao.publicFunc.condition_com import conditionCom
from xiongzhanghao.forms.role import AddForm, UpdateForm, SelectForm
from xiongzhanghao.views_dir.permissions import init_data
import json


# cerf  token验证 用户展示模块
@csrf_exempt
@account.is_token(models.xzh_userprofile)
def role(request):
    response = Response.ResponseObj()
    if request.method == "GET":
        forms_obj = SelectForm(request.GET)
        if forms_obj.is_valid():
            current_page = forms_obj.cleaned_data['current_page']
            length = forms_obj.cleaned_data['length']
            print('forms_obj.cleaned_data -->', forms_obj.cleaned_data)
            order = request.GET.get('order', '-create_date')
            field_dict = {
                'id': '',
                'name': '__contains',
                'create_date': '',
                'oper_user__username': '__contains',
            }
            q = conditionCom(request, field_dict)
            print('q -->', q)
            objs = models.xzh_role.objects.filter(q).order_by(order)
            count = objs.count()

            if length != 0:
                start_line = (current_page - 1) * length
                stop_line = start_line + length
                objs = objs[start_line: stop_line]

            # 返回的数据
            ret_data = []

            for obj in objs:
                # 获取选中的id，然后组合成前端能用的数据
                permissionsList = []
                permissionsData = []
                if obj.permissions:
                    permissionsList = [i['id'] for i in obj.permissions.values('id')]
                    permissionsData = init_data(selected_list=permissionsList)

                #  如果有oper_user字段 等于本身名字
                if obj.oper_user:
                    oper_user_username = obj.oper_user.username
                else:
                    oper_user_username = ''
                # print('oper_user_username -->', oper_user_username)
                #  将查询出来的数据 加入列表
                ret_data.append({
                    'id': obj.id,
                    'name': obj.name,
                    'create_date': obj.create_date.strftime('%Y-%m-%d %H:%M:%S'),
                    'oper_user__username': oper_user_username,
                    'permissionsData': json.dumps(permissionsData)
                })
            #  查询成功 返回200 状态码
            response.code = 200
            response.msg = '查询成功'
            response.data = {
                'ret_data': ret_data,
                'data_count': count,
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
def role_oper(request, oper_type, o_id):
    response = Response.ResponseObj()
    if request.method == "POST":
        if oper_type == "add":
            form_data = {
                'oper_user_id': request.GET.get('user_id'),
                'name': request.POST.get('name'),
                'permissionsList': request.POST.get('permissionsList'),
            }
            #  创建 form验证 实例（参数默认转成字典）
            forms_obj = AddForm(form_data)
            if forms_obj.is_valid():
                print("验证通过")
                # print(forms_obj.cleaned_data)
                #  添加数据库
                # print('forms_obj.cleaned_data-->',forms_obj.cleaned_data)
                print({
                    'name': forms_obj.cleaned_data.get('name'),
                    'oper_user_id': forms_obj.cleaned_data.get('oper_user_id'),
                })
                obj = models.xzh_role.objects.create(**{
                    'name': forms_obj.cleaned_data.get('name'),
                    'oper_user_id': forms_obj.cleaned_data.get('oper_user_id'),
                })

                permissionsList = forms_obj.cleaned_data.get('permissionsList')
                print('permissionsList -->', permissionsList)
                obj.permissions = permissionsList
                obj.save()
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
                'name': request.POST.get('name'),
                'permissionsList': request.POST.get('permissionsList'),
            }

            forms_obj = UpdateForm(form_data)
            if forms_obj.is_valid():
                print("验证通过")
                print(forms_obj.cleaned_data)
                o_id = forms_obj.cleaned_data['o_id']
                name = forms_obj.cleaned_data['name']
                permissionsList = forms_obj.cleaned_data['permissionsList']
                #  查询数据库  用户id
                objs = models.xzh_role.objects.filter(
                    id=o_id
                )
                #  更新 数据
                if objs:
                    objs.update(
                        name=name
                    )

                    objs[0].permissions = permissionsList

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
        objs = models.xzh_role.objects.filter(id=o_id)
        if objs:
            obj = objs[0]
            if obj.xzh_userprofile_set.all().count() > 0:
                response.code = 304
                response.msg = '含有子级数据,请先删除或转移子级数据'
            else:
                objs.delete()
                response.code = 200
                response.msg = "删除成功"
        else:
            response.code = 302
            response.msg = '删除ID不存在'

    else:
        # 获取角色对应的权限
        if oper_type == "get_rules":
            objs = models.xzh_role.objects.filter(id=o_id)
            if objs:
                obj = objs[0]
                rules_list = [i['name'] for i in obj.permissions.values('name')]
                print('dataList -->', rules_list)
                response.data = {
                    'rules_list': rules_list
                }

                response.code = 200
                response.msg = "查询成功"
        else:
            response.code = 402
            response.msg = "请求异常"

    return JsonResponse(response.__dict__)
