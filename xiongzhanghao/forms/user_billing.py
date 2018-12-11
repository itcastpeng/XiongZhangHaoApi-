from django import forms

from xiongzhanghao import models
from xiongzhanghao.publicFunc import account
import time, datetime

# 添加
class AddForm(forms.Form):
    belong_user_id = forms.IntegerField(
        required=True,
        error_messages={
            'required': '归属人不能为空'
        }
    )

    start_time = forms.DateField(
        required=False,
        error_messages={
            'required': "开始时间类型错误"
        }
    )

    stop_time = forms.DateField(
        required=False,
        error_messages={
            'required': "结束时间类型错误"
        }
    )

    billing_cycle = forms.IntegerField(
        required=False,
        error_messages={
            'required': "计费周期类型错误"
        }
    )

    note_text = forms.CharField(
        required=False,
        error_messages={
            'required': "备注类型错误"
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
                self.add_error('belong_user_id', '不可关联管理员')

    def clean_billing_cycle(self):
        billing_cycle = self.data.get('billing_cycle')
        if billing_cycle:
            billing_cycle = int(billing_cycle)
            now = datetime.datetime.now()
            start_time = now.strftime('%Y-%m-%d')
            if billing_cycle == 2:   # 二个月
                month = now.month + 2
            elif billing_cycle == 3:
                month = now.month + 3
            elif billing_cycle == 4:
                month = now.month + 4
            elif billing_cycle == 5:
                month = now.month + 5
            elif billing_cycle == 6:
                month = now.month + 6
            elif billing_cycle == 7:
                month = now.month + 12
            else:
                month = now.month + 1
            if month > 12:
                month = month - 12
            stop_time = now.strftime('%Y-{}-%d'.format(month))
            return billing_cycle, start_time, stop_time

    def clean_start_time(self):
        start_time = self.data.get('start_time')
        stop_time = self.data.get('stop_time')
        if start_time and stop_time:
            if type(start_time) == str and type(stop_time) == str:
                start_time = datetime.datetime.strptime(start_time, "%Y-%m-%d")
                stop_time = datetime.datetime.strptime(stop_time, "%Y-%m-%d")
            days = (stop_time - start_time)
            start_time = start_time.strftime('%Y-%m-%d')
            stop_time = stop_time.strftime('%Y-%m-%d')
            days = days.days
            print('days===========> ',days)
            if days >= 29:
                month = int(days / 30)
                if month >= 7:
                    month = 7
            else:
                if days < 30:
                    self.add_error('start_time', '天数不能小于三十天')
                    return
                else:
                    month = 1

            return start_time, stop_time, month

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

