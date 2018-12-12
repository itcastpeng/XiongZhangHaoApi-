from django.http import JsonResponse, HttpResponse
from django.db.models import Q
from backend.selectDeleteQuery import index
from xiongzhanghao import models
from xiongzhanghao.publicFunc import Response
from xiongzhanghao.publicFunc import account
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.db.models.query import QuerySet
from bs4 import BeautifulSoup
import datetime, requests, json, time, redis

# 脚本 查询熊掌号主页 获取粉丝数量 和主页显示数量 (主页收录)
def xiongzhanghao_index_num(now, appid, url_list):
    requests_obj = requests.session()
    url = 'https://author.baidu.com/home/{}?from=dusite_sresults'.format(appid)
    data = '%22from%22:%22dusite_sresults%22,%22app_id%22:%22{appid}%22'.format(appid=appid)
    url1 = 'https://author.baidu.com/profile?context={%s}&cmdType=&pagelets=root&reqID=0&ispeed=1' % data

    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Mobile Safari/537.36',
        'Referer': '{}'.format(url),
    }
    #======================================获取粉丝数量=================================
    fans_num = 0
    requests_obj.get(url, headers=headers)
    ret1 = requests_obj.get(url1, headers=headers)
    result = ret1.text.split('BigPipe.onPageletArrive(')[1]
    result = result[:-2]
    if result:
        if now == datetime.datetime.now().strftime('%m-%d'):  # 如果查询时间为 今天粉丝数量则查
            html = json.loads(result).get('html')
            soup = BeautifulSoup(html, 'lxml')
            interaction = soup.find('div', id='interaction')
            fans = interaction.find('div', class_='fans')
            fans_num = fans.find('span').get_text()
    # ================================获取文章查询主页展示条数==========================================
    index_url = 'http://xiongzhang.baidu.com/officeplatform/home/zparticlelist?office_id={}&offset=&last_time=0&page_size=30'.format(appid)
    ret2 = requests_obj.get(index_url)
    encode_ret = ret2.apparent_encoding
    if encode_ret == 'GB2312':
        ret2.encoding = 'gbk'
    else:
        ret2.encoding = 'utf-8'
    ret_text = json.loads(ret2.text)
    index_num = 0
    url_data = []
    if ret_text:
        items = ret_text.get('data').get('items')
        for item in items:
            created_at = item.get('created_at')   # 获取文章创建时间戳 对比当前时间
            created_time = time.localtime(created_at)
            created_time = time.strftime("%m-%d", created_time)
            if now == created_time:
                # print('-------------------------> ', now)
                url = item.get('url')
                title = item.get('title')
                for i in url_list:
                    if title == i['title'] or title in i['title']:
                        # print('title===>',title)
                        index_num += 1
                        url_data.append(url)
    data = {
        'fans_num':fans_num,
        'index_num':index_num,
        'url_data':url_data
    }
    return data


