













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
import requests, time
from itertools import islice


timestamp = int(time.time())
img_name = '1.jpg'
img_source = 'img'
num = 0
url = 'http://127.0.0.1:8004/img_upload_shard'
with open('1.jpg', 'rb') as e:
    img_data = e.read()
    # with open('./1.jpg', 'wb') as f:
    #     f.write(img_data)
    print(type(img_data))
    print('img_data-------------> ', img_data)
    chunk = num
    num += 1
    data = {
        'img_name':img_name,
        'img_source':img_source,
        'timestamp':timestamp,
        'chunk':chunk,
        'img_data':str(img_data),
    }
    ret = requests.post(url, data = data)
    print('ret-> ', ret.json())

# time.sleep(2)
# merge_url = 'http://127.0.0.1:8004/img_merge'
# data = {
#     'img_source':img_source,
#     'img_name':img_name,
#     'timestamp':timestamp,
#     'chunk_num':num,
#
# }
# ret = requests.post(merge_url, data=data)
# print('ret.json()--> ', ret.json())






