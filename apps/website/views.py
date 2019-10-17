# -*- coding: utf-8
import random
import re
from os import sys
from string import maketrans
import base64
from django.utils import formats

from django.shortcuts import redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
import json
from django.views.decorators.cache import cache_page
# from django.utils.html import conditional_escape

from django.utils.html import strip_tags
from django.conf import settings
from django.views.generic import ListView
from django.utils import timezone
from django.utils.encoding import smart_text

from apps.website.search import SphinxSearcher
from utils.decorators import render_to
from forms import SiteEditForm, UserSpaceForm
# from haystack.query import SearchQuerySet, SQ
import pygeoip

from endless_pagination.decorators import page_template
from django.template import RequestContext
from django.shortcuts import render_to_response

from apps.catalog.models import Item, Catalog
from models import UserSpace
from models import Website, WebsiteProperty, Point
from apps.account.forms import SignupForm2
from apps.catalog.forms import ExprofileEditForm
from apps.catalog.tasks import force_reindex
from apps.website.const import CHAR_MAP
from apps.manager.models import Banner
from apps.section.models import ProductModel
from apps.coupon.models import Coupon
from apps.coupon.forms import GetCoupon
from apps.coupon.utils import send_coupon_user, send_coupon_store
from apps.distribution.models import Subscriber, CouponSubscriber
from apps.dashboard.models import History , Wishlist

from .search import product_search
from utils.sphinxapi import *

@login_required
#@render_to('site_settings.html')
def site_settings(request):
    # if request.user.website:
    #     print request.user.website.web_property
    #     print "request.user.website:"
    website_property = WebsiteProperty.objects.get(id=request.user.website.web_property_id)
    initial = {'rate': request.user.website.catalog.rate}
    form = SiteEditForm(instance=request.user.website, initial=initial, website_property=website_property)
    if request.method == 'POST':
        form = SiteEditForm(request.POST, request.FILES, instance=request.user.website)
        if form.is_valid():
            form.save()
            c = request.user.website.catalog
            c.rate = form.cleaned_data.get('rate')
            c.save()
            return redirect('site_settings')
    #return {'form': form, 'website_property': website_property}
    return render_to_response('site_settings.html', {'form': form, }, context_instance=RequestContext(request))


#@render_to('themes/findinshop/index.html')
@render_to('themes/findinshop/red/index.html')
def index(request):
    banners = Banner.objects.filter(active=True)
    return {'banners': banners}


@render_to('website.html')
def website(request):
    sites = Website.objects.all()
    return {'site': sites}


def sphinx_test(request):
    sphinx=SphinxClient()
    sphinx.SetLimits(0,settings.SPHINX_MAX_MATCHES)
    result = sphinx.Query('nokia')
    sphinx.SetFilterRange ("price", 300, 400)
    context_dict={'res' : result,'dic':result["matches"],"keys":result.keys()}
    # for k,v in result.items():
    #     if k!="matches":
    #         print k,v
    return render_to_response('sphinx_test.html',context_dict) 

class SearchView(ListView): 
    template_name = 'themes/findinshop/red/search.html'
    queryset = Item.objects.none()

    def get_context_data(self, *args, **kwargs):
        context = super(SearchView, self).get_context_data(*args, **kwargs)
        # search_backend = getattr(settings, "SEARCH_BACKEND")
        context.update(product_search(self.request))#&&&&&&&&&&&&&
        # TODO change all
        # print context
        # for co in context :
        #     print co

        if 'filter_setting' in self.request.session:
            filter_mode = True
        else:
            filter_mode = False
        context['filter_mode'] = filter_mode
        context['form_get_coupon'] = GetCoupon()
        context['sphinx_backend'] = True
        return context

