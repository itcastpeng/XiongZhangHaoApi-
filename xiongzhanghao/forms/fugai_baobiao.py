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

    username = forms.CharField(
        required=True,
        error_messages={
            'required': "用户名不能为空"
        }
    )

    password = forms.CharField(
        required=True,
        error_messages={
            'required': "密码不能为空"
        }
    )

    role_id = forms.IntegerField(
        required=True,
        error_messages={
            'required': "角色名称不能为空"
        }
    )

    website_backstage = forms.IntegerField(
        required=True,
        error_messages={
            'required': "后台类型,类型错误"
        }
    )
    website_backstage_username = forms.CharField(
        required=True,
        error_messages={
            'required': "客户后台账号不能为空"
        }
    )
    website_backstage_password = forms.CharField(
        required=True,
        error_messages={
            'required': "客户后台密码不能为空"
        }
    )
    website_backstage_url = forms.CharField(
        required=True,
        error_messages={
            'required': "客户后台链接不能为空"
        }
    )

    token = forms.IntegerField(
        required=False
    )
    website_backstage_appid = forms.CharField(
        required=True,
        error_messages={
            'required': "熊掌号appid不能为空"
        }
    )
    website_backstage_token = forms.CharField(
        required=True,
        error_messages={
            'required': "熊掌号appid不能为空"
        }
    )


    # 查询名称是否存在
    def clean_username(self):
        username = self.data['username']
        objs = models.xzh_userprofile.objects.filter(
            username=username,
        )
        if objs:
            self.add_error('username', '用户名已存在')
        else:
            return username

    def clean_password(self):
        password = self.data['password']
        return account.str_encrypt(password)

    def clean_token(self):
        password = self.data['password']
        return account.get_token(password + str(int(time.time()) * 1000))

# 添加管理员
class AdminAddForm(forms.Form):
    oper_user_id = forms.IntegerField(
        required=True,
        error_messages={
            'required': '操作人不能为空'
        }
    )

    username = forms.CharField(
        required=True,
        error_messages={
            'required': "用户名不能为空"
        }
    )

    password = forms.CharField(
        required=True,
        error_messages={
            'required': "密码不能为空"
        }
    )

    role_id = forms.IntegerField(
        required=True,
        error_messages={
            'required': "角色名称不能为空"
        }
    )
    token = forms.IntegerField(
        required=False
    )

    # 查询名称是否存在
    def clean_username(self):
        username = self.data['username']
        objs = models.xzh_userprofile.objects.filter(
            username=username,
        )
        if objs:
            self.add_error('username', '用户名已存在')
        else:
            return username

    def clean_password(self):
        password = self.data['password']
        return account.str_encrypt(password)

    def clean_token(self):
        password = self.data['password']
        return account.get_token(password + str(int(time.time()) * 1000))

# 更新
class UpdateForm(forms.Form):
    o_id = forms.IntegerField(
        required=True,
        error_messages={
            'required': '修改id不能为空'
        }
    )

    username = forms.CharField(
        required=True,
        error_messages={
            'required': "用户名不能为空"
        }
    )

    role_id = forms.IntegerField(
        required=True,
        error_messages={
            'required': "角色名称不能为空"
        }
    )

    website_backstage = forms.IntegerField(
        required=False,
        error_messages={
            'required': "后台类型,类型错误"
        }
    )
    website_backstage_username = forms.CharField(
        required=True,
        error_messages={
            'required': "客户后台账号不能为空"
        }
    )
    website_backstage_password = forms.CharField(
        required=True,
        error_messages={
            'required': "客户后台密码不能为空"
        }
    )
    website_backstage_url = forms.CharField(
        required=True,
        error_messages={
            'required': "客户后台链接不能为空"
        }
    )
    website_backstage_appid = forms.CharField(
        required=True,
        error_messages={
            'required': "熊掌号appid不能为空"
        }
    )
    website_backstage_token = forms.CharField(
        required=True,
        error_messages={
            'required': "熊掌号appid不能为空"
        }
    )
    # 判断名称是否存在
    def clean_username(self):
        o_id = self.data['o_id']
        username = self.data['username']
        objs = models.xzh_userprofile.objects.filter(
            username=username,
        ).exclude(
            id=o_id
        )
        if objs:
            self.add_error('username', '用户名已存在')
        else:
            return username


# 管理员更新
class AdminUpdateForm(forms.Form):
    o_id = forms.IntegerField(
        required=True,
        error_messages={
            'required': '角色id不能为空'
        }
    )

    username = forms.CharField(
        required=True,
        error_messages={
            'required': "用户名不能为空"
        }
    )

    role_id = forms.IntegerField(
        required=True,
        error_messages={
            'required': "角色名称不能为空"
        }
    )

    # 判断名称是否存在
    def clean_username(self):
        o_id = self.data['o_id']
        username = self.data['username']
        objs = models.xzh_userprofile.objects.filter(
            username=username,
        ).exclude(
            id=o_id
        )
        if objs:
            self.add_error('username', '用户名已存在')
        else:
            return username


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
