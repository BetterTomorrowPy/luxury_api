# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-29 02:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_auto_20170629_1029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='post_content',
            field=models.TextField(default='', verbose_name='卡片内容'),
        ),
    ]
