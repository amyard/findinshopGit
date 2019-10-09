 # -*- coding: utf-8 -*-
from django.conf import settings
from django.core.urlresolvers import reverse
# from sphinxit.core.processor import Search

from apps.website.models import Website, Point
from apps.catalog.models import Vendor, Item
from apps.catalog.static_names import Color


import logging
import traceback
import itertools
from utils.sphinxapi import *

logger = logging.getLogger('sphinx_search')


class SearchConfig(object):
    DEBUG = settings.DEBUG
    SEARCHD_CONNECTION = {
        'host': settings.SPHINX_HOST,
        'port': settings.SPHINX_PORT,
    }


class SphinxSearcher(object):
    """
        Sphinx searcher over SphinxQL
    """
    def __init__(self, config=SearchConfig):
        self.config = config
        self.last_error = None

    def search_api(self, query=None, filters=None, price_filters=None,
               field_filters=None, colors=None, index=settings.SPHINX_INDEX,
               select_field=None, sort_attr=None, bool_filter=None):
        '''
            query: 'search world'
            filters:  [(name, [values list]), ...]
            price_filters: [(from, to), ...]
            sort_attr: (field, ASC/DESC order) 
            select_field: 'filed, field'
            field_filters: [(name, [values list]), ...](color,gender)
            bool_filters: [(field, True/False), ...]
        '''
        sphinx=SphinxClient()
        sphinx.SetServer(settings.SPHINX_HOST, settings.SPHINX_PORT)
        # function SetRetries ( $count, $delay=0 )
        sphinx.ResetFilters()
        sphinx.SetLimits(0,settings.SPHINX_MAX_MATCHES)
        #move to setting
        sphinx.SetMatchMode(SPH_MATCH_EXTENDED)
        sphinx.SetRankingMode(SPH_RANK_PROXIMITY_BM25)
        # sphinx.SetRankingMode (SPH_RANK_BM25)
        # sphinx.SetRankingMode (SPH_RANK_PROXIMITY )
        field_weights={
                'name': 100,
                'category_name': 20,
                'description': 10}
        sphinx.SetFieldWeights(field_weights) 
        if sort_attr:
            for sort in sort_attr:# change for two attributes
                if sort[1]=='DESC':
                    sphinx.SetSortMode(SPH_SORT_ATTR_DESC, sort[0])
                elif sort[1]=='ASC':
                    sphinx.SetSortMode(SPH_SORT_ATTR_ASC, sort[0])
        else:
            sphinx.SetSortMode(SPH_SORT_RELEVANCE)
    #choise better: by relevance rank or mix of bigger/smaller  SPH_SORT_EXTENDED
        if field_filters:      #color,gender 
            for field in field_filters:
                filters.append(field)
        if filters: 
            for field in filters:
                sphinx.SetFilter(field[0],field[1])
        if price_filters:# foat or integer type??
            price_filters[0]=int(float(price_filters[0]))
            price_filters[1]=int(float(price_filters[1]))
            sphinx.SetFilterRange('price',price_filters[0],price_filters[1],exclude=False)
        if bool_filter:# pickup,store,delivery
            for blfilt in bool_filter:
                sphinx.SetFilter(blfilt[0],1 if blfilt[1] else 0,exclude=False )
                pass
        # if select_field:
            # sphinx.SetFilterString( $attribute, $value, $exclude=false )
        if not query:
            query = ''     
        query = query.replace('/', ' ')#.replace(')', ' ').replace('(', ' ').replace('  ', ' ').strip()
        # q = query.split(" ")
        # q_alt = [ item.replace(item[-1],'**') for item in q ]
        # query +=' | '+' | '.join(q_alt)#+' | '+' | '.join(q)
        result = sphinx.Query(query)
        # print result, '                 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1'
        # print sphinx.GetLastError()
        return result['matches']

    def autocomplete(self, query=None, index=settings.SPHINX_INDEX,):
        sphinx=SphinxClient()
        sphinx.SetServer(settings.SPHINX_HOST, settings.SPHINX_PORT)
        sphinx.ResetFilters()
        sphinx.SetMatchMode(SPH_MATCH_ANY)
        sphinx.SetLimits(0,10)#settings.SPHINX_MAX_MATCHES)
        if query:
            res = sphinx.Query(query)
            res =  res['matches']
            if res:
                a=[] #[{'id':x['id']} for x in res]
                for item in res:
                    a.append({'value:': item['attrs']['name'],'label':  item['attrs']['name'],'id':item['id']})
                return a
            else:
                return []
        else:
            return []

