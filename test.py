
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
        url = 'http://m.evercarebj.com/api.php?op=checkcode&code_len=4&font_size=20&width=130&height=50&font_color=&background='
        login_url = 'http://m.evercarebj.com/index.php?m=admin&c=index&a=login&dosubmit=1'
        if self.cookies:
            self.is_login(login_url)
            return self.cookies

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
        # print('ret.text----------->',ret.text)
        # print('self.requests_obj.cookies---------> ',self.requests_obj.cookies)
        # print('self.requests_obj.cookies---------> ',self.requests_obj.headers)
        cookies = requests.utils.dict_from_cookiejar(self.requests_obj.cookies)
        self.cookies = cookies
        print('cookies============> ',cookies)
        return cookies

    # 判断是否登录
    def is_login(self, login_url):
        post_data = {
            'dosubmit': '',
            'username': self.userid,
            'password': self.pwd,
        }
        # print('判断是否登录========》 ', login_url, self.cookies)
        ret = self.requests_obj.post(login_url, cookies=self.cookies, data=post_data)
        # print(ret.text)
        if "返回上一页" in ret.text:
            self.cookies = ''    # cookie清除掉
            self.login()


    # 获取栏目信息
    def getClassInfo(self):
        url = 'http://m.evercarebj.com/index.php?m=content&c=content&a=public_categorys&type=add&menuid=822&pc_hash=XfRWUu'
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
        if ret.text == '0':
            return True   # 不重复
        return False

    # # 发布文章
    def sendArticle(self, data, title):
        catid = data.get('info[catid]')
        if self.article_test_title(catid, title):
            print('增加文章')
            # url ='http://m.evercarebj.com/index.php?m=content&c=content&a=add&menuid=&catid={}&pc_hash=XfRWUu&pc_hash=XfRWUu'.format(catid)
            url = 'http://m.evercarebj.com/index.php?m=content&c=content&a=add'
            print('发布url==================> ',url)
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
                'Referer':'http://m.evercarebj.com/index.php?m=content&c=content&a=add&menuid=&catid=115&pc_hash=XfRWUu&pc_hash=XfRWUu',
            }
            ret = self.requests_obj.post(url, data=data, cookies=self.cookies, headers=headers)
            print('========> ', ret.text.strip())
            # if '无法解析文档' not in ret.text.strip():
            #     if '成功发布文章' in ret.text:
            #         soup = BeautifulSoup(ret.text, 'lxml')
            #         aid_href = soup.find('a', text='更改文章').get('href')    # 文章id
            #         aid = aid_href.split('?')[1].split('&')[0].split('aid=')[-1]
            #         huilian_href = soup.find('a', text='查看文章').get('href')    # 文章id
            #
            #         ret = self.requests_obj.get(huilian_href, cookies=self.cookies)
            #         encode_ret = ret.apparent_encoding
            #         # print('encode_ret===========', encode_ret)
            #         if encode_ret == 'GB2312':
            #             ret.encoding = 'gbk'
            #         else:
            #             ret.encoding = 'utf-8'

                        # print('title-------------> ',title)
                        # print('ret.text==============> ',ret.text)
                        # if title.strip() in ret.text:
    #                         # print('huilian=============> ', huilian)
    #                         # 更新文档url
    #                         # updateWordUrl = '{home_url}/task_do.php?typeid={cid}&aid={aid}&dopost=makeprenext&nextdo=makeindex,makeparenttype'.format(
    #                         #     home_url=self.home_url,
    #                         #     aid=aid,
    #                         #     cid=cid
    #                         # )
    #                         # # 更新主页url
    #                         # updateIndexUrl = '{home_url}/task_do.php?f=0&typeid={cid}&aid={aid}&dopost=makeindex&nextdo=makeparenttype'.format(
    #                         #     home_url=self.home_url,
    #                         #     aid=aid,
    #                         #     cid=cid
    #                         # )
    #
    #                         # if objCookies:
    #                         #     ret1 = self.requests_obj.get(updateWordUrl, cookies=objCookies)
    #                         #     print('ret1--> ',ret1, ret1.url)
    #                         #
    #                         #     ret2 = self.requests_obj.get(updateIndexUrl, cookies=objCookies)
    #                         #     print('ret2-=--> ',ret2, ret2.url)
    #                         #
    #                         # else:
    #                         #     print('===============else=============else')
    #                         #     ret1 = self.requests_obj.get(updateWordUrl)
    #                         #     print('ret1--> ', ret1, ret1.url)
    #                         #     ret2 = self.requests_obj.get(updateIndexUrl)
    #                         #     print('ret2-=--> ', ret2, ret2.url)
    #                         print('’发布成功=========================发布成功===================发布成功')
    #                         if 'http://4g.scgcyy.com' in self.home_url:  # 四川肛肠  没有发布生成权限 需要拼接回链
    #                             huilian = 'http://4g.scgcyy.com/all/xzh/{}.html'.format(aid)
    #                         return {
    #                             'huilian':huilian,
    #                             'aid':aid,
    #                             'code':200
    #                             # 'code':305
    #                             }
    #                     else:
    #                         print('=============没有查到该标题=============')
    #                         return {
    #                             'code':301,
    #                      }
    #                 else:
    #                     return {
    #                         'huilian': huilian,
    #                         'aid': aid,
    #                         'code': 200
    #                         # 'code':305
    #                     }
    #             else:
    #                 print('’发布失败=========================没有成功发布文章===================发布失败 500')
    #                 return {
    #                     'huilian':'',
    #                      'code':500
    #                     }
    #         else:
    #             print('’模板文件不存在, 请选择子级菜单=========================模板文件不存在, 请选择子级菜单===================模板文件不存在, 请选择子级菜单 305')
    #             return {
    #                 'huilian': '',
    #                 'code': 305
    #             }
    #     else:
    #         print('’发布失败=========================发布失败===================发布失败 300')
    #         return {
    #                 'huilian':'',
    #                  'code':300
    #                 }
    #
    # # 查询是否审核通过
    # def getArticleAudit(self, url, id, aid):
    #     ret = self.requests_obj.get(url, cookies=self.cookies)
    #     encode_ret = ret.apparent_encoding
    #     print('encode_ret===========', encode_ret)
    #     if encode_ret == 'GB2312':
    #         ret.encoding = 'gbk'
    #     else:
    #         ret.encoding = 'utf-8'
    #     # print('ret.text======================> ',ret.text)
    #     soup = BeautifulSoup(ret.text, 'lxml')
    #     center_divs_all = soup.find_all('tr', align='center')
    #     print('center_divs_all=>',len(center_divs_all))
    #     status = False
    #     for center_div in center_divs_all:
    #         if 'http://m.glamzx.com/admin_2230_zbj_2017' not in url: # 北京克莱美舍 匹配条件与其他不一样
    #             height = 26
    #             index = 0
    #             index1 = 6
    #         else:
    #             height = 35
    #             index = 1
    #             index1 = 5
    #         if int(center_div.attrs.get('height') )== height:
    #             aid_text = int(center_div.find_all('td')[index].get_text().strip())
    #             if aid_text == int(aid):
    #                 print('===========================================', )
    #                 auditHtml = center_div.find_all('td')[index1].get_text().strip()
    #                 print('auditHtml------------->',auditHtml)
    #                 if auditHtml == '已生成':
    #                     status = True
    #                     break
    #     return id, status
    #
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
        'pc_hash':'XfRWUu'
    }
    objs = PcV9(user_id, password, cookie)
    objs.login()
    # objs.getClassInfo()
    objs.sendArticle(data, title)