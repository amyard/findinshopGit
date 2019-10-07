# -*- coding: utf-8

from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils import simplejson
from django.utils.html import conditional_escape
import simplejson as json

from utils.decorators import render_to
from forms import SiteEditForm, UserSpaceForm
from haystack.query import SearchQuerySet

from endless_pagination.decorators import page_template
from django.template import RequestContext
from django.shortcuts import render_to_response

from apps.catalog.models import Item
from models import UserSpace
from models import Website, WebsiteProperty
from apps.account.forms import SignupForm2
import re


@login_required
@render_to('site_settings.html')
def site_settings(request):
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
    return {'form': form, 'website_property': website_property}


@render_to('index_main.html')
def index(request):
    return {}


@render_to('website.html')
def website(request):
    sites = Website.objects.all()
    return {'site': sites}


@page_template('search/search_page.html')
def search(request, template='index_main.html', extra_context=None):
    try:
        sTerm = request.GET['q']
        res_search = 1
    except:
        res_search = 0
        sTerm = 'QuickHackForHandle500_NeedSolution'
    results = SearchQuerySet().filter(item_name=sTerm)
    if not results:
        results = SearchQuerySet().auto_query(sTerm)
    context = {
        'entries': results,
        'res_search': res_search
    }
    if extra_context is not None:
        context.update(extra_context)
    return render_to_response(template, context, context_instance=RequestContext(request))


def search_autocomplete(request):
    try:
        sTerm = request.GET.get('q')
    except:
        return {}
    results = SearchQuerySet().filter(item_name=sTerm).values_list('item_name', flat=True)[:20]
    return HttpResponse(simplejson.dumps({'options': list(results)}), content_type="application/json")


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
        return HttpResponse(javascript, mimetype="text/javascript")
    else:
        return HttpResponse('', mimetype="text/javascript")

def get_item_info(request):
    info = {}

    if request.is_ajax():
        item = get_object_or_404(Item.objects.select_related(), id=int(request.GET.get('item')))
        info['description'] = item.description
        # info['name'] = request.website.name
        info['price'] = item.get_price()
        info['phone'] = item.get_phone()
        info['url'] = item.get_url()
        info['image_url'] = item.get_image_url()

        ex_profile = item.get_ExtendedProfile()
        if ex_profile:

            info['store_name']      = ex_profile[0][0]
            info['city']            = ex_profile[0][1]

            x=0
            e_prf = [int(x) for x in re.sub(r'\D', ',', ex_profile[0][2]).split(',') if x]
            e_prf2 = [int(x) for x in re.sub(r'\D', ',', ex_profile[0][4]).split(',') if x]
            e_prf3 = [int(x) for x in re.sub(r'\D', ',', ex_profile[0][7]).split(',') if x]

            day_week = ""
            daliv = ""
            paym = ""
            fl=0
            for k in e_prf:
                if fl>0:
                    daliv=daliv+", "
                fl=k
                daliv=daliv+str(SignupForm2.TRANS_COMP[k-1][1])

            fl=0
            for k in e_prf2:
                if fl>0:
                    paym=paym+", "
                fl=k
                paym=paym+str(SignupForm2.PAY_OPTION[k-1][1])

            fl=0
            for k in e_prf3:
                if fl>0:
                    day_week=day_week+", "
                fl=k
                day_week=day_week+str(SignupForm2.DAYS_WEEK[k-1][1])

            info['delivery']=daliv
            info['credit_sale'] = "Да" if ex_profile[0][3] else "Нет"
            info['nds'] = "Да" if ex_profile[0][5] else "Нет"
            info['wholesale_trade'] = "Да" if ex_profile[0][6] else "Нет"
            info['payment_methods'] = paym
            info['mode']            = day_week
            info['time_of']         = "c "+ex_profile[0][8].strftime("%H:%M") +" по "+ex_profile[0][9].strftime("%H:%M")
            info['store_address']   = ex_profile[0][10]

        else:
            info['store_name'] = "Нет данных"
            info['city'] = "Нет данных"
            info['delivery'] = "Нет данных"
            info['credit_sale'] = "Нет данных"
            info['nds'] = "Нет данных"
            info['wholesale_trade'] = "Нет данных"
            info['payment_methods'] = "Нет данных"
            info['mode'] = "Нет данных"
            info['time_of'] = "Нет данных"
            info['store_address'] = "Нет данных"

    return HttpResponse(json.dumps(info), mimetype="application/json")