class BaseFindResponse(object):
    """
        Base find response struct.
    """

    def __init__(self, sphinx_res, search_value):
        self.sphinx_res = sphinx_res
        self.search_value = search_value
        self.color,self.gender,self.price,self.vendor_id,self.site_id,self.site_type,self.point_ids = set(),set(),set(),set(),set(),set(),set()
        self.delivery,self.pickup,self.store=set(),set(),set()

    def get_attrs(self):
        for item in self.sphinx_res:
            item.update(item.pop('attrs'))
            self.color.add(item["color"])
            self.gender.add(item["gender"])
            self.price.add(item["price"])
            self.vendor_id.add(item["vendor_id"])
            self.site_id.add(item["site_id"])
            self.site_type.add(item["site_type"])
            self.point_ids.update(set(item["point_ids"]))
            self.pickup.add(item["pickup"])
            self.store.add(item["store"])
            self.delivery.add(item["delivery"])

        pass

    def _is_exist(self, field):
        """
            return True or Field if exist Field True
        """
        return bool([item for item in field if item])

    @property
    def get_site(self):
        ids = self.site_id
        return Website.objects.filter(id__in=ids).values_list(
            'name', flat=True).order_by('name')

    @property
    def get_point(self):
        ids = []
        for point_id in self.point_ids:
            #if point_id.isalnum():
            ids.append(point_id)
        point = Point.objects.filter(id__in=ids).filter(approve=True)
        return point

    @property
    def get_colors(self):
        """
            Convert [u'2', u'2,1'] to ['red', 'white']
        """
        color_list = list()
        for item in self.color:
            if Color.get_name(item):
                color_list.append(Color.get_name(item))
        return sorted(color_list) if self._is_exist(color_list) else False
    @property
    def get_vendor(self):
        result = Vendor.objects.values_list(
            'name', flat=True).filter(
            id__in=self.vendor_id).order_by('name')
        return [item.capitalize() for item in result]

    @property
    def get_gender(self):
        """
            Convert [u'1', u'2'] to ['men', 'women']
        """
        print (self.gender)
        gender_list = [Item.GENDER.get_title(item) for item in self.gender if item != 0]
        return gender_list

    def get_responce(self):
        context = {}
        self.get_attrs()
        context['delivery_show'] = self._is_exist(self.delivery)
        context['store_show'] = self._is_exist(self.store)
        context['pickup_show'] = self._is_exist(self.pickup)
        context['query'] = self.search_value.get('query')
        context['colors'] = self.get_colors
        context['gender'] = self.get_gender
        context['max_price'] = int(max(self.price)) if self.price else 0
        context['min_price'] = int(min(self.price)) if self.price else 0
        context['vendors'] = self.get_vendor
        context['express'] = self.site_type
        context['cities'] = self.get_point
        context['stores'] = self.get_site
        
        context['selected_express'] = self.search_value.get('selected_express')
        context['color_list'] = self.search_value.get('color_list')
        context['vendor_list'] = self.search_value.get('vendor_list')
        context['store_list'] = self.search_value.get('store_list')
        context['price_list'] = self.search_value.get('price_list')
        context['gender_list'] = self.search_value.get('gender_list')
        context['selected_cities'] = self.search_value.get('selected_cities')
        context['delivery'] = True if 'delivery' in self.search_value.get('condition') else False
        context['store'] = True if 'store' in self.search_value.get(
            'condition') else False
        context['pickup'] = True if 'pickup' in self.search_value.get(
            'condition') else False
        context['clean_filter'] = '%s?q=%s' % (reverse('search'), self.search_value.get('query'))
        context['entries'] = self.sphinx_res
        
        #  new min and max value
        search = self.search_value['query']
        res = Item.objects.filter(name__icontains=search, price__gt= 0).values_list('price', flat=True)
        context['new_max_price'] = int(max(res)) if res else 0
        context['new_min_price'] = int(min(res)) if res else 0
        

        # print('--------------------------------')
        # print(search)
        # res = Item.objects.filter(vendor__name=search)
        # res = Item.objects.filter(name__icontains=search, price__gt= 0)
        # for i in res:
        #     print(i.point.name)
        #
        # asd = res[1]
        # print(asd.point.all())
        # res = Item.objects.get(name__icontains=search)
        # for nmb, i in enumerate(res):
        #     print(nmb, i, i.point.all)
        #     for asd in i.point.all():
        #         print(asd)

        # res = Item.objects.filter(name__icontains=search, price__gt=0).order_by('point').values_list('point__name', flat=True).distinct('point')
        # print(res)


        # point = models.ManyToManyField('website.Point', verbose_name=u'Магазин', blank=True)
        # site = models.ForeignKey('website.Website', verbose_name=u'Сайт', blank=True, null=True)

        # name = models.CharField(verbose_name=u'Наименование')
        # print('--------------------------------')


        return context
        # context['filter_mode'] = filter_mode
        # context['country_dict'] = country_dict
        # context['countries'] = countries
        # context['country_code'] = country_code
