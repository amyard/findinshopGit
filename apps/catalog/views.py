# -*- coding: utf-8
import os
import shutil
import json
from celery.app.control import Control

from django.shortcuts import redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.forms.formsets import formset_factory
from django.http import HttpResponse
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

from utils2.decorators import render_to
from utils2.utils import set_paginator_window

from forms import CategoryForm, ItemForm, ParamsForm, ItemVideoForm, \
    ImportTaskForm, FilterForm, ActionForm, OrderForm, OrderItemForm, ExprofileEditForm, PointForm, CurrencySettingForm
from models import Category, Item, ItemVideo, ImportTask, ExportTask, \
    Order, OrderItem, CurrencySetting
from apps.website.models import Website, WebsiteProperty, Point
from tasks import (
    import_product,
    export_processing,
    clean_user_catalog, clean_items)
from apps.account.models import ExtendedProfile, Profile

import json

import dse
dse.patch_models(specific_models=[Category, Item])


@login_required
@render_to('catalog.html')
def catalog(request):
    query = request.GET.get('query', '')
    items = []
    if query:
        items = Item.objects.filter(
            name__icontains=query,
            site=request.user.website
        )
    roots = request.user.website.catalog.category_set.filter(parent__isnull=True)
    return {
            'roots': roots,
            'items': items
    }


@login_required
@render_to('orders.html')
def orders(request):
    orders = Order.objects.filter(catalog__website=request.user.website).order_by('status', '-modified_date')
    return {'orders': orders}


@login_required
@render_to('order_control.html')
def order_control(request, order_id, action):
    order = get_object_or_404(Order, id=order_id, catalog__website=request.user.website)
    if action == 'v':
        form = OrderForm(instance=order)
        order_list = OrderItem.objects.filter(order=order)
        OrderFormset = formset_factory(OrderItemForm, extra=0)
        initial = []
        for item in order_list:
            pair = {}
            pair['item'] = item.item
            pair['quantity'] = item.quantity
            pair['cost'] = item.cost
            initial.append(pair)
        formset = OrderFormset(initial=initial)

        for f in formset:
            f.fields['item'].queryset = Item.objects.filter(site=request.user.website)

        if request.method == 'POST':
            form = OrderForm(request.POST, instance=order)
            formset = OrderFormset(request.POST, initial=initial)
            for f in formset:
                f.fields['item'].queryset = Item.objects.filter(site=request.user.website)
            if form.is_valid() and formset.is_valid():
                inst = form.save(commit=False)
                inst.catalog = request.user.website.catalog
                inst.save()
    if action == 'd':
        order.delete()
        return redirect('orders')
    return {'order': order, 'action': action, 'form': form, 'formset': formset}


@login_required
def category_delete(request, cat_id):
    c = get_object_or_404(Category, id=cat_id, catalog__website=request.user.website)
    parent = c.parent
    c.delete()
    if parent:
        return redirect('category', cat_id=parent.id)
    else:
        return redirect('catalog')


@login_required
@render_to('category_page.html')
def category(request, cat_id):
    category_obj = Category.objects.get(id=cat_id)
    subcategories = Category.objects.filter(parent=category_obj)
    goods = Item.objects.filter(category=category_obj)
    p = Paginator(goods, 15)
    try:
        page = p.page(request.GET.get('p', 1))
    except PageNotAnInteger:
        page = p.page(1)
    except EmptyPage:
        page = p.page(p.num_pages)
    set_paginator_window(page)
    form = ItemForm(catalog=request.user.website.catalog)
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, catalog=request.user.website.catalog)
        if form.is_valid():
            inst = form.save(commit=False)
            inst.category = category_obj
            inst.save()
    return {'form': form, 'category_obj': category_obj, 'goods': goods, 'page': page, 'subcategories': subcategories}


@login_required
@render_to('category_page.html')
def delete_item(request, item_id):
    del_item = get_object_or_404(Item, id=item_id, category__catalog__website=request.user.website)
    cid = del_item.category.id
    del_item.delete()
    return redirect('category', cat_id=cid)


