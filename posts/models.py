# -*- coding: utf-8 -*-
"""卡片(posts)相关模型集合"""
import re
from datetime import datetime

from django.db import models
from django.contrib.auth.models import User

from utils.utils import BaseModel


# class SourceReplaceMixin(object):
#     """图片视频资源替换"""
#
#     def source_replace(self, new_uri=''):
#         if not new_uri or (not new_uri.startswith('http://')
#                            or not new_uri.startswith('https://')):
#             self.uri = new_uri
#             self.updated_at = datetime.now()
#             self.save()


class PostLabel(BaseModel):
    """"""
    user = models.ForeignKey(User, verbose_name='标签创建人')
    label_name = models.CharField('标签名', max_length=255, unique=True)
    label_status = models.SmallIntegerField('标签热度', default=0)
    is_deleted = models.SmallIntegerField(choices=(
        (0, '未删除标签'),
        (1, '已删除标签')
    ), default=0)
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'post_labels'
        ordering = ['-label_status', 'id']

    def compute_hot(self):
        return Post.objects.filter(label=self).count() // 100


class Post(BaseModel):
    """"""
    # 默认不允许content为空
    POST_TYPES = (
        (1, '纯文本'),
        (2, '文本+图片'),
        (3, '文本+视频'),
        (4, '文本+图片+视频'),
        (0, '其它')
    )
    user = models.OneToOneField(User, verbose_name='发帖人')
    followers = models.ForeignKey(User, related_name='followers', verbose_name='关注用户', blank=True, null=True)
    label = models.ManyToManyField(PostLabel)
    post_type = models.SmallIntegerField('卡片类型', choices=POST_TYPES, default=1)

    post_title = models.CharField('标题', max_length=255, null=True, blank=True)
    post_content = models.TextField('卡片内容', default='')

    like_count = models.IntegerField('点赞次数', default=0)
    is_deleted = models.SmallIntegerField(choices=(
        (0, '未删除'),
        (1, '已删除')
    ), default=0)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'posts'
        ordering = ['-updated_at']

    def __str__(self):
        return f'{self.post_title} - {self.user.username}'

    def compute_like_count(self):
        self.like_count += 1

    def compute_comment_count(self):
        return self.postcomment_set.all().count()


class PostImages(BaseModel):
    """"""
    post = models.ForeignKey(Post)
    uri = models.URLField('图片地址')
    is_deleted = models.SmallIntegerField(choices=(
        (0, '未删除'),
        (1, '已删除')
    ), default=0)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField('图片更新时间', auto_now_add=True)

    class Meta:
        db_table = 'post_images'
        ordering = ['-updated_at']


class PostVideos(BaseModel):
    """卡片视频内容"""
    post = models.ForeignKey(Post)
    uri = models.URLField('视频地址')
    is_deleted = models.SmallIntegerField(choices=(
        (0, '未删除'),
        (1, '已删除')
    ), default=0)
    updated_at = models.DateTimeField('视频替换时间', auto_now_add=True)
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'post_videos'
        ordering = ['-updated_at']


class AtFriendsMixin(object):
    """"""

    def at_friends(self, friends=[]):
        if not friends or not isinstance(friends, list):
            raise ValueError('@用户参数错误')
        us = User.objects.filter(pk__in=friends)
        self.add_at_friends.extend(us)
        self.save()


class CommentComment(BaseModel):
    """评论楼中楼"""
    post_comment = models.ForeignKey('PostComment', verbose_name='所属评论')
    comment_from = models.OneToOneField(User, related_name='comment_from', verbose_name='评论人')
    comment_to = models.OneToOneField(User, related_name='comment_to', verbose_name='回复人')
    content = models.TextField('回复', default='')
    is_deleted = models.SmallIntegerField(choices=(
        (0, '未删除'),
        (1, '已删除')
    ), default=0)
    created_at = models.DateTimeField(auto_now=True)


class PostComment(BaseModel):
    """卡片评论"""
    post = models.ForeignKey(Post)
    user = models.OneToOneField(User, verbose_name='评论人')

    content = models.TextField('评论内容')
    like_count = models.IntegerField('评论点赞数', default=0)
    is_deleted = models.SmallIntegerField(choices=(
        (0, '未删除'),
        (1, '已删除')
    ), default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'post_comments'
        ordering = ['-created_at']

    def compute_like_count(self):
        self.like_count += 1
        self.save()
