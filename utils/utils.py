# -*- coding: utf-8 -*-
import json
import logging
import functools

from datetime import datetime
from django.utils import six
from django.db import models
from voluptuous import MultipleInvalid

from utils.exceptions import JsonResponse, ApiBadRequest


def generate_response(code=0, content={}, message=''):
    return JsonResponse({
        'code': code,
        'msg': message,
        'content': content
    })


def schema_validator(schema):
    """
    参数验证装饰器
    :param schema:
    :return:
    """

    def func_wrapper(method):
        @functools.wraps(method)
        def wrapper(request, *args, **kwargs):
            content_type = request.content_type
            if content_type and content_type.startswith('application/json'):
                body = request.body
                if six.PY3:
                    body = body.decode('utf-8')
                _arguments = json.loads(body)
            else:
                _arguments = dict()
                if 'GET' == request.method:
                    _arguments = request.GET.dict()
                elif 'POST' == request.method:
                    _arguments = request.POST.dict()
            try:
                request.json_arguments = schema(_arguments)
            except MultipleInvalid as e:
                error_message = f'path: {e.path} \n message: {e.error_message}'
                logging.debug(error_message)
                data = {
                    'code': -1,
                    'msg': error_message
                }
                return ApiBadRequest(data=data)
            return method(request, *args, **kwargs)
        return wrapper

    return func_wrapper


class AuxiliaryMixin(object):
    """Model辅助类"""

    def to_dict(self):
        _json = self.__dict__
        _keys = _json.keys()
        if six.PY3:
            _keys = list(_json.keys())
        for _k in _keys:
            if _k.startswith('_') or callable(_k):
                _json.pop(_k)
                continue
            if isinstance(_json[_k], datetime):
                _json[_k] = _json[_k].strftime('%Y-%m-%d %H:%M:%S') if _json[_k] else ''
        return _json

    def source_replace(self, new_uri=''):
        if not new_uri or (not new_uri.startswith('http://')
                           or not new_uri.startswith('https://')):
            self.uri = new_uri
            self.updated_at = datetime.now()
            self.save()


class BaseModel(models.Model, AuxiliaryMixin):
    class Meta:
        abstract = True
