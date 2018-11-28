from django import forms

from xiongzhanghao import models
from xiongzhanghao.publicFunc import account
import time


# 普通用户添加
class AddForm(forms.Form):
    oper_user_id = forms.IntegerField(
        required=True,
        error_messages={
            'required': '操作人不能为空'
        }
    )

    belong_user_id = forms.IntegerField(
        required=True,
        error_messages={
            'required': "用户名不能为空"
        }
    )

    add_fans_num = forms.IntegerField(
        required=True,
        error_messages={
            'required': "粉丝数量不能为空"
        }
    )

    xiongzhanghaoID = forms.CharField(
        required=True,
        error_messages={
            'required': "熊掌号ID不能为空"
        }
    )

    search_keyword = forms.CharField(
        required=True,
        error_messages={
            'required': "搜索关键词不能为空"
        }
    )

    def clean_belong_user_id(self):
        belong_user_id = self.data.get('belong_user_id')
        objs = models.xzh_userprofile.objects.filter(id=belong_user_id)
        if not objs:
            self.add_error('belong_user_id', '无此用户')
        else:
            obj = objs[0]
            if int(obj.role_id) == 61:
                return belong_user_id
            else:
                self.add_error('belong_user_id', '不可加入管理员')

# 更新
class UpdateForm(forms.Form):
    o_id = forms.IntegerField(
        required=True,
        error_messages={
            'required': '修改用户不能为空'
        }
    )

    oper_user_id = forms.IntegerField(
        required=True,
        error_messages={
            'required': '操作人不能为空'
        }
    )

    belong_user_id = forms.IntegerField(
        required=True,
        error_messages={
            'required': "用户名不能为空"
        }
    )

    add_fans_num = forms.IntegerField(
        required=True,
        error_messages={
            'required': "粉丝数量不能为空"
        }
    )

    xiongzhanghao_url = forms.CharField(
        required=True,
        error_messages={
            'required': "熊掌号url不能为空"
        }
    )

    search_keyword = forms.CharField(
        required=True,
        error_messages={
            'required': "搜索关键词不能为空"
        }
    )
    def clean_belong_user_id(self):
        belong_user_id = self.data.get('belong_user_id')
        objs = models.xzh_userprofile.objects.filter(id=belong_user_id)
        if not objs:
            self.add_error('belong_user_id', '无此用户')
        else:
            obj = objs[0]
            if int(obj.role_id) == 61:
                return belong_user_id
            else:
                self.add_error('belong_user_id', '不可加入管理员')
    def clean_o_id(self):
        o_id = self.data.get('o_id')
        objs = models.xzh_add_fans.objects.filter(id=o_id)
        if not objs:
            self.add_error('o_id', '修改ID不存在')
        else:
            return o_id


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

