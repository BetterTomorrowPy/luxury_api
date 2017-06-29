# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-29 02:18
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import utils.utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CommentComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(default='', verbose_name='回复')),
                ('is_deleted', models.SmallIntegerField(choices=[(0, '未删除'), (1, '已删除')])),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('comment_from', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='comment_from', to=settings.AUTH_USER_MODEL, verbose_name='评论人')),
                ('comment_to', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='comment_to', to=settings.AUTH_USER_MODEL, verbose_name='回复人')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, utils.utils.AuxiliaryMixin),
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_type', models.SmallIntegerField(choices=[(1, '纯文本'), (2, '文本+图片'), (3, '文本+视频'), (4, '文本+图片+视频'), (0, '其它')], default=1, verbose_name='卡片类型')),
                ('post_title', models.CharField(blank=True, max_length=255, null=True, verbose_name='标题')),
                ('post_content', models.TextField(default=1, verbose_name='卡片内容')),
                ('like_count', models.IntegerField(default=0, verbose_name='点赞次数')),
                ('is_deleted', models.SmallIntegerField(choices=[(0, '未删除'), (1, '已删除')])),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('followers', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followers', to=settings.AUTH_USER_MODEL, verbose_name='关注用户')),
            ],
            options={
                'db_table': 'posts',
                'ordering': ['-updated_at'],
            },
            bases=(models.Model, utils.utils.AuxiliaryMixin),
        ),
        migrations.CreateModel(
            name='PostComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='评论内容')),
                ('like_count', models.IntegerField(default=0, verbose_name='评论点赞数')),
                ('is_deleted', models.SmallIntegerField(choices=[(0, '未删除'), (1, '已删除')])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.Post')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='评论人')),
            ],
            options={
                'db_table': 'post_comments',
                'ordering': ['-created_at'],
            },
            bases=(models.Model, utils.utils.AuxiliaryMixin),
        ),
        migrations.CreateModel(
            name='PostImages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uri', models.URLField(verbose_name='图片地址')),
                ('is_deleted', models.SmallIntegerField(choices=[(0, '未删除'), (1, '已删除')])),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True, verbose_name='图片更新时间')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.Post')),
            ],
            options={
                'db_table': 'post_images',
                'ordering': ['-updated_at'],
            },
            bases=(models.Model, utils.utils.AuxiliaryMixin),
        ),
        migrations.CreateModel(
            name='PostLabel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label_name', models.CharField(max_length=255, unique=True, verbose_name='标签名')),
                ('label_status', models.SmallIntegerField(default=0, verbose_name='标签热度')),
                ('is_deleted', models.SmallIntegerField(choices=[(0, '未删除标签'), (1, '已删除标签')], default=0)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='标签创建人')),
            ],
            options={
                'db_table': 'post_labels',
                'ordering': ['-label_status', 'id'],
            },
            bases=(models.Model, utils.utils.AuxiliaryMixin),
        ),
        migrations.CreateModel(
            name='PostVideos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uri', models.URLField(verbose_name='视频地址')),
                ('is_deleted', models.SmallIntegerField(choices=[(0, '未删除'), (1, '已删除')])),
                ('updated_at', models.DateTimeField(auto_now_add=True, verbose_name='视频替换时间')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.Post')),
            ],
            options={
                'db_table': 'post_videos',
                'ordering': ['-updated_at'],
            },
            bases=(models.Model, utils.utils.AuxiliaryMixin),
        ),
        migrations.AddField(
            model_name='post',
            name='label',
            field=models.ManyToManyField(to='posts.PostLabel'),
        ),
        migrations.AddField(
            model_name='post',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='发帖人'),
        ),
        migrations.AddField(
            model_name='commentcomment',
            name='post_comment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.PostComment', verbose_name='所属评论'),
        ),
    ]
