# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2020-05-25 12:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0002_auto_20200521_1614'),
    ]

    operations = [
        migrations.CreateModel(
            name='Friend',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid1', models.IntegerField(verbose_name='好友ID')),
                ('uid2', models.IntegerField(verbose_name='好友ID')),
            ],
        ),
        migrations.AlterField(
            model_name='swiperd',
            name='sid',
            field=models.IntegerField(verbose_name='被滑动者的ID'),
        ),
        migrations.AlterField(
            model_name='swiperd',
            name='uid',
            field=models.IntegerField(verbose_name='滑动者的ID'),
        ),
        migrations.AlterUniqueTogether(
            name='friend',
            unique_together=set([('uid1', 'uid2')]),
        ),
    ]
