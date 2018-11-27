from xiongzhanghao import models
from xiongzhanghao.publicFunc import Response
from xiongzhanghao.publicFunc import account
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from bs4 import BeautifulSoup

import requests, random

pcRequestHeader = [
    'Mozilla/5.0 (Windows NT 5.1; rv:6.0.2) Gecko/20100101 Firefox/6.0.2',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.52 Safari/537.17',
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1.16) Gecko/20101130 Firefox/3.5.16',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; .NET CLR 1.1.4322)',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.99 Safari/537.36',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2)',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.13 (KHTML, like Gecko) Chrome/24.0.1290.1 Safari/537.13',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
    'Mozilla/5.0 (Windows; U; Windows NT 5.2; zh-CN; rv:1.9.0.19) Gecko/2010031422 Firefox/3.0.19 (.NET CLR 3.5.30729)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.2)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.57 Safari/537.17',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13'
]

@csrf_exempt
@account.is_token(models.xzh_userprofile)
def addFansGetTask(request, oper_type):
    response = Response.ResponseObj()
    # 判断是否有任务
    if oper_type == 'judgmentTask':
        objs = models.xzh_add_fans.objects.filter(status=2)[:1]
        flag = False
        if objs:
            flag = True
        response.code = 200
        response.data = {
            'flag':flag
        }

    # 获取任务
    elif oper_type == 'getTask':
        objs = models.xzh_add_fans.objects.filter(status=2).order_by('?')[:10]
        flag = False
        if not objs:
            response.data = {
                'flag':flag
            }
        else:
            flag = True
            obj = objs[0]
            obj.status = 2
            response.code = 200
            response.msg = '查询成功'
            response.data = {
                'flag': flag,
                'o_id':obj.id,
                'xiongzhanghao_url':obj.xiongzhanghao_url,
                'add_fans_num':obj.add_fans_num,
            }
            obj.save()

    # 返回任务 更改状态
    elif oper_type == 'getTaskModel':
        o_id = request.GET.get('o_id')
        o_id = request.GET.get('o_id')
        o_id = request.GET.get('o_id')


    # 加粉前 查询 粉丝数量
    elif oper_type == 'befor':
        headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'}
        keyword = '宁波送子鸟妇科医院 熊掌号'
        # headers = {'User-Agent': pcRequestHeader[random.randint(0, len(pcRequestHeader) - 1)], }
        # objs = models.xzh_add_fans.objects.filter(status=1)[:10]
        # if objs:
        #     obj = objs[0]
        # obj.xiongzhanghao_url
        xiongzhanghao_url = 'https://m.baidu.com/s?word={}'.format(keyword)
        print('=xiongzhanghao_url===================> ',xiongzhanghao_url)
        ret = requests.get(xiongzhanghao_url, headers=headers)
        # print(ret.text)
        soup = BeautifulSoup(ret.text, 'lxml')
        main_div = soup.find('div', class_='wa-guanfanghao-main')
        for i in main_div.find_all('div', class_='c-gap-top-small'):
            print('i---------------------> ', i.find('a'))


    # 加粉后 查询 粉丝数量
    elif oper_type == 'after':
        pass

    return JsonResponse(response.__dict__)



