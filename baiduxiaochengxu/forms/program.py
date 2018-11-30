from django import forms

from xiongzhanghao import models
from xiongzhanghao.publicFunc import account
import datetime, json


# 添加
class AddForm(forms.Form):
    belongUser_id = forms.IntegerField(
        required=True,
        error_messages={
            'required': "栏目创建人不能为空"
        }
    )

    program_name = forms.CharField(
        required=True,
        error_messages={
            'required': "栏目名称不能为空"
        }
    )

    program_type = forms.CharField(
        required=True,
        error_messages={
            'required': '栏目类型不能为空'
        }
    )

    program_text = forms.CharField(
        required=False,
        error_messages={
            'required': '单页内容类型错误'
        }
    )
    suoluetu = forms.CharField(
        required=True,
        error_messages={
            'required': '缩略图不能为空'
        }
    )


# 更新
class UpdateForm(forms.Form):
    belongUser_id = forms.IntegerField(
        required=True,
        error_messages={
            'required': "栏目创建人不能为空"
        }
    )

    program_name = forms.CharField(
        required=True,
        error_messages={
            'required': "栏目名称不能为空"
        }
    )

    program_type = forms.CharField(
        required=True,
        error_messages={
            'required': '栏目类型不能为空'
        }
    )

    program_text = forms.CharField(
        required=False,
        error_messages={
            'required': '单页内容类型错误'
        }
    )
    suoluetu = forms.CharField(
        required=True,
        error_messages={
            'required': '缩略图不能为空'
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