@login_required
@render_to('edit_item.html')
def edit_item(request, item_id):
    item_obj = get_object_or_404(Item, id=item_id, category__catalog__website=request.user.website)
    category_obj = item_obj.category
    try:
        video_obj = ItemVideo.objects.get(item=item_obj)
    except ItemVideo.DoesNotExist:
        video_obj = None
    try:
        param_list = item_obj.parameters.keys()
    except AttributeError:
        param_list = []
    l = max(1, len(param_list))
    ParamsFormset = formset_factory(ParamsForm, extra=l, max_num=l)
    form = ItemForm(instance=item_obj, catalog=request.user.website.catalog)
    initial = []
    for param in param_list:
        pair = {}
        pair['name'] = param
        pair['value'] = item_obj.parameters[param]
        initial.append(pair)
    formset = ParamsFormset(initial=initial)
    # ItemVideoFormset = formset_factory(ItemVideoForm, extra=1)
    form_video = ItemVideoForm(instance=video_obj)
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, instance=item_obj, catalog=request.user.website.catalog)
        formset = ParamsFormset(request.POST)
        form_video = ItemVideoForm(request.POST, instance=video_obj)
        if form.is_valid() and formset.is_valid() and form_video.is_valid():
            inst = form.save(commit=False)
            inst.site = request.user.website
            d = {}
            for form in formset:
                if form.cleaned_data.get('name'):  # and form.cleaned_data.get('value'):
                    d[form.cleaned_data.get('name')] = form.cleaned_data.get('value')
            inst.parameters = d
            inst.save()
            inst_video = form_video.save(commit=False)
            inst_video.item = inst
            inst_video.save()
            return redirect('category', cat_id=category_obj.id)
    return {'form': form, 'formset': formset, 'form_video': form_video}


@login_required
@render_to('add_item.html')
def add_item(request, cat_id):
    category_obj = get_object_or_404(Category, id=cat_id, catalog__website=request.user.website)
    items = Item.objects.filter(category=category_obj).count()
    count_products = WebsiteProperty.objects.get(id=request.user.website.web_property_id).product_max
    if items < count_products:
        category_obj = Category.objects.get(id=cat_id)
        ParamsFormset = formset_factory(ParamsForm, extra=4)
        formset = ParamsFormset()
        # ItemVideoFormset = formset_factory(ItemVideoForm, extra=1)
        form_video = ItemVideoForm()
        form = ItemForm(catalog=request.user.website.catalog, category=category_obj)
        if request.method == 'POST':
            form = ItemForm(request.POST, request.FILES, catalog=request.user.website.catalog, category=category_obj)
            formset = ParamsFormset(request.POST)
            form_video = ItemVideoForm(request.POST)
            if form.is_valid() and formset.is_valid() and form_video.is_valid():
                inst = form.save(commit=False)
                # inst.category = category_obj
                inst.site = request.user.website
                d = {}
                for form in formset:
                    if form.cleaned_data.get('name'):  # and form.cleaned_data.get('value'):
                        d[form.cleaned_data.get('name')] = form.cleaned_data.get('value')
                inst.parameters = d
                inst.save()
                inst_video = form_video.save(commit=False)
                inst_video.item = inst
                inst_video.save()
                return redirect('category', cat_id=cat_id)
        return {'form': form, 'formset': formset, 'form_video': form_video}
    else:
        return HttpResponse('<h4 align="center" style="margin:40px;">Достигнуто максимальное количество товаров для данного пакета. </h4>')


@login_required
def bestseller(request):
    if request.method == 'POST':
        data = request.POST.copy()
        del data['csrfmiddlewaretoken']
        for key in data.keys():
            item = Item.objects.get(id=key)
            if 'True' in data.getlist(key):
                item.bestseller = True
            else:
                item.bestseller = False
            item.save()
        return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required
