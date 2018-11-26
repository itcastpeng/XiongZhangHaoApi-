from django import forms

from xiongzhanghao import models
from xiongzhanghao.publicFunc import account
import datetime, json


# 添加
class AddForm(forms.Form):
    user_id = forms.CharField(
        required=True,
        error_messages={
            'required': "文章创建人不能为空"
        }
    )

    title = forms.CharField(
        required=True,
        error_messages={
            'required': "文章标题不能为空"
        }
    )

    summary = forms.CharField(
        required=True,
        error_messages={
            'required': '文章摘要不能为空'
        }
    )

    content = forms.CharField(
        required=True,
        error_messages={
            'required': '文章内容不能为空'
        }
    )

    column_id = forms.IntegerField(
        required=True,
        error_messages={
            'required': '栏目不能为空'
        }
    )

    belongToUser_id = forms.IntegerField(
        required=True,
        error_messages={
            'required': '归属用户不能为空'
        }
    )

    send_time = forms.DateTimeField(
        required=False,
        error_messages={
            'required': '发送时间格式错误'
        }
    )
    manualRelease = forms.BooleanField(
        required=False,
        error_messages={
            'required': '手动发布格式错误'
        }
    )
    articlePicName = forms.CharField(
        required=False,
        error_messages={
            'required': '文章缩略图格式错误'
        }
    )


    def clean_column_id(self):
        column_id = self.data.get('column_id')
        belongToUser_id = self.data.get('belongToUser_id')
        objs = models.xzh_userprofile.objects.filter(id=belongToUser_id)
        if objs:
            if objs[0].column_all:
                for i in eval(objs[0].column_all):
                    if int(column_id) == int(i[0]):
                        data_dict = {
                            'Id':i[0],
                            'name':i[1]
                        }
                        print('data_dict--> ',data_dict)
                        return data_dict
            else:
                self.add_error('column_id', '该归属用户无栏目')
        else:
            self.add_error('column_id', '无此用户')

    def clean_title(self):
        title = self.data.get('title')
        if len(title) > 22:
            self.add_error('title', '标题长度不得大于22')
        else:
            return title


# 特殊用户添加验证 or 手动添加



# 更新
class UpdateForm(forms.Form):
    user_id = forms.CharField(
        required=False,
        error_messages={
            'required': "文章创建人不能为空"
        }
    )

    title = forms.CharField(
        required=False,
        error_messages={
            'required': "文章标题不能为空"
        }
    )

    summary = forms.CharField(
        required=False,
        error_messages={
            'required': '文章摘要不能为空'
        }
    )

    content = forms.CharField(
        required=False,
        error_messages={
            'required': '文章内容不能为空'
        }
    )

    column_id = forms.IntegerField(
        required=True,
        error_messages={
            'required': '栏目不能为空'
        }
    )

    belongToUser_id = forms.IntegerField(
        required=True,
        error_messages={
            'required': '归属用户不能为空'
        }
    )

    send_time = forms.DateTimeField(
        required=False,
        error_messages={
            'required': '发送时间格式错误'
        }
    )
    def clean_column_id(self):
        column_id = self.data.get('column_id')
        belongToUser_id = self.data.get('belongToUser_id')
        print('column_id--------->', column_id, belongToUser_id)
        objs = models.xzh_userprofile.objects.filter(id=belongToUser_id)
        if objs[0].column_all:
            for i in eval(objs[0].column_all):
                if int(column_id) == int(i[0]):
                    data_dict = {
                        'Id': i[0],
                        'name': i[1]
                    }
                    print('data_dict--> ', data_dict)
                    return data_dict
        else:
            self.add_error('column_id', '该归属用户无栏目')


# 判断是否是数字
class SelectForm(forms.Form):
    current_page = forms.IntegerField(
        required=False,
        error_messages={
            'required': "页码数据类型错误"
        }
    )

    length = forms.IntegerField(
        required=False,
        error_messages={
            'required': "页显示数量类型错误"
        }
    )

    def clean_current_page(self):
        if 'current_page' not in self.data:
            current_page = 1
        else:
            current_page = int(self.data['current_page'])
        return current_page

    def clean_length(self):
        if 'length' not in self.data:
            length = 10
        else:
            length = int(self.data['length'])
        return length


# 脚本修改文章
# class ScriptUpdateForm(forms.Form):
#     articleId = forms.IntegerField(
#         required=True,
#         error_messages={
#             'required': "文章ID不能为空"
#         }
#     )
#     articleStatus = forms.IntegerField(
#         required=True,
#         error_messages={
#             'required': "文章状态不能为空"
#         }
#     )
#     backUrl = forms.CharField(
#         required=False,
#         error_messages={
#             'required': "回链地址类型错误"
#         }
#     )
#     def clean_articleId(self):
#         articleId = self.data.get('articleId')
#         articleStatus = self.data.get('articleStatus')
#         backUrl = self.data.get('backUrl')
#         objs = models.xzh_article.objects.filter(id=articleId)
#         if objs:
#             objs.update(article_status=articleStatus)
#             if backUrl:
#                 objs.update(back_url=backUrl)
#         else:
#             self.add_error('articleId', '修改ID不存在')
