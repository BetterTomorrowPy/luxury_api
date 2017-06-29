# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-29 02:29
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='followers',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='followers', to=settings.AUTH_USER_MODEL, verbose_name='关注用户'),
        ),
        migrations.AlterField(
            model_name='post',
            name='label',
            field=models.ManyToManyField(blank=True, null=True, to='posts.PostLabel'),
        ),
    ]