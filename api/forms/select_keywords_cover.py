from django import forms

from xiongzhanghao import models
from xiongzhanghao.publicFunc import account
import datetime, json


# 添加
class AddForm(forms.Form):
    url = forms.CharField(
        required=True,
        error_messages={
            'required': "匹配到的链接不能为空"
        }
    )

    keywords = forms.CharField(
        required=True,
        error_messages={
            'required': "关键词不能为空"
        }
    )

    rank = forms.IntegerField(
        required=True,
        error_messages={
            'required': '排名不能为空'
        }
    )

    keywords_id = forms.IntegerField(
        required=True,
        error_messages={
            'required': '关键词id不能为空'
        }
    )
