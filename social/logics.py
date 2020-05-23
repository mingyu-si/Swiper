import datetime
import time

from django.db.transaction import atomic

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
    '''从数据库中获取用户'''
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


def updata_swipe_data(uid, sid):
    '''更新 Redis 里的滑动数据'''
    name = keys.REWID_K % uid
    rds.hmset(name, {'last_stime': time.time(), 'last_sid': sid})


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
        raise error.SidError('您的SID错了')
        # 为本次滑动添加一条记录
    Swiperd.swiper(uid, sid, 'like')

    # 强制从优先推荐队列删除 sid
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
        raise error.SidError('您的SID错了')

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


def dislike_someone(uid, sid):
    '''不喜欢(左滑)某人'''
    if not sid or uid == sid:
        raise error.SidError('您的SID错了')

    Swiperd.swiper(uid, sid, 'dislike')

    my_first_q = keys.FIRST_RCMD_Q % uid
    rds.lrem(my_first_q, 1, sid)


def rewind_swiper(uid):
    '''反悔上一次的滑动

    Redis 中记录的数据:{
        'count':0, #当天的反悔次数
        'rewind_date':'2020-5-22', #反悔的日期
        'last_swiper':155445,# 最后一次滑动的时间 时间戳，方便计算
        'last_sid':98,# 最后一次滑动的 SID
    }
    '''
    # 从 Redis 中取出反悔数据
    rewind_key = 'Rewind-%s' % uid
    rewind_data = rds.hgetall(rewind_key)
    rewind_date = rewind_data.get(b'rewind_date', '1970-01-01')
    rewind_cnt = rewind_data.get(b'rewind_cnt', 0)
    last_stime = rewind_data.get(b'last_stime', 0)
    last_sid = rewind_data.get(b'last_sid', 0)

    # 取出当前时间
    now = datetime.date.today()
    today = str(now.date())

    # 检查当天返回次数  超过 3 次 -> 返回状态码
    if today == rewind_data:
        if rewind_cnt >= 3:
            raise error.RewindLimitErr
        else:
            rewind_cnt = 0

    # 从数据库中获取最后一条滑动记录并检查是否为None
    last_swiper = Swiperd.objects.filter(uid=uid).latest('stime')
    if last_swiper is None:
        raise error.NonSwiper

    # 检查时间是否超过 5 分钟
    if (now - last_swiper.stime) > datetime.timedelta(minutes=5):
        raise error.RewindTimeout
    with atomic():
        # 之前匹配成好友， 需要解除好友关系
        if last_swiper.stype in ['like', 'superlike']:
            Friend.break_off(uid, last_swiper.sid)
    # 删除滑动记录
    last_swiper.delet()

    # 之前是超级喜欢， 需要将 ID 从对方推荐队列删除
    rds.lrem(keys.FIRST_RCMD_Q % last_swiper.sid, 0, uid)

    # 更新反悔数据
    rds.hmset(rewind_key, {'rewind_cnt': rewind_cnt + 1, 'rewind_date': today})


def who_liked_me(uid):
    '''过滤出喜欢过我，但是我还没有滑过的人'''
    # 取出我已经滑过的 sid 列表
    sid_list = Swiperd.objects.filter(uid=uid).values_list('sid', flat=True)

    # 取出 uid 列表
    uid_list = Swiperd.objects.filter(sid=uid, stype__in=['like', 'superlike'])\
                                      .exclude(uid__in=sid_list)\
                                      .values_list('uid', flat=True)
    return User.objects.filter(id__in=uid_list)


