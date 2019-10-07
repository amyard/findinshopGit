# -*- coding: utf-8 -*-
from apps.catalog.models import Item, Vendor
for item in Vendor.objects.all():
    new_name = item.name.strip().lower()
    try:
        exist_vendor = Vendor.objects.get(name=new_name)
        Item.objects.filter(vendor=item).update(vendor=exist_vendor)
        item.delete()
    except Vendor.DoesNotExist:
        try:
            item.name = new_name
            item.save()
        except Exception:
            pass

