# -*- coding: utf-8 -*-

#Django imports
from django.contrib import admin

#Findinshop imports
from apps.coupon.models import *


class CouponAdmin(admin.ModelAdmin):
    display_field = ('code', )
    exclude = ('items',)


admin.site.register(Coupon, CouponAdmin)
