from xiongzhanghao import models
from xiongzhanghao.publicFunc import Response
from xiongzhanghao.publicFunc import account
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from xiongzhanghao.publicFunc.condition_com import conditionCom
from xiongzhanghao.forms.article import AddForm, UpdateForm, SelectForm
import json, datetime, requests, os
from django.db.models import Q

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
            start_time = request.GET.get('start_time')
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
            print('start_time============>',start_time)
            if start_time:
                start_time = json.loads(start_time)
                stop_time = start_time[1]
                start_time = start_time[0]
                q.add(Q(articlePublishedDate__gte=start_time) & Q(articlePublishedDate__lte=stop_time), Q.AND)

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
                articlePicName = ''
                if obj.articlePicName:
                    articlePicName = obj.articlePicName
                articlePublishedDate = ''
                if obj.articlePublishedDate:
                    articlePublishedDate = obj.articlePublishedDate


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
                    'is_audit':obj.is_audit,
                    'article_status_id':obj.article_status,
                    'is_delete':obj.is_delete,
                    'manualRelease':obj.manualRelease,
                    'articlePicName':articlePicName,
                    'articlePublishedDate':articlePublishedDate, #发布时间
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
        back_url = request.POST.get('back_url')  # 如果手动发布 回链必填
        manualRelease = request.POST.get('manualRelease')
        user_id = request.GET.get('user_id')
        belongToUser_id = request.POST.get('belongToUser_id')
        articlePicName = request.POST.get('articlePicName')    # 文章缩略图

        form_data = {
            'user_id': user_id,
            'title': request.POST.get('title'),
            'summary': request.POST.get('summary'),
            'content': request.POST.get('content'),
            'column_id': request.POST.get('column_id'),
            'create_date': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'belongToUser_id': belongToUser_id,
            'send_time': request.POST.get('send_time'),
            'manualRelease': manualRelease,
            'articlePicName':articlePicName
        }

        print('form_data===============> ',form_data)
        if oper_type == "add":
            #  创建 form验证 实例（参数默认转成字典）
            forms_obj = AddForm(form_data)
            if forms_obj.is_valid():
                print("验证通过")
                print("forms_obj.data.get('column_id')========> ",forms_obj.cleaned_data.get('articlePicName'))
                obj = models.xzh_article.objects.create(**forms_obj.cleaned_data)
                if manualRelease == 'true':
                    print('手动添加===========手动添加===========================手动添加')
                    if not back_url:
                        response.msg = '回链不能为空'
                        response.code = 301
                        return JsonResponse(response.__dict__)

                    articleObjs = models.xzh_article.objects.filter(id=obj.id)
                    article_status = 4
                    articleTextUrl = request.POST.get('articleTextUrl')  # 特殊用户 二级域名内部添加的 url
                    articleTextKeyword = request.POST.get('articleTextKeyword')  # 特殊用户 二级域名内部添加的 关键词
                    if int(articleObjs[0].belongToUser.userType) == 2:  # 特殊用户
                        if not articleTextUrl:
                            response.code = 301
                            response.msg = '二级域名文章内部超链不能为空'
                            return JsonResponse(response.__dict__)
                        if not articleTextKeyword:
                            response.code = 301
                            response.msg = '二级域名文章内部关键词不能为空'
                            return JsonResponse(response.__dict__)

                        article_status = 6
                    articleObjs.update(
                        article_status=article_status,
                        back_url=back_url,
                        is_audit=True,
                        articlePicName=articlePicName,  # 缩略图
                        articleTextUrl=articleTextUrl,
                        articleTextKeyword=articleTextKeyword,

                    )
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
                            column_id = objForm.get('column_id'),
                            back_url=back_url,
                            articlePicName=articlePicName,  # 缩略图
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

        # 重新发布文章
        elif oper_type == 'redistribution':
            objs = models.xzh_article.objects.filter(id=o_id)
            if objs[0].article_status != 2:
                objs.update(article_status=1,note_content='')
            response.code = 200
            response.msg = '重新发布成功'

    else:
        if oper_type == 'thumbnail':   # 查询缩略图
            img_list = []
            for i in range(5):
                i += 1
                url = 'http://192.168.10.207:8003/statics/thumbnailPic/thumbnail0{}.png'.format(i)
                img_list.append(url)
            for i in range(2):
                i += 1
                url = 'http://192.168.10.207:8003/statics/thumbnailPic/thumbnail00{}.gif'.format(i)
                img_list.append(url)
            for i in range(63):
                i += 1
                url = 'http://192.168.10.207:8003/statics/thumbnailPic/thumbnail{}.jpg'.format(i)
                img_list.append(url)

            # for i in range(5):
            #     i += 1
            #     url = 'http://xiongzhanghao.zhugeyingxiao.com:8003/statics/thumbnailPic/thumbnail0{}.png'.format(i)
            #     img_list.append(url)
            # for i in range(2):
            #     i += 1
            #     url = 'http://xiongzhanghao.zhugeyingxiao.com:8003/statics/thumbnailPic/thumbnail00{}.gif'.format(i)
            #     img_list.append(url)
            # for i in range(63):
            #     i += 1
            #     url = 'http://xiongzhanghao.zhugeyingxiao.com:8003/statics/thumbnailPic/thumbnail{}.jpg'.format(i)
            #     img_list.append(url)


            response.code = 200
            response.msg = '查询成功'
            response.data = img_list

        else:
            response.code = 402
            response.msg = "请求异常"
    return JsonResponse(response.__dict__)

