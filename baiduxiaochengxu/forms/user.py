from django import forms

from xiongzhanghao import models
from xiongzhanghao.publicFunc import account
import time, re


# 普通用户添加
class AddForm(forms.Form):
    # oper_user_id = forms.IntegerField(
    #     required=True,
    #     error_messages={
    #         'required': '操作人不能为空'
    #     }
    # )

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
    lunbotu = forms.CharField(
        required=True,
        error_messages={
            'required': "轮播图不能为空"
        }
    )
    hospital_logoImg = forms.CharField(
        required=True,
        error_messages={
            'required': "logo图片不能为空"
        }
    )
    hospital_phone = forms.IntegerField(
        required=True,
        error_messages={
            'required': "医院电话不能为空"
        }
    )
    hospital_introduction = forms.CharField(
        required=True,
        error_messages={
            'required': "医院简介不能为空"
        }
    )
    hospital_address = forms.CharField(
        required=True,
        error_messages={
            'required': "医院地址不能为空"
        }
    )
    hospital_menzhen = forms.CharField(
        required=True,
        error_messages={
            'required': "医院门诊时间不能为空"
        }
    )

    token = forms.IntegerField(
        required=False
    )

    # 查询名称是否存在
    def clean_username(self):
        username = self.data['username']
        objs = models.xcx_userprofile.objects.filter(
            username=username,
        )
        if objs:
            self.add_error('username', '用户名已存在')
        else:
            return username

    def clean_token(self):
        password = self.data['password']
        return account.get_token(password + str(int(time.time()) * 1000))

    def clean_password(self):
        password = self.data['password']
        return account.str_encrypt(password)

    def clean_hospital_phone(self):
        hospital_phone = self.data.get('hospital_phone')
        phone_pat = re.compile('^(13\d|14[5|7]|15\d|166|17[3|6|7]|18\d)\d{8}$')
        res = re.search(phone_pat, hospital_phone)
        if res:
            return hospital_phone
        else:
            self.add_error('hospital_phone', '请输入正确手机号')



# 更新
class UpdateForm(forms.Form):
    # o_id = forms.IntegerField(
    #     required=True,
    #     error_messages={
    #         'required': '修改id不能为空'
    #     }
    # )

    username = forms.CharField(
        required=True,
        error_messages={
            'required': "用户名不能为空"
        }
    )
    lunbotu = forms.CharField(
        required=True,
        error_messages={
            'required': "轮播图不能为空"
        }
    )
    hospital_logoImg = forms.CharField(
        required=True,
        error_messages={
            'required': "logo图片不能为空"
        }
    )
    hospital_phone = forms.IntegerField(
        required=True,
        error_messages={
            'required': "医院电话不能为空"
        }
    )
    hospital_introduction = forms.CharField(
        required=True,
        error_messages={
            'required': "医院简介不能为空"
        }
    )
    hospital_address = forms.CharField(
        required=True,
        error_messages={
            'required': "医院地址不能为空"
        }
    )
    hospital_menzhen = forms.CharField(
        required=True,
        error_messages={
            'required': "医院门诊时间不能为空"
        }
    )

    # 判断名称是否存在
    # def clean_username(self):
    #     o_id = self.data['o_id']
    #     username = self.data['username']
    #     objs = models.xcx_userprofile.objects.filter(
    #         username=username,
    #     ).exclude(
    #         id=o_id
    #     )
    #     if objs:
    #         self.add_error('username', '用户名已存在')
    #     else:
    #         return username

    def clean_hospital_phone(self):
        hospital_phone = self.data.get('hospital_phone')
        phone_pat = re.compile('^(13\d|14[5|7]|15\d|166|17[3|6|7]|18\d)\d{8}$')
        res = re.search(phone_pat, hospital_phone)
        if res:
            return hospital_phone
        else:
            self.add_error('hospital_phone', '请输入正确手机号')


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

    # def clean_company_id(self):
    #     role_id = self.data.get('role_id')
    #     company_id = self.data.get('company_id')
    #     print('role_id -->', role_id)
    #     print('company_id -->', company_id)
    #     if role_id != '1' and not company_id:
    #         self.add_error('company_id', '公司id不能为空')
    #     else:
    #         return company_id