@render_to('edit_category.html')
def category_add(request):
    form = CategoryForm(catalog=request.user.website.catalog)
    ParamsFormset = formset_factory(ParamsForm, extra=4)
    formset = ParamsFormset()
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, catalog=request.user.website.catalog)
        formset = ParamsFormset(request.POST)
        if form.is_valid() and formset.is_valid():
            inst = form.save(commit=False)
            inst.catalog = request.user.website.catalog
            d = {}
            for form in formset:
                if form.cleaned_data.get('name'):  # and form.cleaned_data.get('value'):
                    d[form.cleaned_data.get('name')] = form.cleaned_data.get('value')
            inst.parameters = d
            inst.save()
            return redirect('catalog')
    return {'form': form, 'formset': formset}


@login_required
@render_to('edit_category.html')
def category_edit(request, cat_id):
    category_obj = get_object_or_404(Category, id=cat_id, catalog__website=request.user.website)
    try:
        param_list = category_obj.parameters.keys()
    except AttributeError:
        param_list = []
    l = max(1, len(param_list))
    form = CategoryForm(instance=category_obj, catalog=request.user.website.catalog, exclude_id=cat_id, cat_id=cat_id)

    ParamsFormset = formset_factory(ParamsForm, extra=l, max_num=l)
    initial = []
    for param in param_list:
        pair = {}
        pair['name'] = param
        pair['value'] = category_obj.parameters[param]
        initial.append(pair)
    formset = ParamsFormset(initial=initial)
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=category_obj, catalog=request.user.website.catalog, exclude_id=cat_id, cat_id=cat_id)
        formset = ParamsFormset(request.POST)
        if form.is_valid() and formset.is_valid():
            inst = form.save(commit=False)
            d = {}
            for form in formset:
                if form.cleaned_data.get('name'):
                    val = form.cleaned_data.get('value') if form.cleaned_data.get('value') else ''
                    d[form.cleaned_data.get('name')] = val
            inst.parameters = d
            inst.catalog = request.user.website.catalog
            inst.save()
            if d:
                merge_parameters(inst)
            return redirect('category', cat_id=cat_id)
    return {'form': form, 'formset': formset}


def merge_parameters(category_obj):
    items = Item.objects.filter(category=category_obj)
    catp = category_obj.parameters.copy()
    for item in items:
        if not item.parameters:
            item.parameters = {}
        for k, v in catp.items():
            if not k in item.parameters.keys():
                item.parameters[k] = v
        item.save()


@login_required
@render_to('import.html')
def import_task(request):
    website_property = WebsiteProperty.objects.get(id=request.user.website.web_property_id)
    form = ImportTaskForm(website_property=website_property)
    if request.method == 'POST':
        form = ImportTaskForm(request.POST, request.FILES)
        if form.is_valid():
            inst = form.save(commit=False)
            inst.site = request.user.website
            inst.catalog = request.user.website.catalog
            inst.format = ImportTask.FORMATS.XML_HOTLINE
            inst.save()
            import_product.delay(inst.id)
            return redirect('import_status')

    if website_property.imp_from_xml==0 :
        flag_rw1 = 0
    else:
        flag_rw1 = 1

    if website_property.imp_from_yml==0 :
        flag_rw2 = 0
    else:
        flag_rw2 = 1

    if website_property.imp_from_exel==0 :
        flag_rw3 = 0
    else:
        flag_rw3 = 1

    if website_property.imp_from_xmlHP==0 :
        flag_rw4 = 0
    else:
        flag_rw4 = 1

    if website_property.imp_from_1c==0 :
        flag_rw5 = 0
    else:
        flag_rw5 = 1

    if website_property.imp_from_xml == 0:
        return {'form': form, 'type': 'task_hide', 'flag_rw1': flag_rw1, 'flag_rw2': flag_rw2, 'flag_rw3': flag_rw3, 'flag_rw4': flag_rw4, 'flag_rw5': flag_rw5}
    else:
        return {'form': form, 'type': 'task', 'flag_rw1': flag_rw1, 'flag_rw2': flag_rw2, 'flag_rw3': flag_rw3, 'flag_rw4': flag_rw4, 'flag_rw5': flag_rw5}