'''
@cache_page(60 * 15)
@page_template('themes/findinshop/find.html')
def search(request, template='themes/findinshop/red/search.html', extra_context=None):
    country_dict = {}
    country_code = None
    country_codes_list = []
    countries = []
    country_selected = ''
    gi4 = pygeoip.GeoIP(settings.GEOIP_FILE_PATH, pygeoip.MEMORY_CACHE)
    ip = request.META.get('REMOTE_ADDR', None)
    if ip:
        country_code = gi4.country_code_by_addr(ip)
    vendor_list = []
    store_list = []
    try:
        sTerm = request.GET['q']
        # min_price = request.GET.get('min_price')
        # max_price = request.GET.get('max_price')
        vendor_list = request.GET.getlist('vendor')
        store_list = request.GET.getlist('store')
        country_selected = request.GET.get('country', None)
        res_search = 1
    except:
        res_search = 0
        sTerm = 'QuickHackForHandle500_NeedSolution'

    normal_sTerm = sTerm.replace(u'купить', '')
    results = []
    results = SearchQuerySet().auto_query(normal_sTerm).exclude(SQ(price__lt=0.01) | SQ(image_url__contains='no_image.png')).order_by('-click_cost')
    if not results:
        transtable = maketrans(CHAR_MAP['en'], CHAR_MAP['ru'])
        normal_sTerm = normal_sTerm.replace(u'regbnm', '').encode('cp1251').translate(transtable
                                        # cp1251 - магия для того, чтобы была
                                        # равная длина строк в maketrans
                                        ).decode('cp1251').strip()
        results = SearchQuerySet().auto_query(normal_sTerm).exclude(SQ(price__lt=0.01) | SQ(image_url__contains='no_image.png')).order_by('-click_cost')
        if not results:
            normal_sTerm = sTerm.replace(u'купить', '')

    countries = sorted(set([item.country for item in results if item.country]))

#    if country_code and not country_selected:
        #results = results.filter(country=country_code)
    #request.session['my_country'] = country_code
    if country_code and country_selected:
        request.session['my_country'] = country_selected
    c = request.session.get('my_country') or country_code
    if c in Catalog.COUNTRIES._enums:
        results = results.filter(country=c)
    #price_bounds = [int(item.price) for item in results]
    #min_bound = min(price_bounds) if price_bounds else 10
    #max_bound = max(price_bounds) if price_bounds else 30000
    #min_price = min_price if isinstance(min_price, int) else min_bound
    #max_price = max_price if isinstance(max_price, int) else max_bound
    vendors = sorted(set([item.vendor.lower().capitalize() for item in results if item.vendor]))
    stores = sorted(set([item.store.lower().capitalize() for item in results if item.store]))
    #if min_price and max_price:
    #    results = results.filter(price__gt=float(min_price), price__lt=float(max_price))
    #else:
    #results = unfiltered_results
    if vendor_list:
        results = results.filter(vendor__in=vendor_list)
    if store_list:
        results = results.filter(store__in=store_list)
    #price_results = [int(item.price) for item in results]
    #min_price = min(price_results) if not min_price else min_price
    #max_price = max(price_results) if not max_price else max_price
    for c in countries:
        country_dict[c] = Catalog.COUNTRIES.get_title(Catalog.COUNTRIES._enums.get(c))

    if 'filter_setting' in request.session:
        filter_mode = True
    else:
        filter_mode = False

    context = {
        'country_dict': country_dict,
        'entries': results,
        #'min_price': min_price,
        #'max_price': max_price,
        #'min_bound': min_bound,
        #'max_bound': max_bound,
        'vendors': vendors,
        'stores': stores,
        'countries': countries,
        'country_code': country_code,
        'res_search': res_search,
        'query': normal_sTerm,
        'filter_mode': filter_mode
    }
    if extra_context is not None:
        context.update(extra_context)
    return render_to_response(template, context, context_instance=RequestContext(request))
'''

def search_autocomplete(request):
    try:
        query = request.GET.get('term')
    except:
        return {}
    print '!!!!!!!!!!!!!!!!!!!!!!!!!!!!', query
    # sphinx.SetFilter('name',query)

    #results = SearchQuerySet().filter(item_name=sTerm).values_list('item_name', flat=True)[:20]
    search = SphinxSearcher()
    results = search.autocomplete(query)    
    return HttpResponse(simplejson.dumps(results), content_type="application/json")


@login_required
@render_to('spaces.html')
def spaces(request):
    spaces = UserSpace.objects.filter(website=request.user.website)
    return {'spaces': spaces}


@login_required
@render_to('spaces_edit.html')
def spaces_edit(request, space_id):
    inst = UserSpace.objects.get(id=space_id)
    form = UserSpaceForm(instance=inst)
    if request.method == 'POST':
        form = UserSpaceForm(request.POST, request.FILES, instance=inst)
        if form.is_valid():
            form.save()
            return redirect('spaces')
    return {'form': form}


@login_required
def create_cookie_js(request):
    if request.user.website.domain:
        javascript = "document.cookie=\"%s=%s; domain=%s; path=/;\"" % ('sessionid', request.session._session_key, request.user.website.domain)
        return HttpResponse(javascript, content_type="text/javascript")
    else:
        return HttpResponse('', content_type="text/javascript")


# @staff_member_required
#     force_reindex.delay()
#     return redirect('index')


def filter_setting(request):
    if not 'filter_setting' in request.session:
        request.session['filter_setting'] = True
    else:
        del request.session['filter_setting']

    return HttpResponse(json.dumps({'status': 'ok'}), content_type='application/json')


def wishlist(request):   
    if request.GET:
        if request.user.is_authenticated():
            item = Item.objects.get(id=int(request.GET.get('item_id')))
            uniq = str(item.id) + ',' +str(request.user.id)
            wishlist = Wishlist()
            wishlist.uniq = uniq
            wishlist.item = item
            wishlist.user = request.user
            try :
                wishlist.save()
                res = {"OK":200}
            except:
                res = {}
        else:
            res = {'fail': 'user is not authenticated'}
    return HttpResponse(json.dumps(res), content_type="application/json")

