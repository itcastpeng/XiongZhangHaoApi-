from xiongzhanghao import models
from xiongzhanghao.publicFunc import Response
from xiongzhanghao.publicFunc import account
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from bs4 import BeautifulSoup
from django.db.models import Q
import requests, random, json, datetime

@csrf_exempt
@account.is_token(models.xzh_userprofile)
def addFansGetTask(request, oper_type):
    response = Response.ResponseObj()
    q = Q()
    q.add(Q(status=2), Q.AND)

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
            obj = objs[0]
            obj.status = 2
            response.code = 200
            response.msg = '查询成功'
            response.data = obj.belong_user.fans_search_keyword
            obj.save()

    # 加粉前后 查询 粉丝数量
    elif oper_type == 'queryFollowersNum':
        objs = models.xzh_add_fans.objects.all().exclude(status__in=[4,5])
        for obj in objs:
            appid = obj.xiongzhanghaoID
            if appid:
                requests_obj = requests.session()
                url = 'https://author.baidu.com/home/{}?from=dusite_sresults'.format(appid)
                data = '%22from%22:%22dusite_sresults%22,%22app_id%22:%22{appid}%22'.format(appid=appid)
                url1 = 'https://author.baidu.com/profile?context={%s}&cmdType=&pagelets=root&reqID=0&ispeed=1' % data
                # print('url-------------> ',url)
                # print('url1-------------> ',url1)
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Mobile Safari/537.36',
                    'Referer': 'https://author.baidu.com/home/{}?from=dusite_sresults'.format(appid),
                }
                requests_obj.get(url, headers=headers)
                ret1 = requests_obj.get(url1, headers=headers)
                result = ret1.text.split('BigPipe.onPageletArrive(')[1]
                result = result[:-2]
                if result:
                    html = json.loads(result).get('html')
                    keyword = obj.belong_user.fans_search_keyword.split('熊掌号')[0].strip()
                    print('html---------------------> ',html, keyword)
                    if html and keyword in html:
                        soup = BeautifulSoup(html, 'lxml')
                        interaction = soup.find('div', id='interaction')
                        # print('interaction--------> ',interaction)
                        fans = interaction.find('div', class_='fans')
                        fans_num = fans.find('span').get_text()
                        obj.after_add_fans = int(fans_num)
                        print('当前粉丝数量------------------------------> ',fans_num)
                        if obj.status == 1:
                            print('粉前查询--------------=============')
                            obj.status = 2
                            obj.befor_add_fans=int(fans_num)

                        elif obj.status == 2:
                            print('加粉中=-------------------=================')
                            if int(fans_num) >= obj.add_fans_num + obj.befor_add_fans:
                                obj.status = 3
                        elif obj.status == 3:
                            print('粉后查询==========-----------------=========')
                            obj.status = 4
                            obj.after_add_fans = int(fans_num)
                        else:
                            obj.status = 5
                    else:
                        obj.status = 5
                        obj.errorText = '关键词与xiongzhanghaoID不匹配 或 连接超时, 请联系管理员'
                    obj.save()
            else:
                obj.status = 5
                obj.errorText = 'xiongzhanghaoID异常,请找管理员操作'
                obj.save()
                response.code = 301
                response.msg = '没有查到熊掌号ID'
        response.code = 200
        response.msg = '查询粉丝数量'
    return JsonResponse(response.__dict__)



