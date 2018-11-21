import time
from xiongzhanghao.publicFunc.account import str_encrypt

def start():
    token = 'a66b1a82b4ba3ca9d444322c8524e844'
    user_id = 44
    timestamp = str(int(time.time() * 1000))
    params = {
        'user_id': user_id,
        'rand_str': str_encrypt(timestamp + token),
        'timestamp': timestamp,
    }
    return params