@login_required
@render_to('import.html')
def import_task_YML(request):
    website_property = WebsiteProperty.objects.get(id = request.user.website.web_property_id)
    form = ImportTaskForm(website_property=website_property)
    if request.method == 'POST':
        ImportTask.objects.filter(catalog=request.user.website.catalog).delete()
        form = ImportTaskForm(request.POST, request.FILES)
        if form.is_valid():
            inst = form.save(commit=False)
            inst.site = request.user.website
            inst.catalog = request.user.website.catalog
            inst.format = ImportTask.FORMATS.YML
            inst.save()
            import_product.delay(inst.id)

            return redirect('import_status')

    if website_property.imp_from_xml==0 :
        flag_rw1 = 0
    else:
        flag_rw1 = 1

    if website_property.imp_from_yml==0 :
        flag_rw2 = 0
    else:
        flag_rw2 = 1

    if website_property.imp_from_exel==0 :
        flag_rw3 = 0
    else:
        flag_rw3 = 1

    if website_property.imp_from_xmlHP==0 :
        flag_rw4 = 0
    else:
        flag_rw4 = 1

    if website_property.imp_from_1c==0 :
        flag_rw5 = 0
    else:
        flag_rw5 = 1

    if website_property.imp_from_yml==0 :
        return {'form': form, 'type': 'task_YML_hide','flag_rw1': flag_rw1, 'flag_rw2': flag_rw2, 'flag_rw3': flag_rw3, 'flag_rw4': flag_rw4, 'flag_rw5': flag_rw5}
    else:
        return {'form': form, 'type': 'task_YML','flag_rw1': flag_rw1, 'flag_rw2': flag_rw2, 'flag_rw3': flag_rw3, 'flag_rw4': flag_rw4, 'flag_rw5': flag_rw5}


@login_required
@render_to('import.html')
def import_task_Excel(request):
    website_property = WebsiteProperty.objects.get(id = request.user.website.web_property_id)
    form = ImportTaskForm(website_property=website_property)
    if request.method == 'POST':
        form = ImportTaskForm(request.POST, request.FILES)
        if form.is_valid():
            inst = form.save(commit=False)
            inst.site = request.user.website
            inst.catalog = request.user.website.catalog
            inst.format = ImportTask.FORMATS.XLS
            inst.save()
            import_product.delay(inst.id)
            return redirect('import_status')

    if website_property.imp_from_xml==0 :
        flag_rw1 = 0
    else:
        flag_rw1 = 1

    if website_property.imp_from_yml==0 :
        flag_rw2 = 0
    else:
        flag_rw2 = 1

    if website_property.imp_from_exel==0 :
        flag_rw3 = 0
    else:
        flag_rw3 = 1

    if website_property.imp_from_xmlHP==0 :
        flag_rw4 = 0
    else:
        flag_rw4 = 1

    if website_property.imp_from_1c==0 :
        flag_rw5 = 0
    else:
        flag_rw5 = 1

    if website_property.imp_from_exel==0 :
        return {'form': form, 'type': 'task_Excel_hide','flag_rw1': flag_rw1, 'flag_rw2': flag_rw2, 'flag_rw3': flag_rw3, 'flag_rw4': flag_rw4, 'flag_rw5': flag_rw5}
    else:
        return {'form': form, 'type': 'task_Excel','flag_rw1': flag_rw1, 'flag_rw2': flag_rw2, 'flag_rw3': flag_rw3, 'flag_rw4': flag_rw4, 'flag_rw5': flag_rw5}