#def History():
#    return None

#@cache_page(60 * 15)
def get_item_info(request):
    info = {}
    if True: #request.is_ajax():
        item = get_object_or_404(Item.objects.select_related(), id=int(request.GET.get('item')))
        if request.user.is_authenticated():
            history = History()
            history.item = item
            history.user = request.user
            history.save()
        info['description_short'] = strip_tags(item.description[:200])
        info['description_full'] = strip_tags(item.description[200:])
        info['name'] = item.name
        info['id'] = item.id
        info['store_name'] = item.site.name if item.site.name else "Нет"
        info['map_stores'] = True if Point.objects.filter(user=item.site.user.id, on_map=True) else False
        info['map_stores_url'] = '%s' % (reverse('map_stores', args=[item.site.user.id]))

        info['price'] = item.get_price()
        info['currency'] = item.get_currency()[:3]
        # info['phone'] = item.get_phone()
        info['phone'] = item.get_phone_call_center() or '-'
        info['url'] = item.get_url()
        info['image_url'] = item.get_image_url()
        ex_profile = item.get_ExtendedProfile()
        if ex_profile:
            ex_profile = ex_profile[0]
            # info['store_name'] = ex_profile.get('store_name', '')
            # info['city'] = ex_profile[0][1] if ex_profile[0][1] else "Нет"
            # It is not clear code
            x = 0
            e_prf = [int(x) for x in re.sub(
                r'\D', ',', ex_profile.get('delivery', [])).split(',') if x]
            daliv = ""
            fl = 0
            for k in e_prf:
                if fl > 0:
                    daliv = daliv + ", "
                fl = k
                try:
                    daliv = daliv + str(ExprofileEditForm.TRANS_COMP[k-1][1])
                except IndexError:
                    # Catch problem with old data
                    pass
            info['delivery'] = daliv if daliv else "Нет"

            paym = ""
            fl = 0
            e_prf2 = [int(x) for x in re.sub(
                r'\D', ',', ex_profile.get('payment_methods', [])).split(',') if x]
            for k in e_prf2:
                if fl > 0:
                    paym = paym + ", "
                fl = k
                try:
                    paym = paym + str(ExprofileEditForm.PAY_OPTION[k-1][1])
                except:
                    pass
            info['payment_methods'] = paym if paym else "Нет"
            info['credit_sale'] = "Да" if ex_profile.get('credit_sale') else "Нет"
            info['nds'] = "Да" if ex_profile.get('nds') else "Нет"
            info['wholesale_trade'] = "Да" if ex_profile.get('wholesale_trade') else "Нет"
            info['store_address'] = ex_profile.get('store_address', '')
        else:
            # info['store_name'] = "Нет данных"
            info['city'] = "Нет данных"
            info['delivery'] = "Нет данных"
            info['credit_sale'] = "Нет данных"
            info['nds'] = "Нет данных"
            info['wholesale_trade'] = "Нет данных"
            info['payment_methods'] = "Нет данных"
            info['store_address'] = "Нет данных"

        # Product_models
        product_model = ProductModel.objects.filter(items=item)
        connect_items = []
        connect_items_count = 0
        if product_model:
            connect_items_count = product_model[0].items.count()
            if connect_items_count > 1:
                for connect_item in product_model[0].items.exclude(
                        pk=item.pk).filter(price__gt=0).order_by('price')[:5]:
                    connect_items.append({
                        'site': connect_item.site.name if connect_item.site.name else "Нет",
                        'price': connect_item.price
                    })
            else:
                connect_items = False
            info['product_set_url'] = "/section/{0}/".format(product_model[0].get_absolute_url())

        else:
            connect_items = False
        info['connect_items'] = connect_items
        info['connect_items_count'] = connect_items_count
        #'%s' % (reverse('product_set', args=[product_model[0].slug])) if product_model else ''

        #coupon
        info['coupon_exist'] = False
        coupon = Coupon.objects.filter(
            items=item, date_end__gt=timezone.now())
        if coupon:
            # Use only first coupon
            info['coupon'] = coupon[0].id
            info['coupon_exist'] = True
            info['coupon_size'] = u'%s%s' % (
                coupon[0].size, u' грн' if coupon[0].types == 'F' else '%')
            info['coupon_expire'] = u'%s' % formats.date_format(
                coupon[0].date_end, "SHORT_DATETIME_FORMAT")

    return HttpResponse(json.dumps(info))


from django.views.generic import View
from django.http import JsonResponse
import re

