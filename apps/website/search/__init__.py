# -*- coding: utf-8 -*-
from django.utils.encoding import smart_text

from .search import SphinxSearcher, BaseFindResponse
from apps.website.models import Website, Point

from apps.catalog.models import Vendor, Item
from apps.catalog.static_names import Color

_all__ = [
    'product_search',
]

"""
Example:
    from apps.website.search.search import SphinxSearcher
    qs = SphinxSearcher()
    qs.search(query=u'Телевизор', field_filters=[('vendor', ['samsung'])])
    qs.search(field_filters=[('color', [u'Белый', u'Чорный'])],
              price_filters=[251, 255])
    qs.search(query=u'Телевизор',
              bool_filter=[('delivery', True), ('one_c', False)],
              sort_attr=('price', 'DESC'))
"""


def prepare_value(request):
    """
        Prepare value
        return: {'query': query, 'filters':..}
    """
    search_value = {}
    search_dict = {}
    field_filters = []
    filters = []
    color_list = []
    bool_filter = []
    gender_list = []
    #get parameters
    sTerm = request.GET.get('q', '')
    if sTerm:
        search_dict['query'] = sTerm.replace(u'купить', '').strip()
    else:
        search_dict['query'] = None
    search_value['vendor_list'] = request.GET.get(
        'vendor').split(',') if request.GET.get('vendor') else []
    if search_value['vendor_list']:
        vendor_list = []
        for item in search_value['vendor_list']:
            try:
                vendor_list.append(Vendor.objects.get(name=item.lower()).pk)
            except Vendor.DoesNotExist:
                pass
        filters.append(('vendor_id', vendor_list))
    if request.GET.get('cities'):
        s_cities = request.GET.get('cities', "").split(',')
        search_value['selected_cities'] = [int(x) for x in s_cities]
        filters.append(('point_ids', search_value['selected_cities']))
    else:
        search_value['selected_cities'] = []

    # if search_value['selected_cities']:
    #     cities_list = Point.objects.filter(city__in=search_value['selected_cities']).values('pk')
    #     filters.append(('city_id', [x['pk'] for x in cities_list]))
    store_list = request.GET.get('store').split(',') if request.GET.get(
        'store') else []
    if store_list:
        #TODO change get storage
        market_id_list = []
        for market_name in store_list:
            market = Website.objects.filter(name=market_name)
            if market:
                market_id_list.append(market[0].id)
        if market_id_list:
            filters.append(('site_id', market_id_list))
    if request.GET.get('express'):
        search_value['selected_express'] = request.GET.get('express')
        market_type_list = []
        for market_type in request.GET.get('express').split(','):
            if not market_type.isdigit():
                continue
            if isinstance(market_type, basestring):
                market_type_list.append(int(market_type))
            else:
                market_type_list.append(market_type)
        if market_type_list:
            filters.append(('site_type', market_type_list))
    price_filters = request.GET.get('price').split(',') if request.GET.get('price') else []
    search_value['color_list'] = request.GET.get('color')
    if request.GET.get('color'):
        color_list = [int(Color.get_id(color))
                      for color in request.GET.get('color').split(',')]
        field_filters.append(('color', color_list))
    search_value['gender_list'] = request.GET.get('gender')
    if request.GET.get('gender'):
        gender_list = [
            int(Item.GENDER.get_keys(item.lower()))
            for item in request.GET.get('gender').split(',')]
        field_filters.append(('gender', gender_list))
    search_dict['field_filters'] = field_filters
    search_dict['price_filters'] = price_filters
    search_dict['filters'] = filters
    search_dict['sort_attr'] = [('price', 'DESC'), ('click_cost', 'DESC')]

    search_value['condition'] = request.GET.get('condition', '')
    if 'delivery' in search_value['condition']:
        bool_filter.append(('delivery', True))
    if 'store' in search_value['condition']:
        bool_filter.append(('store', True))
    if 'pickup' in search_value['condition']:
        bool_filter.append(('pickup', True))
    # SEARCH Value
    search_value['store_list'] = store_list
    search_value['price_list'] = price_filters
    search_value['query'] = search_dict['query']
    #search_value['selected_express'] = request.GET.get('express').split(',')
    #search_value['cities'] = set([x.city for x in Point.objects.all()])

    return search_dict, search_value


def product_search(request):
    qs = SphinxSearcher()
    # Prepare value
    search_dict, search_value = prepare_value(request)
    # Find Items
    search_result = qs.search_api(**search_dict)
    # Prepare response
    rs = BaseFindResponse(search_result, search_value)
    response = rs.get_responce()
    return response


def item_search(name):
    qs = SphinxSearcher()
    ids = [obj['id'] for obj in qs.search_api(query=name, select_field='id')]
    return Item.objects.filter(id__in=ids, price__gt=0)