@csrf_exempt
@account.is_token(models.xzh_userprofile)
def user_statistical(request, oper_type):
    response = Response.ResponseObj()
    # appid = 1611292686377463
    if request.method == 'POST':

        # 查询所有用户七天内数据
        if oper_type == 'user_statistical':
            user_objs = models.xzh_userprofile.objects
            article_objs = models.xzh_article.objects

            deletionTime = datetime.datetime.now()
            for date_i in range(7):          # 获取近七天数据
                now = deletionTime.strftime('%Y-%m-%d')
                start_now = deletionTime.strftime('%Y-%m-%d 00:00:00')    # 今天开始时间
                stop_now = deletionTime.strftime('%Y-%m-%d 23:59:59')     # 当前时间(年月日 时分秒)

                print('now---> ',now, start_now, stop_now)
                userObjs = user_objs.filter(
                    # userType=1,
                    role_id=61,
                    website_backstage_appid__isnull=False,
                    xiong_zhang_hao_user__isnull=False,
                    xiong_zhang_hao_pwd__isnull=False
                )  # 查询所有用户
                for userObj in userObjs:  # 遍历所有用户
                    userObj_id = userObj.id
                    appid = userObj.website_backstage_appid
                    data = {                    # 构造数据
                        'public_num': '',           # 发布数量
                        'belong_user_id': '',       # 归属人
                        'index_show':0,             # 主页显示
                        'fans_num':0,               # 粉丝数量
                        'index_show_url':'',        # 主页展示文章链接
                        'create_date':now,          # 创建时间
                    }

                    articleObjs = article_objs.filter(       # 查询今天发布的文章 总数
                        belongToUser_id=userObj_id
                    ).filter(
                        create_date__gte=start_now,
                        create_date__lte=stop_now
                    )
                    data['belong_user_id'] = userObj_id      # 归属用户
                    data['public_num'] = articleObjs.count() # 该用户今日发布总数

                    url_list = []

                    for articleObj in articleObjs:
                        url_list.append({
                            'back_url':articleObj.back_url,
                            'title':articleObj.title
                        })
                    # 传入now 月日%m-%d
                    now_m_d = deletionTime.strftime('%m-%d')
                    data_list = xiongzhanghao_index_num(now_m_d, appid, url_list)
                    data['fans_num'] = data_list['fans_num']
                    data['index_show'] = data_list['index_num']
                    data['index_show_url'] = data_list['url_data']       # 熊掌号主页 url

                    statisticsObjs = models.user_statistics.objects.filter(belong_user_id=userObj_id, create_date=now)   # 判断今天 该用户是否有数据 有则更新 无则创建
                    print('data====================> ',data)
                    if statisticsObjs:
                        if int(data['fans_num']) == 0:  # 粉丝数量 如果为0则不更改粉丝数量
                            data = {
                                'public_num': articleObjs.count(),
                                'belong_user_id': userObj_id,
                                'index_show': data_list['index_num'],
                                'index_show_url': data_list['url_data'],
                                'create_date': now,
                            }
                        statisticsObjs.update(**data)
                        msg = '更新成功'
                    else:
                        statisticsObjs.create(**data)
                        msg = '创建成功'
                    response.code = 200
                    response.msg = msg
                deletionTime = (deletionTime - datetime.timedelta(days=1))  # 当前时间(年月日)

        # 百度收录返回任务
        elif oper_type == 'baiDuShouLuSaveModel':
            print('baiDuShouLuSaveModel==================baiDuShouLuSaveModel==================baiDuShouLuSaveModel')
            user_id = request.POST.get('user_id')
            url = request.POST.get('url')
            create_date = request.POST.get('create_date')
            if user_id and create_date and url:
                print('user_id, create_date-------->',user_id, create_date)
                objs = models.user_statistics.objects.filter(belong_user_id=user_id, create_date=create_date)
                obj = objs[0]
                baidu_shoulu_url = eval(obj.baidu_shoulu_url)
                if url not in baidu_shoulu_url:   # 避免数据重复入库
                    baidu_shoulu = obj.baidu_shoulu + 1
                    obj.baidu_shoulu = baidu_shoulu
                    baidu_shoulu_url.append(url)
                    obj.baidu_shoulu_url = baidu_shoulu_url
                    obj.save()

            response.code = 200
            response.msg = '保存成功'

        # selenium返回后台数据
        elif oper_type == 'returnTask':
            now = datetime.datetime.now()
            now_date = now.strftime('%Y-%m-%d')
            zhishu = request.POST.get('zhishu')
            shoulu_list = request.POST.get('shoulu_list')
            click_show_list = request.POST.get('click_show_list')
            user_id = request.POST.get('user_id')
            if zhishu and user_id and shoulu_list and click_show_list:
                shoulu_list = json.loads(shoulu_list)
                click_show_list = json.loads(click_show_list)
                statisticsObj = models.user_statistics.objects.filter(belong_user_id=user_id, create_date=now_date)
                if statisticsObj:
                    if zhishu == 0 and statisticsObj[0].zhishu:
                        pass
                    else:
                        statisticsObj.update(zhishu=zhishu)
                for i in click_show_list:
                    click_show_obj = models.user_statistics.objects.filter(belong_user_id=user_id, create_date=i.get('date_time'))
                    if click_show_list:
                        click_show_obj.update(zhanxianliang=i.get('show_num').replace(',', ''), dianjiliang=i.get('click_num').replace(',', ''))
                for i in shoulu_list:
                    show_lu_obj = models.user_statistics.objects.filter(belong_user_id=user_id, create_date=i.get('shoulu_date'))
                    if show_lu_obj:
                        show_lu_obj.update(admin_shoulu=i.get('shoulu_count').replace('条', '').strip())
            response.code = 200
            response.msg = '更新完成'

        # selenium 返回后台报错数据
        elif oper_type == 'errorTask':
            print('request.POST====> ', request.POST)
            user_id = request.POST.get('user_id')
            if user_id:
                print('========================返回报错数据-===============================', user_id)
                userObj = models.xzh_userprofile.objects.filter(id=user_id)
                if userObj:
                    userObj.update(xiong_zhang_hao_admin_select_time=None)
        else:
            response.code = 402
            response.msg = '请求异常'

    else:
        redis_rc = redis.Redis(host='redis_host', port=6379, db=4, decode_responses=True)

        # 查询所有用户七天发布文章 保存redis 百度收录
        if oper_type == 'baidu_shoulu_situation':
            now = datetime.datetime.now()
            nowDateTime = now.strftime('%Y-%m-%d %H:%M:%S')                             # 当前时间为结束时间
            time_Y_M_D = (now + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
            sevenTime = (now - datetime.timedelta(days=6)).strftime('%Y-%m-%d 00:00:00')  # 当前时间减去六天 为开始时间
            print('time_Y_M_D================> ',time_Y_M_D, sevenTime, nowDateTime)
            q = Q()
            q.add(Q(create_date__gte=sevenTime) & Q(create_date__lte=nowDateTime), Q.AND)
            q.add(Q(select_tongji_shoulu_time__lt=time_Y_M_D) | Q(select_tongji_shoulu_time__isnull=True), Q.AND)
            q.add(Q(belongToUser__role_id=61) & Q(belongToUser__website_backstage_appid__isnull=False), Q.AND)
            print('q===> ',q)
            articleObjs = models.xzh_article.objects.filter(q)
            if articleObjs:
                for articleObj in articleObjs:
                    articleObj.select_tongji_shoulu_time = time_Y_M_D
                    articleObj.save()
                    data_list = {
                        'url':articleObj.back_url,
                        'user_id':articleObj.belongToUser_id,
                        'create_date':articleObj.create_date.strftime('%Y-%m-%d'),
                    }
                    redis_rc.lpush('baidu_shoulu_wenzhang', data_list)
                print('articleObjs.count()======================> ',articleObjs.count())
                response.code = 200
                response.msg = '获取数据完成'
            else:
                response.code = 301
                response.msg = '无匹配数据'

        # 百度收录获取任务
        elif oper_type == 'getTask':
            len_baidu_shoulu_wenzhang = redis_rc.llen('baidu_shoulu_wenzhang')
            # print('len_baidu_shoulu_wenzhang==>', len_baidu_shoulu_wenzhang)
            points = request.GET.get('points')
            response.code = 200
            flag = False
            task_keyword = ''
            count = 0
            if len_baidu_shoulu_wenzhang > 0:
                flag = True
                count = len_baidu_shoulu_wenzhang
                if points:
                    task_keyword = redis_rc.lpop('baidu_shoulu_wenzhang')
            else:
                response.code = 500
                response.msg = '无任务'
            response.data = {
                'task_keyword': task_keyword,
                'flag': flag,
                'count':count
            }

        # 熊掌号后台数据 cookie  ×
        elif oper_type == 'xiongzhanghaoTask':
            q = Q()
            q.add(Q(role_id=61) & Q(website_backstage_appid__isnull=False) & Q(xiong_cookie__isnull=False) & Q(xiong_token__isnull=False), Q.AND)
            objs = models.xzh_userprofile.objects.filter(q)
            for obj in objs:
                appid = obj.website_backstage_appid
                xiong_cookie = obj.xiong_cookie
                xiong_token = obj.xiong_token
                if appid and xiong_cookie and xiong_token:
                    now_date = datetime.datetime.now()
                    nowDate = now_date.strftime('%Y-%m-%d')
                    user_id = obj.id

                    data = {}
                    for i in xiong_cookie.strip().split(';'):
                        key = i.split('=')[0]
                        value = i.strip(key + '=')
                        data[key] = value
                    cookies = data

                    print('=============================================测试cookie是否过期======================================================')
                    now_zhishu_url = 'https://xiongzhang.baidu.com/account/exp/current?ajax=1&officeId={appid}&bdstoken={xiong_token}'.format(
                        xiong_token=xiong_token,
                        appid=appid
                    )
                    now_zhishu_ret = requests.get(now_zhishu_url, cookies=cookies)
                    print(now_zhishu_ret.json())
                    if '暂无权限' in now_zhishu_ret.json().get('msg'):
                        print('=============cookie过期', user_id)

                    else:
                        print('=============================================熊掌号指数=================================================================')
                        zhishu_url = 'https://xiongzhang.baidu.com/account/exp/trend?ajax=1&officeId={appid}&bdstoken={xiong_token}&day=30'.format(
                            xiong_token=xiong_token,
                            appid=appid
                        )
                        zhishu_ret = requests.get(zhishu_url, cookies=cookies)
                        if zhishu_ret.json():
                            zhishu_data = zhishu_ret.json().get('data').get('list')
                            now_Y = now_date.strftime('%Y')       # 年
                            for i in zhishu_data:
                                zhishu_date = now_Y + '-' + i.get('date')
                                zhishu_num = i.get('exp')
                                zhishuObj = models.user_statistics.objects.filter(belong_user_id=user_id, create_date=zhishu_date)
                                if zhishuObj:
                                    zhishuObj.update(zhishu=zhishu_num)

                        print('=============================================当前指数====================================================================')
                        now_zhishu_ret = requests.get(now_zhishu_url, cookies=cookies)
                        now_zhishu_data = now_zhishu_ret.json().get('data').get('exp')
                        now_zhishu_obj = models.user_statistics.objects.filter(belong_user_id=user_id, create_date=nowDate)
                        if now_zhishu_obj and now_zhishu_data:
                            now_zhishu_obj.update(zhishu=now_zhishu_data)

                        print('=============================================熊掌号点展量=====================================================================')
                        dianzhan_url = 'https://ziyuan.baidu.com/xzh/analysis/stat?appid={appid}&type=dispClickAll&start=&end=&period=week'.format(appid=appid)
                        dianzhan_ret = requests.get(dianzhan_url, cookies=cookies)
                        if dianzhan_ret.json():
                            data = dianzhan_ret.json()
                            totalClickAll = data.get('totalClickAll')
                            totalDisplayAll = data.get('totalDisplayAll')
                            sticsObjs = models.user_statistics.objects.filter(belong_user_id=user_id,create_date=nowDate)
                            sticsObjs.update(
                                zhanxianliang=totalDisplayAll,
                                dianjiliang=totalClickAll
                            )
                            ret_list = data.get('list')
                            for i in ret_list:
                                # click_show_proportion= i.get('pecent')           # 点展比
                                click_num = i.get('fullDayClick')   # 点击量
                                show_num = i.get('fullDayDisplay')   # 展现量
                                date_time = i.get('date')             # 时间
                                sticsObj = models.user_statistics.objects.filter(belong_user_id=user_id, create_date=date_time)
                                if sticsObj:
                                    sticsObj.update(zhanxianliang=show_num, dianjiliang=click_num)

                        print('=============================================熊掌号后台收录=======================================================================')
                        admin_shoulu_url = 'https://ziyuan.baidu.com/xzh/analysis/stat?appid={appid}&type=commitInfo&start=&end=&period=week'.format(appid=appid)
                        admin_shoulu_ret = requests.get(admin_shoulu_url, cookies=cookies)
                        if admin_shoulu_ret.json():
                            data_list = admin_shoulu_ret.json().get('list')
                            for i in data_list:
                                admin_shoulu_date = i.get('date')
                                shoulu_num = i.get('qualitySuccessSum')
                                admin_shoulu_obj = models.user_statistics.objects.filter(belong_user_id=user_id, create_date=admin_shoulu_date)
                                if admin_shoulu_obj:
                                    admin_shoulu_obj.update(admin_shoulu=shoulu_num)

            response.code = 200
            response.msg = '查询成功'

        # selenium 获取任务
        elif oper_type == 'seleniumGetTask':
            q = Q()
            now = datetime.datetime.now()
            time_Y_M_D = (now - datetime.timedelta(hours=2)).strftime('%Y-%m-%d %H:%M:%S')
            q.add(Q(role_id=61) & Q(website_backstage_appid__isnull=False) & Q(
                xiong_zhang_hao_pwd__isnull=False) & Q(xiong_zhang_hao_user__isnull=False), Q.AND)
            q.add(Q(xiong_zhang_hao_admin_select_time__isnull=True) | Q(xiong_zhang_hao_admin_select_time__lte=time_Y_M_D), Q.AND)
            objs = models.xzh_userprofile.objects.filter(q)
            objCount = objs.count()
            if objs:
                obj = objs[0]
                obj.xiong_zhang_hao_admin_select_time = now.strftime('%Y-%m-%d %H:%M:%S')
                obj.save()

                xiong_zhang_hao_pwd = obj.xiong_zhang_hao_pwd
                xiong_zhang_hao_user = obj.xiong_zhang_hao_user
                user_id = obj.id
                data_dict = {
                    'xiong_zhang_hao_user':xiong_zhang_hao_user,
                    'xiong_zhang_hao_pwd':xiong_zhang_hao_pwd,
                    'user_id':user_id,
                }

                response.code = 200
                response.msg = '查询成功'
                response.data = {
                    'objCount':objCount,
                    'retData':data_dict
                }
            else:
                response.code = 301
                response.msg = '无任务'
        else:
            response.code = 402
            response.msg = '请求异常'

    return JsonResponse(response.__dict__)









