# -*- coding: utf-8 -*-
"""View helpers."""

from django.views.generic.base import View
from django.db.models import Model, QuerySet
from django.core.paginator import Paginator, Page


class ViewHelperMixin(object):
    """class base view 辅助 Mixin"""

    def get_queryset(self, model=None, **kwargs):
        if not model or not issubclass(model, Model):
            raise TypeError('In get_queryset model is None or illegal.')
        kwargs['is_deleted'] =  0
        return model.objects.select_related.filter(**kwargs)

    def generate_list(self, queryset=None):
        if not queryset:
            return []
        if not isinstance(queryset, Page):
            raise TypeError('In generate_list queryset illegal.')
        _ = list()
        for row in queryset:
            _.append(row.to_dict())

        return _

    def paginator(self, queryset=[], parmas={}):
        if not isinstance(queryset, (list, QuerySet)):
            raise TypeError('In paginator queryset illegal.')

        p = Paginator(queryset, int(parmas.get('per_size', 15)))
        page = int(parmas.get('page', 1))
        if page > p.num_pages:
            return [], p.count
        return p.page(page), p.count


class BaseView(View, ViewHelperMixin):
    """Class Base view`s Base class"""

    def __init__(self, *args, **kwargs):
        super(BaseView, self).__init__(*args, **kwargs)
