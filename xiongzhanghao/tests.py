













website_backstage_url = 'http://3g.meilianchen.cn//zxmr/kczx/19845102220.html'

url = website_backstage_url.split('.html')[0]
l = url.split('/')[-1]


print(l)

import datetime
d = datetime.datetime.now()

deletionTime = (d + datetime.timedelta(days=3))

print(deletionTime.weekday())