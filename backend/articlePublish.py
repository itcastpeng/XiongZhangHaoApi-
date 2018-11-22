import requests, json
from bs4 import BeautifulSoup
from backend.lianzhongDama import LianZhongDama
import time

class DeDe(object):
    def __init__(self, domain, home_path, userid, pwd, cookies=None):
        self.requests_obj = requests.session()
        # self.domain = 'http://www.scgcyy.com'
        # self.home_url = self.domain + '/drqaz'

        self.userid = userid
        self.pwd = pwd
        self.domain = domain
        self.home_url = self.domain + home_path
        self.cookies = cookies

    def login(self):
        if self.cookies:
            self.is_login()
            return self.cookies
        login_url = self.home_url + '/login.php'
        print('login_url=====================> ',login_url)
        url = self.home_url + '/login.php?gotopage=%2Fdrqaz%2F'

        ret = self.requests_obj.get(url)
        soup = BeautifulSoup(ret.text, 'lxml')
        gotopage = soup.find('input', attrs={'name': 'gotopage'}).attrs.get('value')
        dopost = soup.find('input', attrs={'name': 'dopost'}).attrs.get('value')
        adminstyle = soup.find('input', attrs={'name': 'adminstyle'}).attrs.get('value')
        # print(gotopage, dopost, adminstyle)
        soup = BeautifulSoup(ret.text, 'lxml')
        yzm = ''
        while True:
            try:
                img_src = soup.find('img', id='vdimgck').attrs.get('src')
                img_url = self.domain + img_src.replace('..', '')

                ret = self.requests_obj.get(img_url)

                # ret.encoding = 'utf8'
                with open('yzm.jpg', 'wb') as f:
                    f.write(ret.content)

                obj = LianZhongDama()
                yzm = obj.get_yzm('yzm.jpg')
                print('yzm -->', yzm)
                # yzm = input('输入验证码 >>>')
                break
            except AttributeError:
                break

        post_data = {
            'gotopage': gotopage,
            'dopost': dopost,
            'adminstyle': adminstyle,
            'validate': yzm,
            'userid': self.userid,
            'pwd': self.pwd,
        }
        ret = self.requests_obj.post(login_url, data=post_data)
        # print('ret.text----------->',ret.text)
        # print('self.requests_obj.cookies---------> ',self.requests_obj.cookies)
        # print('self.requests_obj.cookies---------> ',self.requests_obj.headers)
        cookies = requests.utils.dict_from_cookiejar(self.requests_obj.cookies)
        self.cookies = cookies
        print('cookies============> ',cookies)
        return cookies

    # 判断是否登录
    def is_login(self):
        url = self.home_url + '/index.php'
        print('判断是否登录========》 ', url, self.cookies)
        ret = self.requests_obj.get(url, cookies=self.cookies)
        # print(ret.text)
        if "登录" in ret.text:
            self.cookies = ''    # cookie清除掉
            self.login()

    # 获取栏目信息
    def getClassInfo(self):
        url = self.home_url + '/article_add.php'
        ret = self.requests_obj.get(url, cookies=self.cookies)
        # print(ret.text)
        soup = BeautifulSoup(ret.text, 'lxml')

        select_tag = soup.find('select', id='typeid')
        print('select_tag -->', select_tag)
        retData = []
        for option_tag in select_tag.find_all('option'):
            class_id = int(option_tag.attrs.get('value'))
            class_name = option_tag.get_text()
            if class_id == 0:
                continue

            retData.append([class_id, class_name])

        return retData

    # 判断标题是否可用
    def article_test_title(self, title):
        print("判断标题是否可用")
        url = self.home_url + '/article_test_title.php?t={title}'.format(title=title)
        # print('url -->', url)
        ret = self.requests_obj.get(url, cookies=self.cookies)

        if '存在标题' in ret.text.strip():
            print('标题已存在')
            return False
        return True

    # 发布文章
    def sendArticle(self, data, title):
        if self.article_test_title(data.get('title')):
            # print('增加文章')
            url = self.home_url + '/article_add.php'
            print('发布url==================> ',url)
            print('发布data------------------> ', data)
            ret = self.requests_obj.post(url, data=data, cookies=self.cookies)
            # print('========> ', ret.text.strip())
            if '无法解析文档' not in ret.text.strip():
                if '成功发布文章' in ret.text:
                    soup = BeautifulSoup(ret.text, 'lxml')
                    aid_href = soup.find('a', text='更改文章').get('href')    # 文章id
                    aid = aid_href.split('?')[1].split('&')[0].split('aid=')[-1]
                    huilian_href = soup.find('a', text='查看文章').get('href')    # 文章id
                    huilian = self.domain + huilian_href
                    # print('huilian================> ',huilian)
                    time.sleep(0.5)
                    ret = self.requests_obj.get(huilian, cookies=self.cookies)
                    encode_ret = ret.apparent_encoding
                    # print('encode_ret===========', encode_ret)
                    if encode_ret == 'GB2312':
                        ret.encoding = 'gbk'
                    else:
                        ret.encoding = 'utf-8'
                    print('title==============> ',title)
                    # print(ret.text)
                    if title in ret.text:
                        print('huilian=============> ', huilian)
                        # 更新文档url
                        # updateWordUrl = '{home_url}/task_do.php?typeid={cid}&aid={aid}&dopost=makeprenext&nextdo=makeindex,makeparenttype'.format(
                        #     home_url=self.home_url,
                        #     aid=aid,
                        #     cid=cid
                        # )
                        # # 更新主页url
                        # updateIndexUrl = '{home_url}/task_do.php?f=0&typeid={cid}&aid={aid}&dopost=makeindex&nextdo=makeparenttype'.format(
                        #     home_url=self.home_url,
                        #     aid=aid,
                        #     cid=cid
                        # )

                        # if objCookies:
                        #     ret1 = self.requests_obj.get(updateWordUrl, cookies=objCookies)
                        #     print('ret1--> ',ret1, ret1.url)
                        #
                        #     ret2 = self.requests_obj.get(updateIndexUrl, cookies=objCookies)
                        #     print('ret2-=--> ',ret2, ret2.url)
                        #
                        # else:
                        #     print('===============else=============else')
                        #     ret1 = self.requests_obj.get(updateWordUrl)
                        #     print('ret1--> ', ret1, ret1.url)
                        #     ret2 = self.requests_obj.get(updateIndexUrl)
                        #     print('ret2-=--> ', ret2, ret2.url)
                        print('’发布成功=========================发布成功===================发布成功')
                        return {
                            'huilian':huilian,
                            'aid':aid,
                            'code':200
                            # 'code':305
                            }
                    else:
                        print('=============没有查到该标题=============')
                        return {
                            'code':301,
                        }
                else:
                    print('’发布失败=========================发布失败===================发布失败 500')
                    return {
                        'huilian':'',
                         'code':500
                        }
            else:
                print('’模板文件不存在, 请选择子级菜单=========================模板文件不存在, 请选择子级菜单===================模板文件不存在, 请选择子级菜单 305')
                return {
                    'huilian': '',
                    'code': 305
                }
        else:
            print('’发布失败=========================发布失败===================发布失败 300')
            return {
                    'huilian':'',
                     'code':300
                    }

    # 查询是否审核通过
    def getArticleAudit(self, url, id, aid):
        ret = self.requests_obj.get(url, cookies=self.cookies)
        encode_ret = ret.apparent_encoding
        print('encode_ret===========', encode_ret)
        if encode_ret == 'GB2312':
            ret.encoding = 'gbk'
        else:
            ret.encoding = 'utf-8'
        soup = BeautifulSoup(ret.text, 'lxml')
        center_divs_all = soup.find_all('tr', align='center')
        status = False
        for center_div in center_divs_all:
            if int(center_div.attrs.get('height') )== 26:
                if int(center_div.find_all('td')[0].get_text().strip()) == int(aid):
                    auditHtml = center_div.find_all('td')[6].get_text().strip()
                    if auditHtml == '已生成':
                        status = True
                        break
        return id, status

    # 查询文章是否被删除
    def deleteQuery(self, url):
        print('00000000000000000000> ', self.cookies)
        # url = url + '&pageno=1'
        ret = self.requests_obj.get(url, cookies=self.cookies)
        print('查询文章是否被删除==url==url====url===>', url)
        encode_ret = ret.apparent_encoding
        print('encode_ret===========', encode_ret)
        if encode_ret == 'GB2312':
            ret.encoding = 'gbk'
        else:
            ret.encoding = 'utf-8'
        soup = BeautifulSoup(ret.text, 'lxml')
        next_href = soup.find_all('a')
        for i in next_href:
            print('next_href==========> ',i)







        # flag = False
        # yema = 0
        # page_num = soup.find('div', class_='pagelistbox')
        # print('page_num--------> ',page_num)
        # if page_num:
        #     page = page_num.find('span').get_text()
        #     print('page--------> ',page)
        #     if page:
        #         yema = page.split('页')[0].split('共')[1]
        #         print('yema--------> ',yema)
        #         center_divs_all = soup.find_all('tr', align='center')
        #         for center_div in center_divs_all:
        #             if '“北京长虹医院”千万别忽视急性前列腺炎的危害' in center_div.get_text():
        #                 flag = True
        #     else:
        #         flag = 1
        # else:
        #     flag = 1
        # return flag, int(yema)


# if __name__ == '__main__':
#     domain = 'http://www.bjwletyy.com'
#     home_path = '/wladmin'
#     userid = 'zhidao'
#     pwd = 'zhidao2018'
#     cookies = { 'PHPSESSID': 'oljb8k6gmtn4o96pipo4efcgpk', 'DedeUserID': '3'}
#     obj = DeDe(domain, home_path, userid, pwd, cookies)
#     obj.login()
#     print('obj.cookies -->', obj.cookies)
#
#     class_data = obj.getClassInfo()

