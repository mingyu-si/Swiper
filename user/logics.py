import random

import requests

from swiper import config


def gen_randcode(length=6):
    '''产生一个指定长度的验证码'''
    start = 10 ** (length - 1)
    end = 10 ** length - 1
    return str(random.randint(start, end))


def send_vcode(mobile):
    '''发送短信验证码'''
    # .copy()是浅拷贝
    args = config.YZX_VCODE_ARGS.copy()
    args['mobile'] = mobile
    args['param'] = gen_randcode()

    response = requests.post(config.YZX_API, json=args)
    if response.status_code == 200:
        result = response.json()
        if result['msg'] == 'OK':
            return True
    print(response.text)
    return False
