import requests, json
from bs4 import BeautifulSoup
from backend.lianzhongDama import LianZhongDama


class DeDe(object):
    def __init__(self, domain, home_path):
        self.requests_obj = requests.session()
        # self.domain = 'http://www.scgcyy.com'
        # self.home_url = self.domain + '/drqaz'

        self.domain = domain
        self.home_url = self.domain + home_path

    def login(self, obj, operType):
        if operType == 'getcolumn':
            userid = obj.website_backstage_username
            pwd = obj.website_backstage_password
        else:
            userid = obj.belongToUser.website_backstage_username
            pwd = obj.belongToUser.website_backstage_password
        login_url = self.home_url + '/login.php'

        url = self.home_url + '/login.php?gotopage=%2Fdrqaz%2F'
        ret = self.requests_obj.get(url)

        soup = BeautifulSoup(ret.text, 'lxml')
        gotopage = soup.find('input', attrs={'name': 'gotopage'}).attrs.get('value')
        dopost = soup.find('input', attrs={'name': 'dopost'}).attrs.get('value')
        adminstyle = soup.find('input', attrs={'name': 'adminstyle'}).attrs.get('value')

        soup = BeautifulSoup(ret.text, 'lxml')
        yzm = ''
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

        except AttributeError:
            pass

        post_data = {
            'gotopage': gotopage,
            'dopost': dopost,
            'adminstyle': adminstyle,
            'validate': yzm,
            'userid': userid,
            'pwd': pwd,
        }
        self.requests_obj.post(login_url, data=post_data)
        # print('self.requests_obj.cookies---------> ',self.requests_obj.cookies)
        # print('self.requests_obj.cookies---------> ',self.requests_obj.headers)
        cookies = requests.utils.dict_from_cookiejar(self.requests_obj.cookies)

        print('cookies -------------->', cookies)
        return cookies
        # for i in self.requests_obj.cookies:
        #     print(i, type(i))

    # 获取栏目信息
    def getClassInfo(self, objCookies=None):
        url = self.home_url + '/article_add.php'
        if objCookies:
            ret = self.requests_obj.get(url, cookies=objCookies)
        else:
            ret = self.requests_obj.get(url)
        soup = BeautifulSoup(ret.text, 'lxml')

        select_tag = soup.find('select', id='typeid')
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
        ret = self.requests_obj.get(url)
        if '存在标题' in ret.text.strip():
            print('标题已存在')
            return False
        return True

    # 发布文章
    def sendArticle(self, data, objCookies=None):
        if self.article_test_title(data.get('title')):
            # print('增加文章')
            url = self.home_url + '/article_add.php'
            if objCookies:
                print('-----------------增加文章', objCookies)
                ret = self.requests_obj.post(url, data=data, cookies=objCookies)
            else:
                ret = self.requests_obj.post(url, data=data)

            print(ret.text)
            if '成功发布文章' in ret.text:
                soup = BeautifulSoup(ret.text, 'lxml')
                aid_href = soup.find('a', text='更改文章').get('href')    # 文章id
                aid = aid_href.split('?')[1].split('&')[0].split('aid=')[-1]
                huilian = self.home_url + '/news/{}.html'.format(aid)

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

                return {
                    'huilian':huilian,
                     'code':200
                    }
            else:
                return {
                    'huilian':'',
                     'code':500
                    }
        else:
            return {
                    'huilian':'',
                     'code':300
                    }
# if __name__ == '__main__':
#     domain = 'http://www.bjwletyy.com'
#     home_path = '/wladmin'
#     userid = 'zhidao'
#     pwd = 'zhidao2018'
#     obj = DeDe(domain, home_path)
#     obj.login(userid, pwd)
#     class_data = obj.getClassInfo()

