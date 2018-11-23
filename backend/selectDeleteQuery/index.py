


from xiongzhanghao.publicFunc import Response
from django.http import JsonResponse
from api.public.token import start
from urllib.parse import urlparse
from backend.articlePublish import DeDe




# 判断客户页面 该文章是否删除
def electDeleteQuery():
    params = start()  # 获取token
    response = Response.ResponseObj()

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


