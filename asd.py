#! /usr/bin/env python
# -*- coding: utf-8 -*-


import os, django, random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'source.settings')
django.setup()

from apps.catalog.models import Item
from apps.coupon.models import Coupon


print(asd.id)
print(Coupon.objects.filter(items=asd))

print(Coupon.objects.get(code='1234zaza4321').items.all())
asd = Item.objects.get(name='Чехол-книжка Nokia CP-303 Nokia 3 Blue')