@login_required
@render_to('import.html')
def import_task_HotPrise(request):
    website_property = WebsiteProperty.objects.get(id = request.user.website.web_property_id)
    form = ImportTaskForm(website_property=website_property)
    if request.method == 'POST':
        form = ImportTaskForm(request.POST, request.FILES)
        if form.is_valid():
            inst = form.save(commit=False)
            inst.site = request.user.website
            inst.catalog = request.user.website.catalog
            inst.format = ImportTask.FORMATS.XML_HOTPRICE
            inst.save()
            import_product.delay(inst.id)
            return redirect('import_status')

    if website_property.imp_from_xml==0 :
        flag_rw1 = 0
    else:
        flag_rw1 = 1

    if website_property.imp_from_yml==0 :
        flag_rw2 = 0
    else:
        flag_rw2 = 1

    if website_property.imp_from_exel==0 :
        flag_rw3 = 0
    else:
        flag_rw3 = 1

    if website_property.imp_from_xmlHP==0 :
        flag_rw4 = 0
    else:
        flag_rw4 = 1

    if website_property.imp_from_1c==0 :
        flag_rw5 = 0
    else:
        flag_rw5 = 1

    if website_property.imp_from_xml==0 :
        return {'form': form, 'type': 'task_HotPrise_hide','flag_rw1': flag_rw1, 'flag_rw2': flag_rw2, 'flag_rw3': flag_rw3, 'flag_rw4': flag_rw4, 'flag_rw5': flag_rw5}
    else:
        return {'form': form, 'type': 'task_HotPrise','flag_rw1': flag_rw1, 'flag_rw2': flag_rw2, 'flag_rw3': flag_rw3, 'flag_rw4': flag_rw4, 'flag_rw5': flag_rw5}


@login_required
@render_to('import.html')
def import_task_1c(request):
    website_property = WebsiteProperty.objects.get(id = request.user.website.web_property_id)
    form = ImportTaskForm(website_property=website_property)
    if request.GET.get('one'):
        import_task = ImportTask(
                        site=request.user.website,
                        catalog=request.user.website.catalog,
                        format=ImportTask.FORMATS.ONE_C
                )
        import_task.save()
        import_product.delay(import_task.id)
        return redirect('import_status')

    if website_property.imp_from_xml==0 :
        flag_rw1 = 0
    else:
        flag_rw1 = 1

    if website_property.imp_from_yml==0 :
        flag_rw2 = 0
    else:
        flag_rw2 = 1

    if website_property.imp_from_exel==0 :
        flag_rw3 = 0
    else:
        flag_rw3 = 1

    if website_property.imp_from_xmlHP==0 :
        flag_rw4 = 0
    else:
        flag_rw4 = 1

    if website_property.imp_from_1c==0 :
        flag_rw5 = 0
    else:
        flag_rw5 = 1

    if website_property.imp_from_1c==0 :
        return {'form': form, 'base_domain': settings.BASE_DOMAIN, 'type': 'task_1C_hide','flag_rw1': flag_rw1, 'flag_rw2': flag_rw2, 'flag_rw3': flag_rw3, 'flag_rw4': flag_rw4, 'flag_rw5': flag_rw5}
    else:
        return {'form': form, 'base_domain': settings.BASE_DOMAIN, 'type': 'task_1C','flag_rw1': flag_rw1, 'flag_rw2': flag_rw2, 'flag_rw3': flag_rw3, 'flag_rw4': flag_rw4, 'flag_rw5': flag_rw5}


@login_required
@render_to('import.html')
def import_status(request):
    tasks = ImportTask.objects.filter(catalog=request.user.website.catalog).order_by('start')

    website_property = WebsiteProperty.objects.get(id = request.user.website.web_property_id)
    if website_property.imp_from_xml==0 :
        flag_rw1 = 0
    else:
        flag_rw1 = 1

    if website_property.imp_from_yml==0 :
        flag_rw2 = 0
    else:
        flag_rw2 = 1

    if website_property.imp_from_exel==0 :
        flag_rw3 = 0
    else:
        flag_rw3 = 1

    if website_property.imp_from_xmlHP==0 :
        flag_rw4 = 0
    else:
        flag_rw4 = 1

    if website_property.imp_from_1c==0 :
        flag_rw5 = 0
    else:
        flag_rw5 = 1

    return {'tasks': tasks, 'type': 'status','flag_rw1': flag_rw1, 'flag_rw2': flag_rw2, 'flag_rw3': flag_rw3, 'flag_rw4': flag_rw4, 'flag_rw5': flag_rw5}


@login_required
@render_to('import_error.html')
def import_error(request):
    return {}


