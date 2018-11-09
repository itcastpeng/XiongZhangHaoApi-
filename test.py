







#
# import base64
#
#
# obj = '56GV8J+SpQ=='
#
#
# print(type(obj))
# decode_username = base64.b64decode(obj)
# print('decode_username-=========> ', decode_username)
# # customer_username = str(decode_username, 'utf-8')
# # print(customer_username)
#
#
#
#
# # b'\xe7\xa1\x95\xf0\x9f\x92\xa5'
# decode_username = b'\xe7\xa1\x95\xf0\x9f\x92\xa5'
#
# customer_username = str(decode_username, 'utf-8')
# print(customer_username)


website_backstage_url = 'http://www.scgcyy.com/drqaz/'

home_path = website_backstage_url.split('/')[-2]

# domain = website_backstage_url.split()
domain = website_backstage_url.split(website_backstage_url.split('/')[-2] + '/')[0]


# home_path = website_backstage_url.split('/')[-1]
# domain = website_backstage_url.split(website_backstage_url.split('/')[-1])[0]
# drqaz http://www.scgcyy.com/
# drqaz http://www.scgcyy.com/
print(home_path, domain)

