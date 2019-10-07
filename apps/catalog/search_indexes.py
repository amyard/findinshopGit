# -*- coding: utf-8 -*-
from haystack import indexes

from models import Item, Catalog


class ItemIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    item_name = indexes.NgramField(model_attr='name')
    category = indexes.FacetCharField(model_attr='category')
    vendor = indexes.CharField(model_attr='vendor', null=True)
    website = indexes.CharField(model_attr='site')
    store = indexes.CharField(model_attr='site__name', null=True)
    image_url = indexes.CharField()
    price = indexes.FloatField()
    url = indexes.CharField()
    country = indexes.CharField()
    color = indexes.CharField()
    currency = indexes.CharField()
    test_or = indexes.CharField()
    click_cost = indexes.FloatField()
    express = indexes.BooleanField(model_attr='one_c')

    def get_model(self):
        return Item

    def prepare_test_or(self, obj):
        s = 'OR'
        if Catalog.COUNTRIES.get_name(obj.category.catalog.country) == 'UA':
            s = 'AND'
        return s

    def prepare_country(self, obj):
        return '%s' % Catalog.COUNTRIES.get_name(obj.category.catalog.country)

    def prepare_image_url(self, obj):
        return '%s' % obj.get_image_url()

    def prepare_price(self, obj):
        return obj.get_price()

    def prepare_currency(self, obj):
        return '%s' % Catalog.CURRENCIES.get_title(obj.category.catalog.currency)

    def prepare_url(self, obj):
        return '%s' % obj.get_url()

    def prepare_color(self, obj):
        return obj.color

    def prepare_click_cost(self, obj):
        return obj.click_cost

    def index_queryset(self, using=None):
        return self.get_model().objects.filter()
