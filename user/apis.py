from django.http import JsonResponse


def get_vcode(requset):
    '''获取短信验证码'''
    return JsonResponse({})


def submit_vcode(requset):
    '''通过验证码登入、注册'''
    return JsonResponse({})


def show_profile(requset):
    '''查看个人交友资料'''
    return JsonResponse({})


def modify_prodile(requset):
    '''修改个人资料及交友资料'''
    return JsonResponse({})


def upload_avator(requset):
    '''头像上传'''
    return JsonResponse({})
