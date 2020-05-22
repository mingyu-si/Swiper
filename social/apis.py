from libs.http import render_json
from social import logics
from social.logics import like_someone
from social.models import Swiperd, Friend
from common import error


def rcmd_user(request):
    '''获取推荐列表'''
    users = logics.rcmd_users(request.uid)
    result = [user.to_dict() for user in users]
    return render_json(result)


def like(request):
    '''喜欢(右滑)'''
    sid = int(request.Post.get('sid', 0))
    is_matched = like_someone(request.uid, sid)
    return render_json({'is_matched': is_matched})


def superlike_someone(request):
    '''超级喜欢(上滑)'''
    sid = request.Post.get('sid', 0)
    is_matched = logics.superlike_someone(request.uid, sid)
    return render_json({'is_matched': is_matched})


def dislike(request):
    '''不喜欢(上滑)'''
    sid = request.Post.get('sid', 0)
    logics.dislike_someone(request.uid, sid)
    return render_json()


def rewind(request):
    '''反悔最后一次的滑动

    -每天允许反悔3次
    -反悔的记录只能是五分钟之内的
    '''
