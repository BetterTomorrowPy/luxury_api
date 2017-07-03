# -*- coding: utf-8 -*-
""""""
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User

from posts.models import (Post, PostLabel, PostImage, PostVideo, PostComment,
                          PostFollowers, CommentComment)
from posts.schemas import post_schema, post_label_schema, follower_schema, comment_schema
from utils import BaseView, gen_sub_dict, logger
from utils.utils import generate_response, schema_validator
from utils.exceptions import Api404, ApiBadRequest


def get_object_or_404(model=None, **kwargs):
    """"""
    if not model or not kwargs:
        raise ValueError('参数错误')
    try:
        return model.objects.get(**kwargs)
    except ObjectDoesNotExist as e:
        raise Api404()


class PostLabelView(BaseView):
    """"""

    @method_decorator(csrf_exempt)
    @method_decorator(schema_validator(post_label_schema))
    def dispatch(self, request, *args, **kwargs):
        return super(PostLabelView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        """
        :param request.json_arguments type: dict
        :return:
        """
        params = request.json_arguments
        filters = {

        }
        _labels = PostLabel.objects.filter(**filters)
        labels, label_count = self.paginator(_labels, {'page': params.get('page'),
                                                       'per_size': params.get('per_size')})
        return generate_response(1000, self.generate_list(labels), '获取标签列表成功')

    def post(self, request):
        """"""
        params = request.json_arguments
        try:
            u = User.objects.get(pk=params.get('user_id'))
            params.update({
                'user': u
            })
            label = PostLabel.objects.create(**params)
            return generate_response(1000, label.to_dict(fields=['id', 'label_name']))
        except Exception as e:
            raise Api404(message=str(e))


class PostView(BaseView):
    """"""

    @method_decorator(schema_validator(post_schema))
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(PostView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        """"""
        params = request.json_arguments
        filters = gen_sub_dict(params, ['id', 'user_id', 'post_type', 'created_at'])
        queryset = self.get_queryset(Post, **filters)
        posts, post_count = self.paginator(queryset, params)
        return generate_response(1000, self.generate_list(posts), '返回卡片成功')

    def post(self, request):
        """创建卡片"""
        params = request.json_arguments

        u = User.objects.get(username='guppy')
        post_params = {
            # 'user': request.user,
            'user': u,
            'post_type': params.get('post_type', 1),
            'post_title': params.get('post_title', ''),
            'post_content': params.get('post_content', ''),
        }
        p = Post.objects.create(**post_params)

        labels = PostLabel.objects.filter(pk__in=params.get('label_ids', []))
        p.labels = labels
        p.save()

        # post image
        images = params.get('images', [])
        for image in images:
            try:
                PostImage.objects.create(post=p, uri=image.strip())
            except Exception as e:
                logger.error(f'> created post image {p.id} - {image} failed.')

        # post video.
        videos = params.get('videos', [])
        for video in videos:
            try:
                PostVideo.objects.create(post=p, uri=video.strip())
            except Exception as e:
                logger.error(f'> created post video {p.id} - {video} failed.')

        return generate_response(1000, {'post_id': p.to_dict()}, '创建卡片成功')

    def delete(self, request):
        """"""
        params = request.json_arguments
        post_id = params.get('post_id')
        try:
            p = Post.objects.get(pk=post_id)
            p.is_deleted = 1
            p.save()
            pis = PostImage.objects.filter(post=p)
            for pi in pis:
                pi.is_deleted = 1
                pi.save()
            pvs = PostVideo.objects.filter(post=p)
            for pv in pvs:
                pv.is_deleted = 1
                pv.save()
            return generate_response(1000, {'result': True})
        except Exception as e:
            return generate_response(1000, {'result': False}, '-'.join(e.args))


class FollowerView(BaseView):
    """"""

    @method_decorator(schema_validator(follower_schema))
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(FollowerView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        """获取卡片所有粉丝"""
        post_id = request.json_arguments.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        _followers = PostFollowers.objects.filter(post=post)
        followers, count = self.paginator(_followers, request.json_arguments)
        return generate_response(1000, self.generate_list(followers))

    def post(self, request):
        post_id = request.json_arguments.get('post_id')
        user_id = request.json_arguments.get('user_id')
        post = get_object_or_404(Post, id=post_id)
        user = get_object_or_404(User, id=user_id)
        post_follower = {
            'post': post,
            'user': user
        }
        pf = PostFollowers.objects.create(**post_follower)
        return generate_response(1000, pf.to_dict())

    def delete(self, request):
        post_id = request.json_arguments.get('post_id')
        user_id = request.json_arguments.get('user_id')
        post = get_object_or_404(Post, id=post_id)
        user = get_object_or_404(User, id=user_id)
        post_follower = {
            'post': post,
            'user': user
        }
        pf = get_object_or_404(PostFollowers, **post_follower)
        pf.is_deleted = 1
        pf.save()
        return generate_response(1000, message='取消喜欢成功')


class CommentView(BaseView):
    """卡片评论"""
    
    @method_decorator(schema_validator(comment_schema))
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(CommentView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        """"""
        post = Post.objects.get(pk=request.json_arguments.get('post_id'))
        post_comments = self.get_queryset(PostComment, post=post)
        _comments = self.paginator(post_comments)
        comments = list()
        for _comment in _comments:
            item = _comment.to_dict()
            _c2s = _comment.commentcomment_set.all()
            c2s = list()
            if _c2s:
                c2s = [_c.to_dict() for _c in _c2s]
            item['comment_comments'] = c2s

        return generate_response(1000, comments)

    def post(self, request):
        """
        :param request.json_arguments:
        :return:
        """
        comment_type = request.json_arguments.get('comment_type')

        if 0 == comment_type:
            post = Post.objects.get(pk=request.json_arguments.get('post_id'))
            pc = {
                'post': post,
                'user': request.user,
                'content': request.json_arguments['content']
            }
            post_comment = PostComment.objects.create(**pc)
        elif 1 == comment_type:
            _post_comment = PostComment.objects.get(pk=request.json_arguments.get('post_comment_id'))
            comment_from = User.objects.get(pk=request.json_arguments.get('comment_from_id'))
            comment_to = User.objects.get(pk=request.json_arguments.get('comment_to_id'))
            cc = {
                'post_comment': _post_comment,
                'comment_from': comment_from,
                'comment_to': comment_to,
                'content': request.json_arguments['content'] or ''
            }
            post_comment = CommentComment.objects.create(**cc)
        else:
            raise ApiBadRequest
        return generate_response(1000, post_comment.to_dict())