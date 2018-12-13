from xiongzhanghao import models
from xiongzhanghao.publicFunc import Response
from xiongzhanghao.publicFunc import account
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json, datetime, requests, os, time
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from ftplib import FTP


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


@csrf_exempt
def FTPuploadHtml(request):
    response = Response.ResponseObj()
    if request.method == 'POST':

        title = request.POST.get('title')
        summary = request.POST.get('summary')
        content = request.POST.get('content')
        o_id = request.POST.get('o_id')

        str_num = str(o_id) + str(int(time.time()))
        fileName = str_num + '.html'  # 文件名
        return_path = 'http://m.dracne.net/xiongzhanghao/{}'.format(fileName) # 回链

        article_objs = models.xzh_article.objects.filter(id=o_id)
        article_obj = article_objs[0]
        appid = article_obj.belongToUser.website_backstage_appid
        create_time = article_obj.create_date.strftime('%Y-%m-%dT%H:%M:%S')

        innerHtml = """                       
                   <dl class="jj">
                   <h3 style="text-align: center">{title}</h3>
                          <div style="padding:30px 30px 0px 30px"><p>{summary}</p></div> 
                          <div class="jj2"><p>{content}</p></div>
                  </dl>
                  """.format(title=title, summary=summary, content=content)

        # 开始HTML
        headHTML = """
                  <!doctype html>
                  <html>
                  <head>
                  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
                  <title>Dr.acne痘院长团队</title>
                  <link href="http://m.dracne.net/images/css.css" rel="stylesheet" type="text/css">
                  <link href="http://m.dracne.net/images/bottom.css" rel="stylesheet" type="text/css">
                  <script src="http://m.dracne.net/images/phonecommon.js"></script>
                  <script type="text/javascript" src="http://m.dracne.net/images/jquery-1.7.1.min.js"></script>
                  <script type="text/javascript" src="http://m.dracne.net/images/jquery-1.10.1.min.js"></script>
                  <script type="text/javascript" src="http://m.dracne.net/images/nav.js"></script>
                  <script type="text/javascript" src="http://m.dracne.net/images/tj.js"></script>
                  <meta http-equiv="Cache-Control" content="no-cache"/>
                  <meta name="viewport" content="width=device-width, minimum-scale=1.0, maximum-scale=1.0, user-scalable=no"/>
                  """

        data = """ "@context": "https://ziyuan.baidu.com/contexts/cambrian.jsonld",
                               "@id": "{return_path}",
                               "appid": "{appid}",
                               "title": "{title}",                        
                               "pubDate": "{create_time}"
                               """.format(
                                return_path=return_path,
                                appid=appid,
                                title=title,
                                create_time=create_time
                            )
        innerData = """            
                <script type="application/ld+json">
                    {
                        %s
                    }                                                         
                   """ % data

        # 熊掌号代码
        xiongzhanghaoHtml = """             
                </script>   
                <link rel="canonical" href="{back_url}"/>             
                <script src="//msite.baidu.com/sdk/c.js?appid={appid}"></script>                
              </head>
                     """.format(appid=appid, back_url=return_path)

        # body代码
        bodyHtml = """    <body>
                  <div id='header'>
                      <div id='header_memu' style='display: block;'>
                          <div id='header_memu_left'><img src='http://m.dracne.net/images/imgx1.png'></div>
                          <div id='header_menu_content'><div id='logo'><a href='http://m.dracne.cn/'><img src='http://m.dracne.net/images/imgx3.png' alt='痘院长首页'></a></div></div>
                          <div id='header_menu_right'><a href='tel:18088270124' onclick='ClickPhone()' target='_self'><img src='http://m.dracne.net/images/imgx2.png'></a></div>
                      </div>
                      <div id='header_nav_box' style='display: none;'>
                          <div id='header_nav_left' style='left: -100%;'>
                          <div id='header_nav_top'>
                              <div class='header_nav_top_close'><img src='http://m.dracne.net/images/imgx1_1.png'></div>
                              <a href='http://m.dracne.cn/'><i></i>首页〉</a>
                          </div>
                              <div id='header_nav_content'>
                                  <div class='header_nav_title'><h2><a href='http://m.dracne.net/jj.html'>About Dr.acne</a></h2></div>
                                  <div class='header_nav_title'><h2><a href='http://m.dracne.net/ls.html'>百家连锁</a></h2></div>
                                  <div class='header_nav_title'><h2><a href='http://m.dracne.net/kj.html'>核心科技</a></h2></div>
                                  <div class='header_nav_title'><h2><a href='#'>顾客保障</a></h2></div>
                                  <div class='header_nav_title'><h2><a href='http://m.dracne.net/zj.html'>美肤顾问</a></h2></div>
                                  <div class='header_nav_title'><h2><a href='https://rgbk2.kuaishang.cn/bs/im.htm?cas=59154___718795&fi=70539&ism=1&ref=m.dracne.cn'>新闻动态</a></h2></div>
                                  <div class='header_hd'>
                                      <h2 style='font-size:1.3rem;color:#fff;line-height:4.5rem;text-indent:1.6rem;'>本月活动</h2>
                                      <a class='per_activity act'><img src='http://m.dracne.net/images/hdx1.jpg' width='100%'></a>
                                  </div>
                              </div>
                          </div>
                      </div>
                  </div>
                  <dl class='ban'>
                      <div id='two_xg1' class='two_xg1'>
                          <div class='two_xg_nr1'>
                              <ul><li><a href='https://rgbk2.kuaishang.cn/bs/im.htm?cas=59154___718795&fi=70539&ism=1&ref=m.dracne.cn'><img src='http://m.dracne.net/images/banner_01.jpg'/></a></li></ul>
                              <ul><li><a href='https://rgbk2.kuaishang.cn/bs/im.htm?cas=59154___718795&fi=70539&ism=1&ref=m.dracne.cn'><img src='http://m.dracne.net/images/banner_02.jpg'/></a></li></ul>
                              <ul><li><a href='https://rgbk2.kuaishang.cn/bs/im.htm?cas=59154___718795&fi=70539&ism=1&ref=m.dracne.cn'><img src='http://m.dracne.net/images/banner_03.jpg'/></a></li></ul>
                              <ul><li><a href='https://rgbk2.kuaishang.cn/bs/im.htm?cas=59154___718795&fi=70539&ism=1&ref=m.dracne.cn'><img src='http://m.dracne.net/images/banner_04.jpg'/></a></li></ul>
                          </div>
                          <div class='two_xg_tit1'>
                              <ul>
                                  <li></li>
                                  <li></li>
                                  <li></li>
                                  <li></li>
                              </ul>
                          </div>
                      </div>
                  <script type='text/javascript'>
                      phonecommon({
                          id: '#two_xg1',
                          titkj: '.two_xg_tit1 li',
                          contkj: '.two_xg_nr1',
                          xiaoguo: 'leftauto',
                          autoplay: true,
                          cxtime: 200,
                          jgtime: 3000,
                          morenindex: 0,
                          tjclass: 'hover',
                          autopage: false,
                          leftarr: '.xiaoguo2prev',
                          rightarr: '.xiaoguo2next',
                          showpage: '.showpage',
                          arrauto: 'false',
                          startfn: null,
                          endfn: null,
                          changeload: null
                      });
                  </script>
                  </dl>          """

        # 结束HTML
        tailHtml = """
                    <dl class="dy">
                        <h3>连锁分布<span>The distribution chain</span></h3>
                        <div class="dy1"><img src="http://m.dracne.net/images/imgx29.jpg"></div>
                        <div class="dy2"><a href="http://m.dracne.net/ls.html">连锁详情</a><a href="https://rgbk2.kuaishang.cn/bs/im.htm?cas=59154___718795&fi=70539&ism=1&ref=m.dracne.cn" class="a1">预约附近门店</a></div>
                    </dl>
                    <dl class='wb'>
                        <p>24H电话咨询热线: 400-1099588                
                        <br/>地址：青年路与人民路交叉口美亚大厦1楼(必胜客旁边)</p>
                    </dl>
                  </body>
                </html>  
                """



        HTML = headHTML + innerData + xiongzhanghaoHtml + bodyHtml + innerHtml + tailHtml

        host = '61.188.39.201'
        port = 1987
        username = 'kmxzh'
        password = 'kmdyzXZH123'

        F = FTP()  # 实例化FTP对象
        F.connect(host, port)
        F.login(username, password)  # 登录


        path = 'statics/xiongzhanghao/{}'.format(fileName)

        print('path-----------> ',path)
        with open(path, 'w', encoding="utf-8") as f:
            f.write(HTML)


        # print('path======================> ',F.nlst())  # 获取当前路径下文件 返回列表

        bufsize = 1024  # 设置缓冲器大小
        F.cwd('xiongzhanghao')   # 进入熊掌号目录

        # 读取本地文件
        ft = open(path, 'rb')
        F.storbinary('STOR ' + fileName, ft, bufsize)  # 写入FTP文件
        ft.close()

        print('return_path============> ',return_path)
        response.code = 200
        response.msg = '上传成功'
        response.data = {
            'return_path':return_path
        }
    else:
        response.code = 402
        response.msg = '请求异常'
    return JsonResponse(response.__dict__)

