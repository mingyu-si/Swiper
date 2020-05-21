from django.db import models


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
