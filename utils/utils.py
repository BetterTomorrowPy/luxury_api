# -*- coding: utf-8 -*-
import json
import logging
import functools

from datetime import datetime
from django.utils import six
from django.db import models
from voluptuous import MultipleInvalid, Schema

from utils.exceptions import JsonResponse, ApiBadRequest


def gen_sub_dict(original={}, fields=[]):
    """
    :params
        :original :type dict
        :fields :type list
    :return: dict
    """
    if not isinstance(original, dict):
        raise TypeError('原始字典参数错误')
    if not fields:
        return original
    _ = dict()
    keys = original.keys()
    for field in fields:
        if field not in keys:
            continue
        _[field] = original[field]
    return _


def generate_response(code=0, content={}, message=''):
    return JsonResponse({
        'code': code,
        'msg': message,
        'content': content
    })


def schema_validator(fields):
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
                _schema = fields.get(request.method, {})
                schema = Schema(_schema)
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

    def to_dict(self, fields=[]):
        _json = self.__dict__
        _keys = _json.keys()
        if six.PY3:
            _keys = list(_json.keys())
        for _k in _keys:
            if _k.startswith('_') or callable(_k):
                _json.pop(_k)
                continue
            if fields:
                if _k not in fields:
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