@csrf_exempt
def import_1c(request, user_id):

    if request.GET.get('mode') == 'checkauth':
        return HttpResponse('%s\n%s\n%s\n' % ('success', 'sessionid', request.META["CSRF_COOKIE"]))

    if request.GET.get('mode') == 'init':
        limit = 1000 * 1024;
        user = get_object_or_404(User, pk=user_id)
        source = os.path.join(settings.MEDIA_ROOT, '1c_files/%s/' % user.username.lower())
        for f in ['import.xml', 'offers.xml']:
            if os.path.exists('%s%s' % (source, f)):
                os.remove('%s%s' % (source, f))
        if os.path.exists('%s%s' % (source, 'import_files')):
            shutil.rmtree('%s%s' % (source, 'import_files'))
        return HttpResponse('zip=no\nfile_limit=%s\n' % limit)#file limit 40MБ

    if request.GET.get('mode') == 'file':
        file_name = request.GET.get('filename')
        if not file_name:
            return HttpResponse('failure\nERROR 10: No file name variable\nMODE: %s\n' % request.GET.get('mode'))
        user = get_object_or_404(User, pk=user_id)
        file_source = os.path.join(settings.MEDIA_ROOT, '1c_files/%s/%s' % (user.username.lower(), file_name))
        data = request.read()

        if 'import_files' in file_name:
            os.makedirs(os.path.join(settings.MEDIA_ROOT, '1c_files/%s/%s' % (user.username.lower(), os.path.dirname(file_name))))
        f = open( file_source, 'w+')
        f.write(data)
        f.close()
        os.chmod(file_source, 0777)
        return HttpResponse('success')

    if request.GET.get('mode') == 'import':
        file_name = request.GET.get('filename')
        if not file_name:
            return HttpResponse('failure\nERROR 10: No file name variable\nMODE: %s\n' % request.GET.get('mode'))
        #user = get_object_or_404(User, pk=user_id)
        #file_source = os.path.join(settings.MEDIA_ROOT, '1c_files/%s/%s' % (user.username.lower(), file_name))
        #data = request.read()
        #f = open( file_source, 'w+')
        #f.write(data)
        #f.close()
        #os.chmod(file_source, 0777)
        return HttpResponse('success')

    return HttpResponse('failure\n ERROR: Not GET parameters.\nGET - %s\nPOST - %s\n' % (request.GET, request.POST))


@login_required
@render_to('export.html')
def export_task(request, action, task_id=None):
    exp_xls=0
    exp_yml=0
    if action == 'lst':
        website_property = WebsiteProperty.objects.get(id = request.user.website.web_property_id)
        exp_yml=website_property.exp_from_yml
        exp_xls= website_property.exp_from_xls

        tasks = ExportTask.objects.filter(catalog=request.user.website.catalog)
        return {'tasks': tasks, 'exp_xls':exp_xls, 'exp_yml':exp_yml}
    elif action == 'add':
        task = ExportTask()
        task.site = request.user.website
        task.catalog = request.user.website.catalog
        task.save()
        export_processing.delay(task.id)
        return redirect('export_task', action='lst')
    elif action == 'del' and task_id:
        ExportTask.objects.get(catalog=request.user.website.catalog, id=task_id).delete()
        return redirect('export_task', action='lst')


@login_required
@render_to('flush_catalog.html')
def flush_catalog(request, status_code):
    res = {'status': status_code}
    if request.method == 'POST':
        if status_code == u'flush_confirm' and request.user.website.catalog.state != 1:
            clean_user_catalog.delay(user=request.user)
            request.user.website.catalog.state = 1
            request.user.website.catalog.save()
            res = {'status': 'flush_start'}
        elif request.user.website.catalog.state == 1:
            res = {'status': 'flush_start'}

        elif request.user.website.catalog.state == 2:
            res = {'status': 'flush_end'}
    else:
        if status_code == u'flush_confirm' and request.user.website.catalog.state != 1:
            res = {'status': 'flush_confirm'}
        elif request.user.website.catalog.state == 1:
            res = {'status': 'flush_start'}
        elif request.user.website.catalog.state == 2:
            res = {'status': 'flush_end'}
    return res


