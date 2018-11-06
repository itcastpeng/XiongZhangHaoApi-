

import requests
import json
import base64


class LianZhongDama(object):

    def __init__(self):
        self.softwareId = 11845
        self.softwareSecret = 'v4RsfAB2DDmCXUa1EsNlNZD7UfCaXm1jhIYQtyRc'
        self.username = 'zhangcong123'
        self.password = 'hzkq@2018.123'

    # 获取还剩余多少点
    def check_points(self):
        post_data = {
            'softwareId': self.softwareId,
            'softwareSecret': self.softwareSecret,
            'username': self.username,
            'password': self.password
        }
        url = 'https://v2-api.jsdama.com/check-points'
        ret = requests.post(url, data=json.dumps(post_data))
        print(ret.text)

    # 获取图片验证码
    def get_yzm(self, file_path):
        f = open(file_path, 'rb')
        fdata = f.read()
        filedata = base64.b64encode(fdata)
        f.close()
        captchaData = str(filedata, encoding='utf-8')

        post_data = {
            'softwareId': self.softwareId,
            'softwareSecret': self.softwareSecret,
            'username': self.username,
            'password': self.password,
            'captchaType': 1001,
            'captchaData': captchaData
        }
        import datetime
        print(str(datetime.datetime.now()) + '--------------------> 请求获取验证码')

        url = 'https://v2-api.jsdama.com/upload'
        ret = requests.post(url, data=json.dumps(post_data))
        print('ret.text -->', ret.text)
        yzm = ret.json()['data']['recognition']
        print(str(datetime.datetime.now()) + '--------------------> 返回验证码')
        return yzm


if __name__ == '__main__':
    obj = LianZhongDama()
    yzm = obj.get_yzm('screenshot.png')
    print('yzm -->', yzm)
