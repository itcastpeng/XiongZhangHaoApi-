import requests
from bs4 import BeautifulSoup

from lianzhongDama import LianZhongDama


class DeDe(object):
    def __init__(self, domain, home_path):
        self.requests_obj = requests.session()
        # self.domain = 'http://www.scgcyy.com'
        # self.home_url = self.domain + '/drqaz'

        self.domain = domain
        self.home_url = self.domain + home_path

    def login(self, userid, pwd):
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
            'userid': userid,
            'pwd': pwd,
            'validate': yzm
        }

        login_url = self.home_url + '/login.php'
        self.requests_obj.post(login_url, data=post_data)

        cookies = requests.utils.dict_from_cookiejar(self.requests_obj.cookies)

        print(cookies)
        # for i in self.requests_obj.cookies:
        #     print(i, type(i))

    # # 获取子分类信息
    # def getChildClassInfo(self, class_id):
    #     url = 'http://www.scgcyy.com/drqaz/catalog_do.php?dopost=GetSunLists&cid=' + class_id
    #     ret = self.requests_obj.get(url)
    #     print(ret.text)

    # 获取分类信息
    def getClassInfo(self):
        class_data_dict = {}
        url = self.home_url + '/article_add.php'
        ret = self.requests_obj.get(url)

        soup = BeautifulSoup(ret.text, 'lxml')

        select_tag = soup.find('select', id='typeid')
        current_level = 0
        level_list = []
        for option_tag in select_tag.find_all('option'):
            class_id = int(option_tag.attrs.get('value'))
            class_name = option_tag.get_text()
            level = class_name.count('─')
            if class_id == 0:
                continue
            # if current_level == level:
            #
            #     print(class_id, class_name, )
            # print('level -->', level, 'level_list -->', level_list)
            if len(level_list) - 1 >= level:
                level_list[level] = class_id
            else:
                level_list.append(class_id)

            parent_data = {}
            if level == 0:
                parent_data = class_data_dict
                print(class_id, class_name)
            else:
                print(class_id, class_name, level_list[level -1])
                # for i in level_list[:level]:
                #     print('class_data_dict[i] -->', class_data_dict)
                #     if parent_data:
                #         parent_data = parent_data[i]['children']
                #     else:
                #         parent_data = class_data_dict[i]['children']

        #     parent_data[class_id] = {
        #         'class_name': class_name,
        #         'children': {}
        #     }
        #
        #     print('level_list -->', level_list)
        #     print('class_data_dict -->', class_data_dict)
        # print('class_data_dict -->', json.dumps(class_data_dict))


        # table_tags = soup.find_all('table', width="100%", border="0", cellspacing="0", cellpadding="2")
        # for table_tag in table_tags:
        #     # print("table_tag ===>", table_tag)
        #     for a_tag in table_tag.find_all('a'):
        #         if 'oncontextmenu' in a_tag.attrs:
        #             class_name = a_tag.get_text().split('[')[0]
        #             class_id = a_tag.get_text().split(':')[1].replace(']', '')
        #
        #             print(class_name, class_id)
        #             class_data_dict[class_id] = {
        #                 'name': class_name
        #             }
        #             self.getChildClassInfo(class_id)

    # 判断标题是否可用
    def article_test_title(self, title):
        print("判断标题是否可用")
        url = self.home_url + '/article_test_title.php?t={title}'.format(title=title)
        print('url -->', url)
        ret = self.requests_obj.get(url)
        if '存在标题' in ret.text.strip():
            print('标题已存在')
            return False

        return True

    # 发布文章
    def sendArticle(self, data):
        if self.article_test_title(data.get('title')):
            print('增加文章')
            url = self.home_url + '/article_add.php'
            ret = self.requests_obj.post(url, data=data)
            if '成功发布文章' in ret.text:
                print('发布成功')
            else:
                print("========================================> 发布失败")
                print(ret.text)


if __name__ == '__main__':
    domain = 'http://www.bjwletyy.com'
    home_path = '/wladmin'
    userid = 'zhidao'
    pwd = 'zhidao2018'
    obj = DeDe(domain, home_path)
    obj.login(userid, pwd)