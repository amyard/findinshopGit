# -*- coding: utf-8

from django.shortcuts import redirect, get_object_or_404
from django.views.decorators.cache import cache_page
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.utils.html import conditional_escape
from django.db.models import Q
from django.core.mail import send_mail

from datetime import datetime
from random import sample
from mailshelf import messages
from utils.decorators import r_to
from utils.utils import set_paginator_window
# from haystack.query import SearchQuerySet

from apps.catalog.models import (
    Category,
    Item,
    Catalog,
    ItemVideo,
    Order,
    OrderItem,
    Vendor
)
from apps.website.models import Website
# from forms import FilterForm


#@cache_page(60 * 15)
@r_to('index.html')
def website_index(request):
    items = None
    bestsellers = None
    if request.website.catalog:
        items = Item.objects.filter(price__gt=0, category__catalog=request.website.catalog)#.cache()
        bestsellers = items.filter(bestseller=True)#.cache()
        amount = min(len(items), 6)
        if bestsellers:
            items = items.filter(bestseller=False)
        if items:
            items = sample(items, amount)
        amount = min(len(bestsellers), 6)
        if Website.SKINS.get_name(request.website.skin) == "TECHNO" or Website.SKINS.get_name(request.website.skin) == "NARWIK":
            amount = min(len(items), 4)
            if items:
                items = sample(items, amount)
            amount = min(len(bestsellers), 8)
        bestsellers = sample(bestsellers, amount)
    return {'items': items, 'bestsellers': bestsellers}


#@cache_page(60 * 15)
@r_to('index.html')
def filter_by_cat(request, cat_id):
    sub_items = []
    vendors = []
    cat_obj = get_object_or_404(
        Category, id=cat_id, catalog__website=request.website)
    if cat_obj.is_leaf_node():
        items = Item.objects.filter(
            category=cat_obj,
            category__catalog__website=request.website
        )  # .cache()
        vendor_id = set(items.exclude(
            vendor_id=None).values_list(
            'vendor_id', flat=True))
        vendors = Vendor.objects.filter(
            id__in=vendor_id).values_list('name', flat=True).order_by('name')

    else:
        items = None
    # form = FilterForm(request.GET or None, category=cat_obj)
    # if request.method == 'GET' and form.is_valid() and form.cleaned_data:
    #     sqs = []
    #     for k, v in form.cleaned_data.items():
    #         sqs.append(Q(parameters__icontains='''"%s": "%s"''' % (k, v)))
    #     items = Item.objects.filter(category=cat_obj, category__catalog__website=request.website, *sqs)
    if request.method == 'GET' and request.GET.get('f'):
        items = items.filter(vendor__in=request.GET.getlist('vendor'))#.cache()
        # print request.GET.getlist('vendor')
    p = Paginator(items, 12)
    if not items:
        sub_items = Category.objects.filter(parent=Category.objects.get(id=cat_id))#.cache()
        p = Paginator(sub_items, 12)
    try:
        page = p.page(request.GET.get('p', 1))
    except PageNotAnInteger:
        page = p.page(1)
    except EmptyPage:
        page = p.page(p.num_pages)
    set_paginator_window(page)
    return {'items': items, 'sub_items': sub_items, 'page': page, 'category': cat_obj, 'vendors': vendors}


@r_to('item_page.html')
def item_page(request, item_id):
    item = get_object_or_404(Item, id=item_id, category__catalog=request.website.catalog)
    try:
        video = ItemVideo.objects.get(item=item)
        video_url = video.url.replace('watch?v=', 'embed/')
    except ItemVideo.DoesNotExist:
        video_url = None
    parent = item.category
    item.hit_counter += 1
    item.save()
    return {'item': item, 'video_url': video_url, 'parent': parent}


def add_to_basket(request, item_id):
    if not request.website_private_session.get('basket'):
        request.website_private_session['basket'] = []
    if not request.website_private_session.get('quantity'):
        request.website_private_session['quantity'] = {}
    request.website_private_session['basket'].append(int(item_id))
    request.website_private_session['quantity'][int(item_id)] = 1
    request.website_private_session.modified = True

    return redirect('item_page', item_id=item_id)


def clean_basket(request):
    if request.website_private_session.get('basket'):
        request.website_private_session['basket'] = []
        request.website_private_session['quantity'] = {}
    return redirect(request.META.get('HTTP_REFERER', '/'))


def rm_from_basket(request, pos):
    b = request.website_private_session.get('basket')
    p = b.index(int(pos))
    del request.website_private_session.get('basket')[p]
    del request.website_private_session.get('quantity')[int(pos)]
    request.website_private_session.modified = True
    return redirect('view_basket')


@r_to('basket.html')
def view_basket(request):
    basket_list = request.website_private_session.get('basket')
    q = request.website_private_session.get('quantity')
    a = 0.0
    items = []
    if basket_list:
        items = Item.objects.filter(id__in=basket_list)
        for item in items:
            setattr(item, 'quantity', q[item.id])
            total = int(q[item.id]) * float(item.get_price())
            setattr(item, 'total', total)
            a += total
    return {'items': items, 'sum': a}


def recalculate(request):
    if request.method == 'POST':
        data = request.POST.copy()
        del data['csrfmiddlewaretoken']
        for item in data.items():
            request.website_private_session['quantity'][int(item[0])] = int(item[1])
        request.website_private_session.modified = True
        return redirect('view_basket')


