#! /usr/bin/env python
# -*- coding: utf-8 -*-


import os, django, random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'source.settings')
django.setup()

from apps.catalog.models import Item
from apps.coupon.models import Coupon

asd = Item.objects.get(name='Рюкзак для ноутбука Dell Alienware Vindicator 2.0 17 Bp (460-BCBT)')
print(asd.id)
print(Coupon.objects.filter(items=asd))

print(Coupon.objects.get(code='1234zaza4321').items.all())