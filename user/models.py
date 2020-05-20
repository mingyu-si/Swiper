from django.db import models


class User(models.Model):
    GENDER = (
        ('male', '男性'),
        ('female', '女性'),
    )
    LOCATION = (
        ('北京', '北京'),
        ('上海', '上海'),
        ('深圳', '深圳'),
        ('郑州', '郑州'),
        ('西安', '西安'),
        ('武汉', '武汉'),
        ('成都', '成都'),
        ('沈阳', '沈阳'),
    )
    phonenum = models.CharField(max_length=15, unique=True, verbose_name='手机号')
    nickname = models.CharField(max_length=32, verbose_name='昵称')
    gender = models.CharField(max_length=10, choices=GENDER, verbose_name='性别')
    birthday = models.DateField(default='2000-01-01', verbose_name='生日')
    avator = models.CharField(max_length=256, verbose_name='个人形象的URL')
    location = models.CharField(max_length=10, default='北京', choices=LOCATION, verbose_name='常居地')

    @property
    def profile(self):
        '''用户对于的Profile'''
        # get_or_create()方法有两个返回值,第一个是对象，第二个是布尔值,若是创建出来的，为True，否则为False
        # 动态的为self添加属性，防止多次操作数据库，拿同一个数据
        self._profile, _ = Profile.objects.get_or_create(id=self.id)
        return self._profile

    def to_dict(self):
        return {
            'id': self.id,
            'phonenum': self.phonenum,
            'nickname': self.nickname,
            'gender': self.gender,
            'birthday': str(self.birthday),
            'avator': self.avator,
            'location': self.location,
        }


class Profile(models.Model):
    '''交友资料'''
    dating_gender = models.CharField(max_length=10, default='female', choices=User.GENDER,
                                     verbose_name='匹配的性别')
    dating_location = models.CharField(max_length=10, default='北京', choices=User.LOCATION,
                                       verbose_name='⽬标城市')

    min_distance = models.IntegerField(default=1, verbose_name='最⼩查找范围')
    max_distance = models.IntegerField(default=10, verbose_name='最⼤查找范围')
    min_dating_age = models.IntegerField(default=20, verbose_name='最⼩交友年龄')
    max_dating_age = models.IntegerField(default=50, verbose_name='最⼤交友年龄')

    vibration = models.BooleanField(default=True, verbose_name='开启震动')
    only_matched = models.BooleanField(default=True, verbose_name='不让陌⽣⼈看我的相册')
    auto_play = models.BooleanField(default=True, verbose_name='⾃动播放视频')

    def to_dict(self):
        return {
            'id': self.id,
            'dating_gender': self.dating_gender,
            'dating_location': self.dating_location,
            'min_distance': self.min_distance,
            'max_distance': self.max_distance,
            'min_dating_age': self.min_dating_age,
            'max_dating_age': self.max_dating_age,
            'vibration': self.vibration,
            'only_matched': self.only_matched,
            'auto_play': self.auto_play,
        }
