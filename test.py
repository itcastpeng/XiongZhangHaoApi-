
import requests, json
from bs4 import BeautifulSoup





from backend.lianzhongDama import LianZhongDama



data = {
    'dosubmit':'',
    'username':'Ymexiongzhanghao',
    'password':'Yme@evercare20181126',
    'code':''

}




# url = 'http://m.evercarebj.com/index.php?m=admin&c=index&a=login%dosubmit=1'
# ret2 = requests.post(url, data=data)
# print(ret2.text)



class PcV9(object):
    def __init__(self, userid, pwd, cookies=None):
        self.requests_obj = requests.session()
        self.userid = userid
        self.pwd = pwd
        self.cookies = cookies


    def login(self):
        url = 'http://m.evercarebj.com/api.php?op=checkcode&code_len=4&font_size=20&width=130&height=50&font_color=&background='  # 获取验证码
        login_url = 'http://m.evercarebj.com/index.php?m=admin&c=index&a=login&dosubmit=1'  # 登录
        if self.cookies:
            pc_hash = self.is_login(login_url)
            return self.cookies, pc_hash

        while True:
            try:
                yzmRet = self.requests_obj.get(url)
                with open('yzm.jpg', 'wb') as f:
                    f.write(yzmRet.content)
                obj = LianZhongDama()
                yzm = obj.get_yzm('yzm.jpg')
                print('yzm -->', yzm)
                break
            except AttributeError:
                break
        yzm = ''
        post_data = {
            'dosubmit': '',
            'username': self.userid,
            'password': self.pwd,
            'code': '{}'.format(yzm)
        }
        ret = self.requests_obj.post(login_url, data=post_data)
        soup = BeautifulSoup(ret.text, 'lxml')
        pc_hash = soup.find('a', text='如果您的浏览器没有自动跳转，请点击这里')
        pc_hash = pc_hash.attrs.get('href').split('pc_hash=')[-1]
        # print('ret.text----------->',ret.text)
        # print('self.requests_obj.cookies---------> ',self.requests_obj.cookies)
        # print('self.requests_obj.cookies---------> ',self.requests_obj.headers)
        cookies = requests.utils.dict_from_cookiejar(self.requests_obj.cookies)
        self.cookies = cookies
        print('cookies============> ',cookies)
        return cookies, pc_hash

    # 判断是否登录
    def is_login(self, login_url):
        post_data = {
            'dosubmit': '',
            'username': self.userid,
            'password': self.pwd,
        }
        # print('判断是否登录========》 ', login_url, self.cookies)
        ret = self.requests_obj.post(login_url, cookies=self.cookies, data=post_data)
        if '登录成功' in ret.text:
            # print(ret.text)
            soup = BeautifulSoup(ret.text, 'lxml')
            pc_hash = soup.find('a', text='如果您的浏览器没有自动跳转，请点击这里')
            pc_hash = pc_hash.attrs.get('href').split('pc_hash=')[-1]
            return pc_hash
        if "返回上一页" in ret.text:
            self.cookies = ''    # cookie清除掉
            self.login()

    # 获取栏目信息
    def getClassInfo(self, pc_hash):
        url = 'http://m.evercarebj.com/index.php?m=content&c=content&a=public_categorys&type=add&menuid=822&pc_hash={}'.format(pc_hash)
        ret = self.requests_obj.get(url, cookies=self.cookies)
        soup = BeautifulSoup(ret.text, 'lxml')
        category_tree = soup.find('ul', id='category_tree')
        li_tags = category_tree.find_all('li')
        retData = []
        for li_tag in li_tags:
            a_tag = li_tag.find('span', class_='')
            class_id = a_tag.find('a').attrs.get('href').split('&')[-1].split('=')[-1]
            class_name = a_tag.get_text()
            print('class_id-------class_name---> ',class_id, class_name)

            data_list = [class_id, class_name]

            if data_list not in retData:
                retData.append(
                    data_list
                )
        return retData

    # # 判断标题是否可用
    def article_test_title(self, catid, title):
        print("判断标题是否可用")
        url = 'http://m.evercarebj.com/index.php?m=content&c=content&a=public_check_title&catid={}&sid=2.037687345459017&data={}'.format(catid, title)
        ret = self.requests_obj.get(url, cookies=self.cookies)
        print(ret.text)
        if ret.text == '0':
            return True   # 不重复
        return False

    # # 发布文章
    def sendArticle(self, data, title, pc_hash):
        catid = data.get('info[catid]')
        if self.article_test_title(catid, title):
            print('增加文章')
            data['pc_hash'] = pc_hash
            # url ='http://m.evercarebj.com/index.php?m=content&c=content&a=add&menuid=&catid={}&pc_hash=XfRWUu&pc_hash=XfRWUu'.format(catid)
            url = 'http://m.evercarebj.com/index.php?m=content&c=content&a=add'
            print('发布url==================> ',url)
            ret = self.requests_obj.post(url, data=data, cookies=self.cookies)
            # print('========> ', ret.text.strip())
            if '数据添加成功' in ret.text:
                url = 'http://m.evercarebj.com/index.php?m=content&c=content&a=init&menuid=822&catid={}&pc_hash={}'.format(data.get('info[catid]'), pc_hash)
                print('url--------------------> ',url)
                ret = self.requests_obj.get(url, cookies=self.cookies)
                # print(ret.text)
                title = data.get('info[title]')
                print('=============title================title=================> ',title)
                if title in ret.text:
                    print('---------------------------发布成功-------------------------')
                    soup = BeautifulSoup(ret.text, 'lxml')
                    tr_all = soup.find_all('tr')
                    aid = 0
                    huilian = ''
                    for tr in tr_all:
                        if title.strip() in tr.get_text():
                            td_all = tr.find_all('td')
                            aid = td_all[2].get_text()
                            huilian = td_all[3].find('a').attrs.get('href')
                            break
                    return {
                        'huilian':huilian,
                        'aid':aid,
                        'code':200
                    }
                else:
                    print('标题未==查到===============================标题未查到==========================标题未查到')
                    return {
                        'huilian': '',
                        'code': 301
                    }
            else:
                print('===============添加文章失败=============')
                return {
                    'huilian': '',
                    'code': 500
                }
        else:
            print('’发布失败=========================发布失败===================发布失败 300')
            return {
                'huilian': '',
                'code': 300
                    }


    # # 查询文章是否被删除
    # def deleteQuery(self, url, maxtime):
    #     # print('----查询文章是否被删除-----------》 ', url)
    #     ret = self.requests_obj.get(url, cookies=self.cookies)
    #     # print('查询文章是否被删除==url==url====url===>', url)
    #     encode_ret = ret.apparent_encoding
    #     # print('encode_ret===========', encode_ret)
    #     if encode_ret == 'GB2312':
    #         ret.encoding = 'gbk'
    #     else:
    #         ret.encoding = 'utf-8'
    #
    #     time.sleep(0.5)
    #     soup = BeautifulSoup(ret.text, 'lxml')
    #
    #     flag = 0
    #     yema = 0
    #     page_num = soup.find('div', class_='pagelistbox')
    #     maxtime = datetime.datetime.strptime(maxtime, '%Y-%m-%d %H:%M:%S')
    #     maxtime = maxtime.strftime('%Y-%m-%d')
    #     data_list = []
    #     if page_num:
    #         page = page_num.find('span').get_text()
    #         # print('page==========> ',page)
    #         if page:
    #             yema = page.split('页')[0].split('共')[1]
    #             center_divs_all = soup.find_all('tr', align='center')
    #             for center_div in center_divs_all:
    #                 releaseTime = center_div.find_all('td')[3].get_text()
    #                 if releaseTime >= maxtime:
    #                     if center_div.find('a'):
    #                         aid = center_div.find_all('td')[0].get_text().strip()
    #                         title = center_div.find('a').get_text().strip()
    #                         if aid:
    #                             data_list.append({
    #                                 'aid':aid,
    #                                 'title':title,
    #                                 'releaseTime':releaseTime
    #                             })
    #                 else:
    #                     flag = 1
    #         else:
    #             flag = 1
    #     else:
    #         flag = 1
    #     return flag, yema, data_list

