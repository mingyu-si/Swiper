from django.core.cache import cache

from common import keys
from common import error
from libs.http import render_json
from user import logics
from user.models import User


def get_vcode(requset):
    '''获取短信验证码'''
    phonenum = requset.GET.get('phonenum')
    is_successed = logics.send_vcode(phonenum)
    if is_successed:
        return render_json()
    else:
        return render_json(code=error.VCODE_SEND_ERR)


def submit_vcode(requset):
    '''通过验证码登入、注册'''
    phonenum = requset.POST.get('phonenum')
    vcode = requset.POST.get('vcode')

    # 从缓存中取出验证码
    key = keys.VCODE_K % phonenum
    cashed_vcode = cache.get(key)
    print('==========================')
    print(cashed_vcode)
    print('--------------------')
    print(vcode)
    # 检查用户的验证码和缓存的验证码是否一致
    # 注意：当用户没有传验证码，获取到的是None，缓存里也没有，获取到的也是None
    if vcode and vcode == cashed_vcode:
        # 先获取用户
        try:
            # 如果用户存在，直接从数据库获取
            user = User.objects.get(phonenum=phonenum)
        except   User.DoesNotExist:
            # 如果不存在，则创建出来
            user = User.objects.create(phonenum=phonenum, nickname=phonenum)

        # 记录用户登入信息
        requset.session['uid'] = user.id
        return render_json(data=user.to_dict())
    else:
        return render_json(code=error.VCODE_ERR)


def show_profile(requset):
    '''查看个人交友资料'''
    user = User.objects.get(id=requset.id)

    result = {}
    result.update(user.to_dict())
    result.update(user.profile.to_dict())
    return render_json(result)


def modify_prodile(requset):
    '''修改个人资料及交友资料'''
    return render_json()


def upload_avator(requset):
    '''头像上传'''
    return render_json()
