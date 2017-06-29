# -*- coding: utf-8 -*-
""""""
from django.http import JsonResponse
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ObjectDoesNotExist

from posts.models import Post
from posts.schemas import get_post_schema
from utils.utils import generate_response, schema_validator
from utils.exceptions import Api404


def get_object_or_404(model=None, **kwargs):
    """"""
    if not model or not kwargs:
        raise ValueError('参数错误')
    try:
        return model.objects.get(**kwargs)
    except ObjectDoesNotExist as e:
        raise Api404('')


class PostView(View):
    """"""

    @method_decorator(schema_validator(get_post_schema))
    def dispatch(self, request, *args, **kwargs):
        return super(PostView, self).dispatch(request, *args, **kwargs)

    # @method_decorator(schema_validator(get_post_schema))
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