import datetime
if __name__ == '__main__':
    catid = 115
    title = '测试标题'
    user_id = 'Ymexiongzhanghao'
    password = 'Yme@evercare20181126'
    cookie = {'PHPSESSID': 'q5981m9bglfllmc3bib4lvuti6',
              'Hhuvt_sys_lang': 'a5e0FMsBPHEjViLciHcdIze2UdMxPOkOwJq4edMDAAwEiw',
              'Hhuvt_admin_username': 'e242V5S-mKfYXHGRRUODNuUI42_b-YJ_XHZcoxfaiEzJ03n62WyVb9vuZ-d9',
              'Hhuvt_siteid': '9222HgxnLMBETl68Jcw2DQcV_cAY8T3ZF6KeueBl',
              'Hhuvt_admin_email': '0e467jj9jrpv_NDlXj-m_73TUGIWn3ab4iKirTA4qN-ElYcCtAZcBwx-w_Y',
              'Hhuvt_userid': '9b82AUqls4zcOtqf33LDiw-ZpeOSjZIx9gLE6NOFAA'}
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data = {
        'info[thumb]':'',
        'info[relation]':'',
        'info[inputtime]':now,
        'info[islink]':0,
        'info[template]':'',
        'info[allow_comment]':1,
        'info[readpoint]':'',
        'info[paytype]':0,
        'info[catid]':catid,
        'info[title]':title,
        'style_color':'',
        'style_font_weight':'',
        'info[keywords]':'',
        'info[copyfrom]':'',
        'copyfrom_data':0,
        'info[description]':'测试摘要====',
        'info[content]':'测试内容----内容',
        'page_title_value':'',
        'add_introduce':1,
        'introcude_length':200,
        'auto_thumb':1,
        'auto_thumb_no':1,
        'info[paginationtype]':0,
        'info[maxcharperpage]':10000,
        'info[posids][]':-1,
        'info[groupids_view]':1,
        'info[voteid]':'',
        'dosubmit':'保存后自动关闭',
    }
    objs = PcV9(user_id, password, cookie)
    cookie, pc_hash = objs.login()
    # objs.getClassInfo()
    objs.sendArticle(data, title, pc_hash)