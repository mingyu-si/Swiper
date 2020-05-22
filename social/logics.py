import datetime

from common import error
from common import keys
from libs.cashe import rds
from user.models import User
from social.models import Swiperd
from social.models import Friend


def rcmd_users_from_q(uid):
    '''从优先推荐队列获取用户'''
    name = keys.FIRST_RCMD_Q % uid
    uid_list = rds.lrange(name, 0, 24)
    uid_list = [int(uid) for uid in uid_list]  # redis都是bytes类型，需转换
    return User.objects.filter(id__in=uid_list)


def rcmd_users_from_db(uid, num):
    '''从数据库中获取物件用户'''
    user = User.objects.get(id=uid)  # 当前用户
    today = datetime.date.today()

    # 计算目标人群的出生日期范围
    # 最大交友年龄40，出生最早
    earliest_birthday = today - datetime.timedelta(user.Profile.max_dating_age * 365)  # timedelta支持天，小时，不支持年类型
    # 最小交友年龄20 ，出生最晚
    latest_birthday = today - datetime.timedelta(user.Profile.min_dating_age * 365)

    # 取出所有已滑过的用户的 ID 列表
    sid_list = Swiperd.objects.filter(uid=uid).values_list('sid', flat=True)
    # values_list方法是只要sid字段，未加flat参数，结果为<Queryset[(24,), (84)]>,加上flat参数结果为<Queryset[24,84]>

    # 从数据库中获取目标用户
    users = User.objects.filter(
        gender=user.profile.dating_gender,
        location=user.profile.dating_location,
        birthday__gte=earliest_birthday,
        birthday__lte=latest_birthday
    ).exclude(id__in=sid_list)[:num]  # 懒加载， Django会解析完整语句，然后拼接成他一条SQL，然后发给 MySQL 执行
    # 排除已经滑过的用户
    return users


def rcmd_users(uid):
    '''为用户推荐一些可以交友的对象'''
    users_from_q = set(rcmd_users_from_q(uid))
    remain = 25 - len(users_from_q)
    users_from_db = set(rcmd_users_from_db(uid, remain))

    return users_from_q | users_from_db


def like_someone(uid, sid):
    '''喜欢(右滑)了某人'''
    # 先检查开销小的，后检查开销大的
    # 检查 uid 和 sid 是否相同
    # sid必须有值
    # sid 不能是已经滑过的人,在数据库中通过联合唯一判断
    if sid and uid != sid:
        raise error.SidError
        # 为本次滑动添加一条记录
    Swiperd.swiper(uid, sid, 'like')

    #强制从优先推荐队列删除 sid
    name = keys.FIRST_RCMD_Q % uid
    rds.lrem(name, 1, sid)

    # 检查对方是否喜欢过自己 如果是，则匹配成好友
    if Swiperd.is_liked(sid, uid):
        Friend.make_friends(uid, sid)
        return True
    else:
        return False


def superlike_someone(uid, sid):
    '''超级喜欢(上滑)了某人'''
    # 检查 sid 是否正确
    if not sid or uid == sid:
        raise error.SidError

    Swiperd.swiper(uid, sid, 'superlike')

    # 强制从 优先推荐队列删除 sid
    my_first_q = keys.FIRST_RCMD_Q % uid
    rds.lrem(my_first_q, 1, sid)

    # 检查对方是否喜欢过自己 如果是， 则匹配成好友
    is_liked = Swiperd.is_liked(sid, uid)
    if is_liked == True:
        Friend.make_friends(uid, sid)
        return True
    elif is_liked is None:
        other_first_q = keys.FIRST_RCMD_Q % sid
        rds.rpush(other_first_q, uid)  # 将 uid 添加到对方的优先推荐队列
        return False
    else:
        return False
