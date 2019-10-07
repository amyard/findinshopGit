# -*- coding: utf-8 -*-

#Django imports
from django.contrib import admin
from django import forms

#Findinshop imports
from apps.cpa.models import *
from apps.cpa.forms import OwnAndUserCategoryForm


class ReportAdmin(admin.ModelAdmin):
    list_display = ('user', 'section', 'category', 'product_name', 'cost', 'ip', 'date')
    readonly_fields = ('user', 'section', 'category', 'product_name', 'cost', 'ip', 'date')


class OwnAndUserCategoryAdmin(admin.ModelAdmin):
    list_display = ('site', 'our_section')

    form = OwnAndUserCategoryForm

    class Media:
        js = (
                '/static/js/admin/categories_by_site.js',
        )


class RefreshCostTaskAdmin(admin.ModelAdmin):
    list_display = ('setting', 'item_count', 'status')
    readonly_fields = ('setting', 'item_count', 'status', 'error', 'start', 'complete')

admin.site.register(Report, ReportAdmin)
admin.site.register(OwnAndUserCategory, OwnAndUserCategoryAdmin)
admin.site.register(RefreshCostTask, RefreshCostTaskAdmin)