@login_required
@render_to('item_operation.html')
def filter(request):
    website_property = WebsiteProperty.objects.get(id = request.user.website.web_property_id)
    applied = False
    items = Item.objects.none()
    wholesale = False
    vendor = None
    discount = None
    currency_setting = CurrencySetting.objects.filter(site=request.user.website)
    fform = FilterForm(catalog=request.user.website.catalog)
    aform = ActionForm()
    if currency_setting:
        currency_setting_form = CurrencySettingForm(instance=currency_setting[0])
    else:
        currency_setting_form = CurrencySettingForm()
    if request.method == 'GET':
        if request.GET:
            fform = FilterForm(request.GET, catalog=request.user.website.catalog)
            if fform.is_valid():
                items = Item.objects.filter(category__catalog=request.user.website.catalog, **fform.cleaned_data)
    if request.method == 'POST':
        if request.GET:
            fform = FilterForm(request.GET, catalog=request.user.website.catalog)
            aform = ActionForm(request.POST)
            if aform.is_valid() and fform.is_valid():
                vendor = fform.cleaned_data.get('vendor')
                discount = aform.cleaned_data.get('discount')
                wholesale = aform.cleaned_data.get('wholesale')
                items = Item.objects.filter(category__catalog=request.user.website.catalog, **fform.cleaned_data)
                if items.update(**aform.cleaned_data) > 0:
                    applied = True
    if request.method == 'POST' and 'currency_setting' in request.POST:
        currency_setting_form = CurrencySettingForm(request.POST)
        if currency_setting_form.is_valid():
            if currency_setting:
                currency_setting.update(**currency_setting_form.cleaned_data)
            else:
                currency_setting = CurrencySetting(site=request.user.website, **currency_setting_form.cleaned_data)
                currency_setting.save()
        return redirect(reverse('filter'))

    return {
            'aform': aform,
            'fform': fform,
            'items': items,
            'wholesale': wholesale,
            'vendor': vendor,
            'discount': discount,
            'applied': applied,
            'website_property': website_property,
            'currency_setting_form': currency_setting_form
    }


@login_required
@render_to('point_add.html')
def point_add(request, point_id=False):
    narrows_fields = ['weekdays_from', 'weekdays_to', 'saturday_from', 'saturday_to', 'sunday_from', 'sunday_to']
    message = u'Новая точка успешно создана.'

    if not point_id:
        form = PointForm(request.POST or None)
    else:
        point = get_object_or_404(Point, pk=point_id)
        message = u'Точка "%s" успешно изменена' % point.name
        form = PointForm(request.POST or None, instance=point)

    if form.is_valid():
        point = form.save(commit=False)
        point.user = request.user
        point.save()
        messages.success(request, message)
        return redirect(reverse('points'))
    return {
                'form': form,
                'narrows_fields': narrows_fields
            }


@login_required
@render_to('points.html')
def points(request):
    points = Point.objects.filter(user=request.user).order_by('kind')
    return {'points': points}


@login_required
def point_delete(request, point_id):
    point = Point.objects.filter(pk=point_id, user=request.user)
    point.delete()
    messages.success(request, u'Точка успешно удалена.')
    return redirect(reverse('points'))


@render_to('map_stores.html')
def map_stores(request, user_id):
    if request.is_ajax():
        city = request.REQUEST.get('city', None)
        if city:
            points = Point.objects.filter(user=user_id, on_map=True, city=city)
        else:
            points = Point.objects.filter(user=user_id, on_map=True)
        Locals = []
        for point in points:
            if point.lat:
                description = u"""<p class="p-shop-url"><b>%s</b></p>
                <p class="p-shop-kind">%s</p>
                <p class="p-shop-name"><b>%s</b></p>""" % (
                    point.user.website.name,
                    point.get_kind_display(),
                    point.name
                )
                if point.notes:
                    description += u'\
                        <p class="p-shop-notes">%s</p>' % point.notes
                if point.weekdays_from:
                    description += u'\
                        <p class="p-shop-work"><b>Режим работы</b><br/>\
                        <span>Пн-Пт.</span> %s - %s' % (
                        point.weekdays_from,
                        point.weekdays_to)
                if point.saturday_from:
                    description += u'\
                        <span>Сб.</span>  %s - %s' % (
                        point.saturday_from,
                        point.saturday_to)
                if point.sunday_from:
                    description += u'\
                        <span>Вс.</span> %s - %s</p>' % (
                        point.sunday_from,
                        point.sunday_to
                    )
                if point.phone:
                    description += u'\
                        <p class="p-shop-phone"><b>Телефон:</b> %s</p>' % (
                        point.phone)
                points_dict = {
                    'lat': point.lat,
                    'lon': point.lon,
                    'zoom': 12,
                    'title': point.name,
                    'html': description
                }
                if point.user.website.logo_map:
                    points_dict['icon'] = '%s' % point.user.website.logo_map.url

                Locals.append(points_dict)
        return HttpResponse(json.dumps(Locals), 'application/json')
    city_list = set(Point.objects.filter(
        user=user_id, on_map=True).values_list('city', flat=True))
    points = Point.objects.filter(user=user_id, on_map=True)
    return {'points': points, 'cities': city_list, 'user_id': user_id}


