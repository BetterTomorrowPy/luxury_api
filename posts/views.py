# -*- coding: utf-8 -*-
""""""
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User

from posts.models import Post, PostLabel
from posts.schemas import get_post_schema, label_schema
from utils import BaseView
from utils.utils import generate_response, schema_validator
from utils.exceptions import Api404


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
    @method_decorator(schema_validator(label_schema))
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

    @method_decorator(schema_validator(get_post_schema))
    def dispatch(self, request, *args, **kwargs):
        return super(PostView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        try:
            post = get_object_or_404(Post, **request.json_arguments)
            return generate_response()
        except Exception as e:
            return generate_response(message=str(e))


@schema_validator(get_post_schema)
@require_http_methods(['GET'])
def get_posts(request):
    """"""
    try:
        post = get_object_or_404(Post, **request.json_arguments)
        return generate_response()
    except Exception as e:
        return generate_response(message=str(e))
