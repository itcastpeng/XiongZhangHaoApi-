













# website_backstage_url = 'http://3g.meilianchen.cn//zxmr/kczx/19845102220.html'
#
# url = website_backstage_url.split('.html')[0]
# l = url.split('/')[-1]
#
#
# print(l)
#
# import datetime
# d = datetime.datetime.now()
#
# deletionTime = (d + datetime.timedelta(days=3))
#
# print(deletionTime.weekday())



# import json
#
# list = [{'click_num': '19', 'show_num': '773', 'date_time': '2018-12-19', 'click_show_rate': '2.46%'}, {'click_num': '10', 'show_num': '1,529', 'date_time': '2018-12-18', 'click_show_rate': '0.65%'}, {'click_num': '16', 'show_num': '830', 'date_time': '2018-12-17', 'click_show_rate': '1.93%'}, {'click_num': '7', 'show_num': '919', 'date_time': '2018-12-16', 'click_show_rate': '0.76%'}, {'click_num': '12', 'show_num': '902', 'date_time': '2018-12-15', 'click_show_rate': '1.33%'}, {'click_num': '12', 'show_num': '931', 'date_time': '2018-12-14', 'click_show_rate': '1.29%'}, {'click_num': '6', 'show_num': '547', 'date_time': '2018-12-13', 'click_show_rate': '1.1%'}]
#
# print(json.dumps(list))


import datetime


p = datetime.datetime.strptime("2018-12-22", "%Y-%m-%d")

print(p.weekday())









