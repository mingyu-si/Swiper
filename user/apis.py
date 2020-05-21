import os

from django.core.cache import cache

from common import keys
from common import error
from libs.http import render_json
# from libs.qncloud import upload_to_qncloud
# from libs.qncloud import upload_data_to_qncloud
from user import logics
from user.models import User, Profile
from user import forms


def get_vcode(request):
    '''获取短信验证码'''
    phonenum = request.GET.get('phonenum')
    is_successed = logics.send_vcode(phonenum)
    if is_successed:
        return render_json()
    else:
        return render_json(code=error.VCODE_SEND_ERR)


def submit_vcode(request):
    '''通过验证码登入、注册'''
    phonenum = request.POST.get('phonenum')
    vcode = request.POST.get('vcode')

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
        request.session['uid'] = user.id
        return render_json(data=user.to_dict())
    else:
        return render_json(code=error.VCODE_ERR)


def show_profile(request):
    '''查看个人交友资料'''
    user = User.objects.get(id=request.id)

    result = {}
    result.update(user.to_dict())
    result.update(user.profile.to_dict())
    return render_json(result)


def modify_prodile(request):
    '''修改个人及交友资料'''
    # 定义两个Form 表单
    user_form = forms.UserForm(request.POST)
    profile_form = forms.ProfileForm(request.POST)

    # 检查 user_form 和profile_form
    if not user_form.is_valid() or not profile_form.is_valid():
        errors = {}
        errors.update(user_form.errors)
        errors.update(profile_form.errors)
        return render_json(errors, error.PROFILE_FORM_ERR)
    # 更新user
    User.objects.filter(id=request.uid).update(**user_form.cleaned_data)

    # 更新或创建profile
    # 如果用户没有调用查看个人交友资料接口，数据库里就没有对应的profile数据，防止直接调用修改个人资料接口
    Profile.objects.update_or_create(id=request.uid, defaults=profile_form.cleaned_data)


def upload_avator(request):
    '''个人照片上传'''
    # 获取上传的文件对象
    avator = request.Files.get('avator')
    logics.handle_avator.delay(request.uid, avator)
    return render_json()
