from xiongzhanghao import models
from xiongzhanghao.publicFunc import Response
from xiongzhanghao.publicFunc import account
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from bs4 import BeautifulSoup
from django.db.models import Q
import requests, random, json, datetime

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

    # now = datetime.datetime.now()
    # deletionTime = (now - datetime.timedelta(hours=2)).strftime('%Y-%m-%d %H:%M:%S')
    # deletionTime = datetime.datetime.strptime(deletionTime, '%Y-%m-%d %H:%M:%S')
    q = Q()
    q.add(Q(status=2), Q.AND)
    # q.add(Q(taskTimeBetween__isnull=True) | Q(taskTimeBetween__lte=deletionTime), Q.AND)

    # 判断是否有任务
    if oper_type == 'judgmentTask':
        objs = models.xzh_add_fans.objects.filter(q)[:1]
        flag = False
        if objs:
            flag = True
        response.code = 200
        response.data = {
            'flag':flag
        }

    # 获取任务
    elif oper_type == 'getTask':
        objs = models.xzh_add_fans.objects.filter(q).order_by('?')[:1]
        if objs:
            # now = datetime.datetime.now()
            # objs[0].taskTimeBetween=now
            # objs[0].save()
            obj = objs[0]
            obj.status = 2
            response.code = 200
            response.msg = '查询成功'
            response.data = obj.search_keyword
            obj.save()

    # 返回任务 更改状态
    # elif oper_type == 'getTaskModel':
    #     o_id = request.GET.get('o_id')
    #     objs = models.xzh_add_fans.objects.filter(id=o_id)
    #     if objs and objs[0].status == 2:
    #         obj = objs[0]
    #         obj.status = 3
    #         obj.save()
    #     response.code = 200
    #     response.msg = '更新成功'


    # 加粉前后 查询 粉丝数量
    elif oper_type == 'queryFollowersNum':
        objs = models.xzh_add_fans.objects.order_by('?')[:10]
        for obj in objs:
            appid = obj.xiongzhanghaoID
            requests_obj = requests.session()
            url = 'https://author.baidu.com/home/{}?from=dusite_sresults'.format(appid)
            data = '%22from%22:%22dusite_sresults%22,%22app_id%22:%22{appid}%22'.format(appid=appid)
            url1 = 'https://author.baidu.com/profile?context={%s}&cmdType=&pagelets=root&reqID=0&ispeed=1' % data
            print('url-------------> ',url)
            print('url1-------------> ',url1)
            headers = {
                'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Mobile Safari/537.36',
                'Referer': 'https://author.baidu.com/home/{}?from=dusite_sresults'.format(appid),
            }

            ret = requests_obj.get(url, headers=headers)
            ret1 = requests_obj.get(url1, headers=headers)
            print('ret1.text--------> ', ret1.text)

            result = ret1.text.split('BigPipe.onPageletArrive(')[1]
            print('result--------->==========',result)
            result = result[:-2]
            if result:
                html = json.loads(result).get('html')
                if html:
                    soup = BeautifulSoup(html, 'lxml')
                    interaction = soup.find('div', id='interaction')
                    print('interaction--------> ',interaction)
                    fans = interaction.find('div', class_='fans')
                    fans_num = fans.find('span').get_text()
                    print('当前粉丝数量------------------------------> ',fans_num)
                    if obj.status == 1:
                        print('粉前查询--------------=============')
                        obj.status = 2
                        obj.befor_add_fans=int(fans_num)

                    elif obj.status == 2:
                        print('加粉中=-------------------=================')
                        if int(fans_num) >= obj.add_fans_num:
                            obj.status = 3

                    elif obj.status == 3:
                        print('粉后查询==========-----------------=========')
                        obj.status = 4
                        obj.after_add_fans=int(fans_num)
                else:
                    obj.status = 0
                    print('未请求到==================================')
                obj.save()
        response.code = 200
        response.msg = '查询粉丝数量'
    return JsonResponse(response.__dict__)



