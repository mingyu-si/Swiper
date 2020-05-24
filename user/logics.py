import random

import requests
from django.core.cache import cache

from libs.qncloud import upload_data_to_qncloud
from swiper import config
from common import keys
from user.models import User
from task import celery_app


def gen_randcode(length=6):
    '''产生一个指定长度的验证码'''
    start = 10 ** (length - 1)
    end = 10 ** length - 1
    return str(random.randint(start, end))


def send_vcode(mobile):
    '''发送短信验证码'''
    # 放置用户重复发送验证码，先检查缓存中是否有验证码，如果存在直接返回
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
                cache.set(key, args['param'], 900)  # 设置缓存时间
                return True
        print('--------------')
        print(response.text)
        return False


# 方法一：上传源文件
# def upload_avator(request):
#     '''个人头像上传'''
#     # 获取上传的文件对象
#     avator = request.FILES.get('avator')
#     # print('------------------')
#     # print(request.uid.exists())
#     # print('+++++++++++++++++++++++++')
#
#     #将文件保存到硬盘上
#     filepath, filename = logics.save_avator(request.uid, avator)
#
#     #将文件上传到七牛云
#     avator_url = upload_to_qncloud(filepath, filename)
#
#     #将图片的链接保存到数据库
#     User.objects.filter(id=request.uid).update(avator=avator_url)
#
#     #将本地的文件删除
#     os.remove(filepath)
#
#     return render_json()

#方法一：上传源文件
# def save_avator(uid, avator_obj):
#     '''将个人形象保存到硬盘上'''
#     filename = f'Avator-{uid}'  # Python3.6 以后的版本支持这种语法
#     filepath = f'/Users/SMY/Desktop/{filename}'
#
#     with open(filepath, 'wb')as fp:
#         for chunk in avator_obj.chunks():
#             fp.write(chunk)  # 分块写入到硬盘
#
#     return filepath, filename


# 方法二：上传二进制流数据
@celery_app.task
def handle_avator(uid, avator_file):

    # 将文件上传到七牛云
    filename = f'Avator-{uid}'
    filedata = avator_file.read()
    avator_url = upload_data_to_qncloud(filename, filedata)

    # 将图片的链接保存到数据库
    User.objects.filter(id=uid).update(avator=avator_url)




