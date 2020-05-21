import datetime

from user.models import User


def rcmd_users(uid):
    '''为用户推荐一些可以匹配的对象'''
    user = User.objects.get(id=uid)  # 当前用户
    today = datetime.date.today()

    # 最大交友年龄40，出生最早
    earliest_birthday = today - datetime.timedelta(user.Profile.max_dating_age * 365)  # 1980
    # 最小交友年龄20 ，出生最晚
    latest_birthday = today - datetime.timedelta(user.Profile.min_dating_age * 365)  # 1990

    # 满足用户的对象
    users = User.objects.filter(
        gender=user.profile.dating_gender,
        location=user.profile.dating_location,
        birthday__gte=earliest_birthday,
        birthday__lte=latest_birthday
    )[:25]  # 懒加载， Django会解析完整语句，然后拼接成他一条SQL，然后发给 MySQL 执行
    # TODO:排除已经滑过的用户
    return users


def like_someone(uid, sid):
    '''喜欢(右滑)了某人'''
    # sid 不能是已经滑过的人
    # 检查 uid 和 sid 是否相同
    # sid必须有值

    # 为本次滑动添加一条记录

    # 检查对方是否 向右或向上 滑动过自己， 如果有，则匹配成好友
