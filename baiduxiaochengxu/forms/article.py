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

    content = forms.CharField(
        required=True,
        error_messages={
            'required': '文章内容不能为空'
        }
    )

    belongToUser_id = forms.IntegerField(
        required=True,
        error_messages={
            'required': '归属用户不能为空'
        }
    )
    article_program_id = forms.IntegerField(
        required=True,
        error_messages={
            'required': '栏目不能为空'
        }
    )
    article_type =  forms.IntegerField(
        required=True,
        error_messages={
            'required': '栏目不能为空'
        }
    )
    article_introduction = forms.CharField(
        required=True,
        error_messages={
            'required': '文章简介不能为空'
        }
    )
    suoluetu = forms.CharField(
        required=True,
        error_messages={
            'required': '缩略图不能为空'
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
    title = forms.CharField(
        required=True,
        error_messages={
            'required': "文章标题不能为空"
        }
    )

    content = forms.CharField(
        required=True,
        error_messages={
            'required': '文章内容不能为空'
        }
    )

    belongToUser_id = forms.IntegerField(
        required=True,
        error_messages={
            'required': '归属用户不能为空'
        }
    )
    article_program_id = forms.IntegerField(
        required=True,
        error_messages={
            'required': '栏目不能为空'
        }
    )
    article_type = forms.IntegerField(
        required=True,
        error_messages={
            'required': '类型不能为空'
        }
    )
    article_introduction = forms.CharField(
        required=True,
        error_messages={
            'required': '文章简介不能为空'
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