### orders
@r_to('order.html')
def order(request, status=None, order_id=None, stat_b=None):
    sum_order = request.website_private_session.get('sum_order')
    request.website_private_session['sum_order'] = []
    return {'status': status, 'order_id': order_id, 'stat_b': stat_b, 'sum_order': sum_order}


def make_order(request):
    items = Item.objects.filter(id__in=request.website_private_session.get('basket'))
    total = sum([float(item.get_price()) for item in items])
    request.website_private_session['sum_order'] = total
    try:
        m = Order.objects.latest('id').id
    except Order.DoesNotExist:
        m = 1
    order = Order.objects.create(number='%s%s' % (datetime.now().strftime('%d%m%y'), m),
                                 catalog=request.website.catalog,
                                 email=request.POST.get('email'),
                                 phone=request.POST.get('phone'),
                                 description=request.POST.get('description'),
                                 contact='%s %s' % (request.POST.get('first_name'), request.POST.get('last_name')),
                                 cost=total)
    stat_b = 2 if request.POST.get('privat24') else 1
    for item in request.website_private_session.get('quantity').items():
        order_item = Item.objects.get(id=item[0])
        OrderItem.objects.create(order=order, item=order_item, quantity=item[1], cost=order_item.get_price())
    try:
        send_mail(u'Ваш заказ на сайте %s' % request.website,
                  u'Ваше имя: %s %s. Телефон: %s. Товаров: %s. Сумма: %s' % (
                                                request.POST.get('first_name'),
                                                request.POST.get('last_name'),
                                                request.POST.get('phone'),
                                                len(items),
                                                total
                                        ),
                'no-reply@%s' % request.website,
                [request.POST.get('email')],
                fail_silently=False
        )
        #messages.ORDER_CLIENT.send(request.POST.get('email'),
        #                           **{'first_name': request.POST.get('first_name'),
        #                              'last_name': request.POST.get('last_name'),
        #                              'phone': request.POST.get('phone'),
        #                              'email': request.POST.get('email'),
        #                              'items': items,
        #                              'total': total})

        admin_email = request.website.user.email
        send_mail(u'Заказ на сайте %s' % request.website,
                  u'Имя покупателя: %s %s. Телефон: %s. Товаров: %s. Сумма: %s' % (
                                                request.POST.get('first_name'),
                                                request.POST.get('last_name'),
                                                request.POST.get('phone'),
                                                len(items),
                                                total
                                        ),
                'no-reply@%s' % request.website,
                [admin_email],
                fail_silently=False
        )
        #messages.ORDER_ADMIN.send(admin_email,
        #                          **{'first_name': request.POST.get('first_name'),
        #                             'last_name': request.POST.get('last_name'),
        #                             'phone': request.POST.get('phone'),
        #                             'email': request.POST.get('email'),
        #                             'items': items,
        #                             'total': total})
    except Exception:
        return redirect('order_status', status=0, order_id=order.number, stat_b=stat_b)
    request.website_private_session['basket'] = []
    return redirect('order_status', status=1, order_id=order.number, stat_b=stat_b)


@r_to('search.html')
def search(request):
    try:
        sTerm = request.GET['q']
    except:
        return {}
    # results = SearchQuerySet().auto_query(sTerm).filter(website='%s' % request.website)
    results = []
    p = Paginator(results, 15)
    try:
        page = p.page(request.GET.get('p', 1))
    except PageNotAnInteger:
        page = p.page(1)
    except EmptyPage:
        page = p.page(p.num_pages)
    set_paginator_window(page)
    return {'items': results, 'page': page}


def exportYML(request):
    catalog = Catalog.objects.get(website=request.website)
    categories = Category.objects.filter(catalog=catalog)
    items = Item.objects.filter(category__in=categories, site=request.website)
    xml_data = []
    xml_data.append("<yml_catalog date='%s'>" % datetime.now().strftime("%Y-%m-%d %H:%M"))
    xml_data.append('<shop>')
    xml_data.append('<name>%s</name><company>%s</company>' % (request.website.name, request.website.name))
    xml_data.append('<url>%s</url>' % request.website)
    xml_data.append("<currencies><currency id='UAH' rate='1'/></currencies>")
    xml_data.append('<categories>')
    for row in categories:
        xml_data.append("<category id='%s'" % row.id)
        if row.parent:
            xml_data.append(" parentId='%s'" % row.parent.id)
        xml_data.append('>%s</category>' % conditional_escape(row.name))
    xml_data.append('</categories>')
    xml_data.append('<offers>')
    for row in items:
        xml_data.append("<offer id='%s'" % row.id)
        if row.stock == row.STATUS.IN_STOCK:
            xml_data.append(" available='true'")
        xml_data.append('><categoryId>%s</categoryId>' % row.category.id)
        xml_data.append('<name>%s</name>' % conditional_escape(row.name))
        xml_data.append('<description>')
        if row.description:
            xml_data.append(conditional_escape(row.description))
        xml_data.append('</description>')
        xml_data.append('<url>http://%s/w/ip/%s/</url>' % (request.website, row.id))
        xml_data.append('<picture>')
        if row.image_url:
            xml_data.append(conditional_escape(row.image_url))
        xml_data.append('</picture>')
        xml_data.append('<currencyId>UAH</currencyId>')
        xml_data.append('<price>%s</price>' % row.get_price())
        xml_data.append('</offer>')
    xml_data.append('</offers>')
    xml_data.append('</shop>')
    xml_data.append("</yml_catalog>")
    return HttpResponse(xml_data, content_type='text/xml')

