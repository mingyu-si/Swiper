import random

import requests
from django.core.cache import cache
from swiper import config
from common import keys


def gen_randcode(length=6):
    '''产生一个指定长度的验证码'''
    start = 10 ** (length - 1)
    end = 10 ** length - 1
    return str(random.randint(start, end))


def send_vcode(mobile):
    '''发送短信验证码'''
    #放置用户重复发送验证码，先检查缓存中是否有验证码，如果存在直接返回
    key = keys.VCODE_K % mobile
    if cache.get(key):
        return True
    else:
        # .copy()是浅拷贝
        args = config.YZX_VCODE_ARGS.copy()
        args['mobile'] = mobile
        args['param'] = gen_randcode()

        response = requests.post(config.YZX_API, json=args)
        if response.status_code == 200:
            result = response.json()
            if result['msg'] == 'OK':
                cache.set(key, args['param'], 900) #设置缓存时间
                return True
        print(response.text)
        return False
