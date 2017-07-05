# -*- coding: utf-8 -*-

from django.db import models
from utils.utils import BaseModel


class YXArea(BaseModel):
    """"""
    parent_id = models.IntegerField('父节点ID')
    path = models.CharField('路径', max_length=255)
    level = models.IntegerField('级别')
    cn_name = models.CharField('中文名', max_length=255)
    en_name = models.CharField('英文名', max_length=255)
    cn_pinyin = models.CharField('拼音', max_length=255)
    code = models.CharField('代码', max_length=64)

    class Meta:
        db_table = 'yx_area_table'


class Area(BaseModel):
    name = models.CharField(max_length=64)
    parent_id = models.CharField(max_length=64)
    level = models.SmallIntegerField()

    class Meta:
        db_table = 'area_table'