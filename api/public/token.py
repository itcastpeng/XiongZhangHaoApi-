import time
from xiongzhanghao.publicFunc.account import str_encrypt

def start():
    token = '87358e1e762b76cca29de2a14dd2a70f'
    user_id = 54
    timestamp = str(int(time.time() * 1000))
    params = {
        'user_id': user_id,
        'rand_str': str_encrypt(timestamp + token),
        'timestamp': timestamp,
    }
    return params
