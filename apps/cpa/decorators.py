# -*- coding: utf-8 -*-
#Python imports
from functools import wraps
import datetime

#Django import
from django.utils.decorators import available_attrs
from django.shortcuts import get_object_or_404

#findinshop imports
from apps.cpa.utils import get_item_unique_cookie_key
from apps.catalog.models import Item


def transition_action(view_func):
    def _transaction_action(self, *args, **kwargs):
        view = view_func(self, *args, **kwargs)
        item = get_object_or_404(Item, pk=kwargs['product_id'])

        expires = datetime.datetime.strftime(datetime.datetime.utcnow() + \
                datetime.timedelta(seconds=12*3600), "%a, %d-%b-%Y %H:%M:%S GMT") #12 hours
        cookie_item_key = get_item_unique_cookie_key(item)

        if not cookie_item_key in self.request.COOKIES:
            view.set_cookie(cookie_item_key, item.id, expires=expires)

        return view
    return wraps(view_func, assigned=available_attrs(view_func))(_transaction_action)
