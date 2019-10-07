# -*- coding: utf-8 -*-

#Django imports
from django.contrib import admin

#Findinshop imports
from apps.manager.models import *


class BannerAdmin(admin.ModelAdmin):
    list_display = ('name',  'sort', 'active')
    list_editable = ('sort', 'active')


admin.site.register(Banner, BannerAdmin)
