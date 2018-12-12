from backend.articlePublish import DeDe, PcV9
import json, requests, datetime
from urllib.parse import urlparse
from api.public.token import start
from random import randint
from django.shortcuts import render, render_to_response

# 发布文章
def publishedArticles():
    params = start()
    # url = 'http://127.0.0.1:8003/api/articleScriptOper/sendArticle?user_id=17&timestamp=123&rand_str=4297f44b13955235245b2497399d7a93'
    # ret = requests.get(url)
    url = 'http://xiongzhanghao.zhugeyingxiao.com:8003/api/articleScriptOper/sendArticle'
    ret = requests.get(url, params=params)
    # print('=ret.text=========> ',ret.text)
    resultData = json.loads(ret.text).get('data')
    if resultData:
        print('===========================开始发布文章==========================================开始发布文章=========================')
        o_id =  resultData.get('o_id')
        website_backstage = resultData.get('website_backstage')
        result_data = {}

        # 织梦后台
        if int(website_backstage) == 1:
            website_backstage_url = resultData.get('website_backstage_url').strip()
            # print('====================================website_backstage_url', website_backstage_url)
            if 'http' in website_backstage_url:
                url = urlparse(website_backstage_url)
                domain = 'http://' + url.hostname + '/'
                home_path = website_backstage_url.split(domain)[1].replace('/', '')
            else:
                web_url =  website_backstage_url.split('/')[0] + '/'
                domain = 'http://' + web_url
                home_path = website_backstage_url.split(web_url)[1].replace('/', '')
            userid = resultData.get('website_backstage_username')
            pwd = resultData.get('website_backstage_password')
            typeid = resultData.get('typeid')
            cookie = ''
            if resultData.get('cookies'):
                cookie = eval(resultData.get('cookies'))
            title = resultData.get('title')
            picname = resultData.get('picname')
            summary = resultData.get('summary')
            content =  resultData.get('content')
            print('00000000000000000000000000website_backstage_url00000000000000000000000>',summary)
            if 'http://m.chyy120.com/netadmin' in website_backstage_url or 'http://wap.tysgmr.com/dede' in website_backstage_url or 'http://m.oy120.com/@qz120_@' in website_backstage_url or 'http://xzh.nk-hospital.mobi' in website_backstage_url:  # 判断utf8 还是 gbk
                print('------==========----------------------GBK')
                title =  resultData.get('title').encode('gbk')
                summary =  resultData.get('summary').encode('gbk')
                content =  resultData.get('content').encode('gbk')

            article_data = {
                "channelid": "1",  # 表示普通文章
                "dopost": "save",  # 隐藏写死属性
                "title": title,  # 文章标题
                "weight": "1033",  # 权重
                "typeid": typeid,  # 栏目id
                "autokey": "1",  # 关键字自动获取
                "description": summary,  # 描述
                "remote": "1",  # 下载远程图片和资源
                "autolitpic": "1",  # 提取第一个图片为缩略图
                "sptype": "hand",  # 分页方式 手动
                "spsize": "5",
                "body": content,
                "notpost": "0",
                "click": randint(100, 200),
                "sortup": "0",
                "arcrank": "0",
                "money": "0",
                "pubdate": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "ishtml": 1,
                "imageField.x": "30",
                "imageField.y": "12",

            }
            articlePicName = ''
            if picname:
                if 'http://www.zjnbsznfk120.com' in picname:
                    articlePicName = picname.split('http://www.zjnbsznfk120.com')[-1]
                elif 'http://www.zjsznnk.com' in picname:
                    articlePicName = picname.split('http://www.zjsznnk.com')[-1]
            article_data['picname'] = articlePicName
            if 'http://m.oy120.com' in website_backstage_url:
                article_data['litpic'] = '(binary)'
                article_data['color'] = ''
                article_data['weight'] = '5693'
                article_data['keywords'] = ''
                article_data['filename'] = ''
                article_data['redirecturl'] = ''
                article_data['voteid'] = ''
                article_data['redirecturl'] = ''
                article_data['tags'] = ''
                article_data['shorttitle'] = ''
                article_data['source'] = ''
                article_data['writer'] = ''
                article_data['typeid2'] = ''
                article_data['dede_addonfields'] = ''
                article_data['templet'] = ''
            # print('domain, home_path, userid, pwd, cookie-----------------> ',domain, home_path, userid, pwd, cookie)
            DeDeObj = DeDe(domain, home_path, userid, pwd, cookie)
            cookie = DeDeObj.login()
            # print("===============-----9999999999999999999999999999999999900-----------> ",article_data)
            resultData = DeDeObj.sendArticle(article_data, resultData.get('title'), picname) # picname缩略图本地上传

            result_data = {
                'resultData': json.dumps(resultData),
                'o_id': o_id
            }

        # PcV9后台
        elif int(website_backstage) == 2:
            print('PcV9后台======================PcV9后台发布文章========================PcV9后台发布文章')
            userid = resultData.get('website_backstage_username')
            pwd = resultData.get('website_backstage_password')
            cookie = resultData.get('cookies')
            title = resultData.get('title')
            picname = resultData.get('picname')
            summary = resultData.get('summary')
            content = resultData.get('content')
            typeid = resultData.get('typeid')
            PcV9Obj = PcV9(userid, pwd, cookie)
            cookies, pc_hash = PcV9Obj.login()
            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            data = {
                'info[thumb]': '',
                'info[relation]': '',
                'info[inputtime]': now,
                'info[islink]': 0,
                'info[template]': '',
                'info[allow_comment]': 1,
                'info[readpoint]': '',
                'info[paytype]': 0,
                'info[catid]': typeid,
                'info[title]': title,
                'style_color': '',
                'style_font_weight': '',
                'info[keywords]': '',
                'info[copyfrom]': '',
                'copyfrom_data': 0,
                'info[description]': summary,
                'info[content]': content,
                'page_title_value': '',
                'add_introduce': 1,
                'introcude_length': 200,
                'auto_thumb': 1,
                'auto_thumb_no': 1,
                'info[paginationtype]': 0,
                'info[maxcharperpage]': 10000,
                'info[posids][]': -1,
                'info[groupids_view]': 1,
                'info[voteid]': '',
                'dosubmit': '保存后自动关闭',
            }
            resultData = PcV9Obj.sendArticle(data, title, pc_hash)
            result_data = {
                'resultData': json.dumps(resultData),
                'o_id': o_id
            }

        # FTP
        elif int(website_backstage) == 3:
            title = resultData.get('title')
            summary = resultData.get('summary')
            content = resultData.get('content')

            innerHtml = """                       
                 <dl class="jj">
                 <h3 style="text-align: center">{title}</h3>
                        <div><p>{summary}</p></div> 
                        <div class="jj2"><p>{content}</p></div>
                </dl>
                """.format(title=title, summary=summary, content=content)

            # 开始HTML
            headHTML = """
            
                <!doctype html>
                <html>
                <head>
                <meta charset="utf-8">
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
                <script type="application/ld+json">
                    {
                        "@context": "https://ziyuan.baidu.com/contexts/cambrian.jsonld",
                        "@id": "http://m.dracne.net/zj.html",
                        "appid": "1619456659599101",
                        "title": "Dr.acne痘院长团队",
                        "pubDate": "2018-12-01T08:00:01"
                    }
                </script>
                <script src="//msite.baidu.com/sdk/c.js?appid=1619456659599101"></script>
                </head>
                <body>
                
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
                </dl>                
               """

            # 结束HTML
            tailHtml = """
                    <dl class="dy">
                        <h3>连锁分布<span>The distribution chain</span></h3>
                        <div class="dy1"><img src="http://m.dracne.net/images/imgx29.jpg"></div>
                        <div class="dy2"><a href="http://m.dracne.net/ls.html">连锁详情</a><a href="https://rgbk2.kuaishang.cn/bs/im.htm?cas=59154___718795&fi=70539&ism=1&ref=m.dracne.cn" class="a1">预约附近门店</a></div>
                    </dl>
                    <script language="javascript" type="text/javascript" src="http://m.dracne.net/images/footer.js"></script>
                    </body>
                    </html>
                        """

            HTML = headHTML + innerHtml + tailHtml

            # return render(request, 'index.html', {
            #     'my_message': objs.DomainNameText
            # })

            huilian = ''
            resultData = {
                'huilian': huilian,
                'aid': 0,
                'code': 200
            }
            result_data = {
                'resultData': json.dumps(resultData),
                'o_id': o_id
            }


        print('result_data==============================> ',resultData)
        # url = 'http://127.0.0.1:8003/api/articleScriptOper/sendArticleModels?user_id=17&timestamp=123&rand_str=4297f44b13955235245b2497399d7a93'
        url = 'http://xiongzhanghao.zhugeyingxiao.com:8003/api/articleScriptOper/sendArticleModels?user_id=44&timestamp=1542788198850&rand_str=86b24054d91240d9559e369296af06cd'
        requests.post(url, data=result_data)


# if __name__ == '__main__':
#     publishedArticles()



