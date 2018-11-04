from django import forms

from xiongzhanghao import models
from xiongzhanghao.publicFunc import account
import datetime


# 添加
class AddForm(forms.Form):
    user_id = forms.CharField(
        required=True,
        error_messages={
            'required': "文章作者不能为空"
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

    TheColumn = forms.CharField(
        required=True,
        error_messages={
            'required': '栏目不能为空'
        }
    )



# 更新
class UpdateForm(forms.Form):
    user_id = forms.CharField(
        required=False,
        error_messages={
            'required': "文章作者不能为空"
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

    TheColumn = forms.CharField(
        required=False,
        error_messages={
            'required': '栏目不能为空'
        }
    )

    create_date = forms.DateTimeField(
        required=False,
        error_messages={
            'required': '时间不能为空'
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