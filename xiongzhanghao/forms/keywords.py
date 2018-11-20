from django import forms

from xiongzhanghao import models
from xiongzhanghao.publicFunc import account
import json

# 普通用户添加
class AddForm(forms.Form):
    user_id = forms.IntegerField(
        required=True,
        error_messages={
            'required': '请选择客户名称'
        }
    )

    keywords = forms.CharField(
        required=True,
        error_messages={
            'required': "关键词不能为空"
        }
    )

    # 查询名称是否存在
    def clean_user_id(self):
        user_id = self.data['user_id']
        objs = models.xzh_userprofile.objects.filter(
            id=user_id,
        )
        if not objs:
            self.add_error('user_id', '请求异常')
        else:
            return user_id

    def clean_keywords(self):
        keywords = self.data['keywords']
        if isinstance(json.loads(keywords), list):
            return json.loads(keywords)
        else:
            self.add_error('keywords', '关键词格式异常，请提交列表格式的字符串')


# 判断是否是数字
class SelectForm(forms.Form):
    uid = forms.IntegerField(
        # required=False,
        error_messages={
            'required': "请选择客户"
        }
    )
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
