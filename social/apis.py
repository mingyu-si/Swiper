from libs.http import render_json
from social import logics


def rcmd_user(request):
    '''获取推荐列表'''
    users = logics.rcmd_users(request.uid)
    result = [user.to_dict() for user in users]
    return render_json(result)


def like(request):
    '''喜欢(右滑)'''
    return render_json()


def superlike(request):
    '''超级喜欢(左滑)'''
    return render_json()


def dislike(request):
    '''不喜欢(上滑)'''
    return render_json()


def rewind(request):
    '''反悔最后一次的滑动

    -每天允许反悔3次
    -反悔的记录只能是五分钟之内的
    '''


