from django import forms

from xiongzhanghao import models
from xiongzhanghao.publicFunc import account
import datetime


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
        required=False,
        error_messages={
            'required': '栏目类型错误'
        }
    )

    belongToUser_id = forms.IntegerField(
        required=True,
        error_messages={
            'required': '归属用户不能为空'
        }
    )


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
        required=False,
        error_messages={
            'required': '栏目类型错误'
        }
    )

    create_date = forms.DateTimeField(
        required=False,
        error_messages={
            'required': '时间不能为空'
        }
    )

    belongToUser_id = forms.IntegerField(
        required=True,
        error_messages={
            'required': '归属用户不能为空'
        }
    )


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