# @login_required
# @render_to('payment_systems.html')
# def payments(request):
#     tasks = ImportTask.objects.filter(catalog=request.user.website.catalog)
#     return {'tasks': 1}


@login_required
@render_to('information.html')
def information(request):
    try:
        extended_profile = ExtendedProfile.objects.get(user_id=request.user.id)
    except ExtendedProfile.DoesNotExist:
        extended_profile = ExtendedProfile.objects.create(user=request.user)
    # extended_profile = ExtendedProfile.objects.get(user_id=request.user.id)
    profile = Profile.objects.get(user=request.user)

    initial = {
        'site_name': request.user.website.name,
        'phone_call_center': request.user.website.phone_call_center,
        'phone_number': profile.phone_number
            #request.user.profile.phone_number
    }
    form = ExprofileEditForm(instance=profile, initial=initial)
    if request.method == 'POST':
        form = ExprofileEditForm(request.POST, request.FILES, instance=ExtendedProfile.objects.get(user=request.user))
        if form.is_valid():
            form.save()
            c = request.user.website
            c.name = form.cleaned_data.get('site_name')
            c.phone_call_center = form.cleaned_data.get('phone_call_center')
            c.save()

            pr = profile #request.user.profile
            pr.phone_number = form.cleaned_data.get('phone_number')
            pr.save()
            return redirect('information')
    return {'form': form, 'extended_profile': extended_profile}

@login_required
def import_restart(request, task_id):
    try:
        import_task = ImportTask.objects.get(id=task_id)
        import_task.start = None
        import_task.complete = None
        import_task.status = 0
        import_task.save()
        import_product.delay(import_task.id)
        result = {
            'state': "success",
            'start': str(import_task.start),
            'end': str(import_task.complete),
            'status': ImportTask.STATUS._choices[import_task.status][1]
        }
        return HttpResponse(json.dumps(result), content_type="application/json")
    except:
        return HttpResponse('failure', status=400)


@login_required
def import_stop(request, task_id):
    try:
        ctl = Control()
        ctl.revoke(task_id=task_id, terminate=True)
        import_task = ImportTask.objects.get(id=task_id)
        import_task.start = None
        import_task.complete = None
        import_task.status = 0
        import_task.save()
        #import_product.delay(import_task.id)
        result = {
            'state': "success",
            'start': str(import_task.start),
            'end': str(import_task.complete),
            'status': ImportTask.STATUS._choices[import_task.status][1]
        }
        return HttpResponse(json.dumps(result), content_type="application/json")
    except:
        return HttpResponse('failure', status=400)


@login_required
def import_disable(request, task_id):
    try:
        import_task = ImportTask.objects.get(id=task_id)
        import_task.status = 4
        import_task.save()
        clean_items.delay(import_task.site_id)
        result = {
            'state': "success",
            'start': str(import_task.start),
            'end': str(import_task.complete),
            'status': ImportTask.STATUS._choices[import_task.status][1]
        }
        return HttpResponse(json.dumps(result), content_type="application/json")
    except:
        return HttpResponse('failure', status=400)
