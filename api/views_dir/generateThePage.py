from xiongzhanghao import models
from xiongzhanghao.publicFunc import Response
from xiongzhanghao.publicFunc import account
from django.http import JsonResponse
from django.shortcuts import render, render_to_response
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from xiongzhanghao.publicFunc.condition_com import conditionCom
from xiongzhanghao.forms.article import AddForm, UpdateForm, SelectForm
import json, datetime, requests, os
from bs4 import BeautifulSoup
from urllib.parse import urlparse


# 特殊用户 生成页面
@csrf_exempt
@account.is_token(models.xzh_userprofile)
def specialUserGenerateThePage(request):
    response = Response.ResponseObj()
    objs = models.xzh_article.objects.filter(article_status=6, belongToUser__userType=2)
    for obj in objs:
        print('obj.id----------> ',obj.id)
        if obj.back_url:
            website_backstage_url = obj.belongToUser.website_backstage_url
            url = urlparse(website_backstage_url)
            if url.hostname:
                domain = 'http://' + url.hostname
            else:
                domain = 'http://' + website_backstage_url.split('/')[0]
            print('website_backstage_url==========> ',website_backstage_url)
            ret = requests.get(obj.back_url)
            encode_ret = ret.apparent_encoding
            if encode_ret == 'GB2312':
                ret.encoding = 'gbk'
            else:
                ret.encoding = 'utf-8'
            soup = BeautifulSoup(ret.text, 'lxml')
            result_data = ret.text

            a_tags_all = soup.find_all('a')  # 替换a标签
            for a_tag in a_tags_all:
                a_href = a_tag.attrs.get('href')
                if a_href and 'http' not in a_href and len(a_href) > 3 and '/' in a_href:
                    href = domain + a_tag.attrs.get('href')
                    result_data = result_data.replace(a_href, href)

            script_tags_all = soup.find_all('script')  # script替换js
            for script_tag in script_tags_all:
                src = script_tag.attrs.get('src')
                if src and 'http' not in src and len(src) > 3 and '/' in src:
                    href = domain + src
                    result_data = result_data.replace(src, href)

            img_tags_all = soup.find_all('img')  # img替换src
            for img_tag in img_tags_all:
                src = img_tag.attrs.get('src')
                if src and 'http' not in src and len(src) > 3 and '/' in src:
                    href = domain + src
                    result_data = result_data.replace(src, href)

            link_tags_all = soup.find_all('link')
            for link_tag in link_tags_all:
                link_href = link_tag.attrs.get('href')
                if link_href and 'http' not in link_href and len(link_href) > 3 and '/' in link_href:
                    href = domain + link_href
                    result_data = result_data.replace(link_href, href)

            head_div = soup.find('head')
            body_div = soup.find('body')
            title = ''
            if body_div.find('title'):
                title = body_div.find('title').get_text()
            elif body_div.find('h1'):
                title = body_div.find('h1').get_text()

            script_json = head_div.find('script', type='application/ld+json')
            create_date = obj.create_date.strftime('%Y-%m-%dT%H:%M:%S')

            appid = obj.belongToUser.website_backstage_appid

            print('id, appid, articlePublishedDate============> ',id, appid, title, create_date)

            domain = obj.belongToUser.secondaryDomainName
            back_url = domain + '{}.html'.format(obj.id)
            insert_script = """
                <script type="application/ld+json">
                    {
                        "@context": "https://ziyuan.baidu.com/contexts/cambrian.jsonld",
                        "@id": "%s",
                        "appid": %s,
                        "title": "%s",
                        "images": [
                            "http://m.meilianchen.cn/new/images/sy.jpg"
                        ],
                        "pubDate": "%s"
                    }
                </script>
                <script src="//msite.baidu.com/sdk/c.js?appid=%s"></script>
                </head>
                """ % (back_url, appid, title, create_date, appid)

            if not script_json:
                result_data = result_data.replace('</head>', insert_script)
            else:
                result_data = result_data.replace(str(script_json), insert_script)


            # back_url = 'article/{}.html'.format(obj.id)
            obj.article_status = 4
            obj.back_url = back_url
            obj.DomainNameText = result_data  # 二级域名内容
            # obj.article_status = 0  # 测试
            obj.save()
    response.code = 200
    response.msg = '生成完成'
    return JsonResponse(response.__dict__)


# 查询二级域名
@csrf_exempt
def SearchSecondaryDomainName(request, article):
    response = Response.ResponseObj()
    print('article_id============> ', article)
    article_id = article.split('.html')[0]
    objs = models.xzh_article.objects.get(id=article_id)
    if objs:
        return render(request, 'index.html', {
            'my_message': objs.DomainNameText
        })
    else:
        response.code = 301
        response.msg = '无此id'
        return JsonResponse(response.__dict__)
