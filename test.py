from xiongzhanghao.publicFunc import Response
from django.http import JsonResponse
from api.public.token import start
from urllib.parse import urlparse
from backend.articlePublish import DeDe



# 判断客户页面 该文章是否删除
def deleteQuery():
    params = start()  # 获取token
    response = Response.ResponseObj()
    # objs = models.xzh_article.objects.filter(article_status__in=[2, 4, 5])
    # objs = models.xzh_article.objects.filter(id=20)
    # for obj in objs:

    website_backstage_url = 'http://wap.tysgmr.com/dede'
    url = urlparse(website_backstage_url)
    if url.hostname:
        domain = 'http://' + url.hostname + '/'
        home_path = website_backstage_url.split(domain)[1].replace('/', '')
    else:
        domain = 'http://' + website_backstage_url.split('/')[0] + '/'
        home_path = website_backstage_url.split('/')[1]
    userid = 'admin123'
    pwd = 'admin'
    cookie = ''
    print('home_path--------------->? ', domain, home_path, userid, pwd, cookie)
    DeDeObj = DeDe(domain, home_path, userid, pwd, cookie)
    cookie = DeDeObj.login()
    title = '做隆鼻手术后还能化妆吗？'
    aid = 179
    if website_backstage_url[-1] == '/':
        website_backstage_url = website_backstage_url + 'content_list.php?channelid=1'
    else:
        website_backstage_url = website_backstage_url + '/content_list.php?channelid=1'
    flag = False
    page = 0
    while True:
        page +=1
        flag, yema = DeDeObj.deleteQuery(website_backstage_url + '&pageno={}'.format(page), title, aid)
        print('flag=========================> ',flag, page)
        if page >= int(yema) + 1:
            break
        if flag or flag == '1':
            break




# if __name__ == '__main__':
#     deleteQuery()

# p = [{'aid': '119', 'title': '“北京长虹医院”婚k后一直有遗精 该引起重视了'}, {'aid': '148', 'title': '北京长虹告诉你前列腺肿大有哪些饮食禁忌'}, {'aid': '95', 'title': '包皮手术前要了解这些事'}]
# o = []
# for i in p:
#     print(i)
#     o.append(i)

import requests, json
from bs4 import BeautifulSoup

requests_obj = requests.session()
# url1 = 'https://author.baidu.com/profil'
url1 = 'https://author.baidu.com/profile?context={%22from%22:%22dusite_sresults%22,%22app_id%22:%221604474303074024%22}&cmdType=&pagelets=root&reqID=0&ispeed=1'
url = 'https://author.baidu.com/home/1604474303074024?from=dusite_sresults'

headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Mobile Safari/537.36',
    'Referer': 'https://author.baidu.com/home/1604474303074024?from=dusite_sresults',
}

# ret = requests_obj.get(url, headers=headers)
# ret1 = requests_obj.get(url1, headers=headers)
#
#
# result = ret1.text.split('BigPipe.onPageletArrive(')[1]
# result = result[:-2]
#
# html = json.loads(result)['html']
# soup = BeautifulSoup(html, 'lxml')
# interaction = soup.find('div', id='interaction')
# fans = interaction.find('div', class_='fans')
# fans_num = fans.find('span').get_text()
# print(fans_num)



# url = 'http://127.0.0.1:8003/api/addFansGetTask/getTask?user_id=17&timestamp=123&rand_str=4297f44b13955235245b2497399d7a93'
# ret = requests.get(url)
#
# print(ret.json().get('data'))

































