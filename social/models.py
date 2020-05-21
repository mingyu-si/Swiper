from django.db import models
from django.db import IntegrityError


class Swiperd(models.Model):
    '''滑动记录'''
    STYPES = (
        ('like', '右滑'),
        ('superlike', '上滑'),
        ('dislike', '左滑'),
    )
    uid = models.IntegerField(verbose_name='滑动着的ID')
    sid = models.IntegerField(verbose_name='被滑动着的ID')
    stype = models.CharField(max_length=10, choices=STYPES, verbose_name='滑动类型')
    stime = models.DateTimeField(auto_now_add=True, verbose_name='滑动时间')

    class Meta:  # Django不支持联合唯一，但可以通过这样执行
        unique_together = ['uid', 'sid']

    @classmethod
    def swiper(cls, uid, sid, stype):
        '''增加一次滑动记录'''
        if stype not in ['like', 'superlike', 'dislike']:
            return '滑动类型错误'

        try:
            cls.objects.create(uid=uid, sid=sid, stype=stype)
        except  IntegrityError:
            return '重复滑动'  # TODO:错误码待处理

    @classmethod
    def is_liked(cls, uid, sid):
        '''检查是否喜欢过某人'''
        like_stypes = ['like', 'superlike']
        return cls.objects.filter(uid=uid, sid=sid, stype__in=like_stypes).exists()


class Friend(models.Model):
    '''好友表'''
    uid1 = models.IntegerField(verbose_name='好友ID')
    uid2 = models.IntegerField(verbose_name='好友ID')

    class Meta:
        unique_together = ['uid1', 'uid2']

    @staticmethod
    def sort_uid(uid1, uid2):
        if uid1 > uid2:
            return uid2, uid1
        else:
            return uid1, uid2

    @classmethod
    def make_friends(cls, uid1, uid2):
        '''建立好友关系'''
        uid1, uid2 = cls.sort_uid(uid1, uid2)
        return cls.objects.create(uid1=uid1, uid2=uid2)