def validate_coupon_form(request):
        answer = {'status': 'error'}
        data = request.GET.get('post_data')

        name = re.findall(r'(?<=name=)[^&$]+', data)[0]
        email = re.findall(r'(?<=email=)[^&$]+', data)[0].replace('%40', '@')
        phone = re.findall(r'(?<=phone=)[^&$]+', data)[0]
        coupon = re.findall(r'(?<=coupon=)[^&$]+', data)[0]
        item_id = re.findall(r'(?<=item=)[^$]+', data)[0]

        if coupon:
            # coupon = self.request.GET.get('coupon', '9')
            # item_id = self.request.GET.get('item', '1')
            # form = GetCoupon(self.request.GET)
            # if form.is_valid() and coupon:
            # save user
            subscriber, subscriber_created = Subscriber.objects.get_or_create(email=email)
            if subscriber_created:
                subscriber.first_name = name
                subscriber.phone = phone
                subscriber.status = 1
                subscriber.save()
            # count user for coupon + 1
            coupon = Coupon.objects.get(id=coupon)
            coupon.count += 1
            coupon.save()
            # save cupon
            item = Item.objects.get(id=item_id)
            obj, created = CouponSubscriber.objects.get_or_create(
                subscriber=subscriber,
                price=item.price,
                coupon=coupon,
                product_name=item.name,
                product_group=item.category.name,
                market_name=item.site.name
            )
            if not created:
                obj.count += 1
                obj.save()
            # send sms
            # send email
            email_context = {
                'coupon': coupon.code,
                'name': subscriber.first_name,
                'store_name': item.site.name,
                'item_name': item.name,
                'item_link': item.url,
                'store_phone': item.site.phone_call_center
                if item.site.phone_call_center else ''
            }


            send_coupon_user(subscriber.email, context=email_context)
            # send email to store
            send_coupon_store(coupon, subscriber.first_name, subscriber.email)

            answer = {
                'status': 'ok',
                'code': coupon.code,
                'store': u'%s' % item.site,
                'store_name': item.site.name,
                'redirect': u'<a href="http://%s/?coupon=%s">Использовать купон</a>' % (
                item.site, coupon.code)

            }
            return JsonResponse(answer, safe=False)
        else:
            return HttpResponse(json.dumps(answer), content_type="application/json")



            
# class ValidateCouponForm(View):
#
#     def post(self, request, *args, **kwargs):
#         answer = {'status': 'error'}
#         data = self.request.POST.get('post_data')
#
#         name = re.findall(r'(?<=name=)[^&$]+', data)[0]
#         email = re.findall(r'(?<=email=)[^&$]+', data)[0].replace('%40', '@')
#         phone = re.findall(r'(?<=phone=)[^&$]+', data)[0]
#         coupon = re.findall(r'(?<=coupon=)[^&$]+', data)[0]
#         item_id = re.findall(r'(?<=item=)[^$]+', data)[0]
#
#         if coupon:
#             # coupon = self.request.GET.get('coupon', '9')
#             # item_id = self.request.GET.get('item', '1')
#             # form = GetCoupon(self.request.GET)
#             # if form.is_valid() and coupon:
#             #save user
#             subscriber, subscriber_created = Subscriber.objects.get_or_create( email=email )
#             if subscriber_created:
#                 subscriber.first_name = name
#                 subscriber.phone = phone
#                 subscriber.status = 1
#                 subscriber.save()
#             #count user for coupon + 1
#             coupon = Coupon.objects.get(id=coupon)
#             coupon.count += 1
#             coupon.save()
#             #save cupon
#             item = Item.objects.get(id=item_id)
#             obj, created = CouponSubscriber.objects.get_or_create(
#                 subscriber=subscriber,
#                 price=item.price,
#                 coupon=coupon,
#                 product_name=item.name,
#                 product_group=item.category.name,
#                 market_name=item.site.name
#             )
#             if not created:
#                 obj.count += 1
#                 obj.save()
#             #send sms
#             #send email
#             email_context = {
#                 'coupon': coupon.code,
#                 'name': subscriber.first_name,
#                 'store_name': item.site.name,
#                 'item_name': item.name,
#                 'item_link': item.url,
#                 'store_phone': item.site.phone_call_center
#                 if item.site.phone_call_center else ''
#             }
#
#             print('email_context')
#             #  TODO - тут жопа
#             # send_coupon_user(subscriber.email, context=email_context)
#             print('send_coupon_user')
#             #send email to store
#             # send_coupon_store(coupon, subscriber.first_name)
#
#             answer = {
#                 'status': 'ok',
#                 'code': coupon.code,
#                 'store': u'%s' % coupon.user.website,
#                 'store_name': coupon.user.website.name,
#                 'redirect': u'<a href="http://%s/?coupon=%s">Использовать купон</a>' % (coupon.user.website, coupon.code)
#
#             }
#             print(answer)
#             return JsonResponse(answer, safe = False)
#         else:
#             return HttpResponse(json.dumps(answer), content_type="application/json")

