# -*- coding: utf-8 -*-

from django.http import JsonResponse


class ApiBadRequest(JsonResponse):
    status_code = 400

    def __init__(self, *args, **kwargs):
        super(ApiBadRequest, self).__init__(*args, **kwargs)


class Api404(JsonResponse):
    status_code = 404

    def __init__(self, *args, **kwargs):
        super(ApiBadRequest, self).__init__(*args, **kwargs)
