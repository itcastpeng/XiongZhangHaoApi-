








# cookie = {'PHPSESSID': 'cmdde92k7qjm77s0ap19tibvv1'}
cookie = {'DedeUserID': '73', 'PHPSESSID': '1p1n0u2uo29bsg9qpm3vkkrj93', '_csrf_name_087450a5': '3afc0cca2f4da5c91546b79f2fdf2e53', 'DedeLoginTime': '1541851441', '_csrf_name_087450a5__ckMd5': '4a182a6373f6a9bd', 'DedeUserID__ckMd5': '66b18ea1251520b3', 'DedeLoginTime__ckMd5': '53f56e2f14a36a01'}
import requests

url = 'http://m.oy120.com/@qz120_@/content_list.php?channelid=1'
ret = requests.get(url, cookies=cookie)
print(ret.text)
