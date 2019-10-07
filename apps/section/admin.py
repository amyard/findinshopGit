# -*- coding: utf-8 -*-

#Django imports
from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.files.temp import NamedTemporaryFile
from django.contrib import messages
from django.http import HttpResponseRedirect

import os


#Findinshop imports
from apps.section.models import *

from .import_productmodel import (
    ImportProductModel,
    ImportProductException
)

from django.core.urlresolvers import reverse


class InlineEditLinkMixin(object):
    readonly_fields = ['edit_details']
    edit_label = "Edit"
    def edit_details(self, obj):
        if obj.id:
            opts = self.model._meta
            return "<a href='%s' target='_blank'>%s</a>" % (reverse(
                'admin:%s_%s_change' % (opts.app_label, opts.object_name.lower()),
                args=[obj.id]
            ), self.edit_label)
        else:
            return "(save to edit details)"
    edit_details.allow_tags = True

class SectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'get_thumb', 'sort', 'deleted')
    list_editable = ('sort', 'deleted')
    readonly_fields = ('have_child',)
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

    class Media:
        js = ('/static/themes/findinshop/js/admin/section.js',)


class ParameterAdmin(admin.ModelAdmin):
    list_display = ('name', 'sort')
    list_editable = ('sort',)


class MeasureAdmin(admin.ModelAdmin):
    list_display = ('name', 'sign_rus', 'sign')


class FeatureGroupAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class FeatureIcecatAdmin(admin.ModelAdmin):
    list_display = ('name', 'measure')
    search_fields = ('name',)


class FeatureParameterConnectionInLine(admin.TabularInline):
    model = FeatureParameterConnection
    extra = 1


class FeatureParameterProductConnection(admin.TabularInline):
    model = FeatureParameterProductConnection
    extra = 1


class FeatureIcecatProductConnection(InlineEditLinkMixin, admin.StackedInline):
# class FeatureIcecatProductConnection(admin.TabularInline):
    model = FeatureIcecatProductConnection
    extra = 1
    fields = ['feature', 'value', 'group']
    # filter_horizontal =  ('feature',  'group',)
    raw_id_fields = ('feature', 'group',)


class FeatureAdmin(admin.ModelAdmin):
    inlines = (FeatureParameterConnectionInLine, )

    list_display = ('admin_name', 'name', 'sort')
    list_editable = ('sort',)


class ProductModelAdmin(admin.ModelAdmin):
    inlines = (FeatureIcecatProductConnection,)
    raw_id_fields = ('section',)
    search_fields = ('name', 'code')
    list_display = ('name', 'section', 'inner_id', 'bad', 'alternative_connections', 'get_image', 'count', 'votes', 'total_score', 'rating', 'is_new')
    readonly_fields = ('votes', 'total_score', 'rating', 'count')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('is_new',)

    class Media:
        js = (
                '/static/js/admin/product_model.js',
                '/static/js/admin/prepopulate_for_productmodel.js',
        )

    def render_change_form(self, request, context, *args, **kwargs):
        self.save_as = True
        self.change = True
        return super(ProductModelAdmin, self).render_change_form(request, context, args, kwargs)

    def get_urls(self):
        from django.conf.urls import patterns, url
        urls = super(ProductModelAdmin, self).get_urls()
        my_urls = patterns("",
                           url(r"^export/$", export))
        return my_urls + urls


@staff_member_required
def export(request):
    if request.method == 'POST':
        if request.FILES.get('product_model'):
            tmp_file = NamedTemporaryFile(delete=True)
            tmp_file.write(request.FILES.get('product_model').read())
            tmp_file.flush()
            try:
                pars = ImportProductModel(tmp_file.name)
                pars.process()
                messages.success(
                    request, u'Продукты загружены')
            except ImportProductException as err:
                messages.error(
                    request, str(err))
            os.unlink(tmp_file.name)
            return HttpResponseRedirect('/admin/section/productmodel')
    return render_to_response(
        'section/upload_product_models.html',
        context_instance=RequestContext(request))


admin.site.register(Section, SectionAdmin)
admin.site.register(Parameter, ParameterAdmin)
admin.site.register(Feature, FeatureAdmin)
admin.site.register(ProductModel, ProductModelAdmin)
admin.site.register(Measure, MeasureAdmin)
admin.site.register(FeatureGroup, FeatureGroupAdmin)
admin.site.register(FeatureIcecat, FeatureIcecatAdmin)
