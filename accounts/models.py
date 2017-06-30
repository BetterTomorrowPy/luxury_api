# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.db import models

from utils.utils import AuxiliaryMixin


class UserProfile(models.Model, AuxiliaryMixin):
    """用户资料"""
    user = models.OneToOneField(User, verbose_name='用户')

    nick_name = models.CharField('昵称', max_length=64, blank=True, default='')
    phone_no = models.CharField('电话', max_length=16, db_index=True)
    id_no = models.CharField('身份证号码', max_length=32, blank=True, default='')

    wx_openid = models.CharField('微信唯一标识', max_length=256, blank=True, default='')
    qq_no = models.CharField('QQ账号', max_length=16, blank=True, default='')

    is_active = models.SmallIntegerField('是否活跃', choices=(
        (0, '非活跃用户'),
        (1, '活跃用户')
    ), default=1)
    is_deleted = models.SmallIntegerField('是否注销', choices=(
        (0, '未删除'),
        (1, '已删除')
    ), default=1)

    created_at = models.DateTimeField('注册时间', auto_now_add=True)
    updated_at = models.DateTimeField('资料更新时间', auto_now=True)

    # objects = LuxuryManager()

    class Meta:
        db_table = 'user_profile'
        ordering = ['-id', 'phone_no']

    def __str__(self):
        return f'{self.nick_name} - {self.get_is_active_display()}'
