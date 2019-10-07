# -*- coding: utf-8 -*-

from apps.website.models import Point
from .base import BaseReader
from apps.catalog.models import Category, Item, Vendor
from apps.catalog.static_names import Color

from django.db import transaction
from django.core.exceptions import MultipleObjectsReturned

import xml.etree.cElementTree as ET

import traceback


FIELDS_MAPS = {
    'currency': './shop/currencies/currency',
    'category': './shop/categories/category',
    'offer': './shop/offers/offer',
    'outlets': './shop/outlets/outlet'

}

FIELDS_ITEM = ('inner_id', 'category_id')

ITEM_FILED = (
    ('url', 'url'),
    ('price', 'price'),
    ('name', 'name'),
    ('description', 'description'),
    ('picture', 'image_url'),
    ('currencyId', 'currency'),

)

EXTRA_PARAM = (
    ('color', (u'цвет', u'color')),
    ('gender', (u'пол',))
)

COLOR_SPLIT = (',', '-', '/', '+')


class YmlReader(BaseReader):
    """YmlReader"""

    def __init__(self, *args, **kwargs):
        super(YmlReader, self).__init__(*args, **kwargs)
        self.category = {}
        self.outlets = {}
        self.delete_category_id = []
        self.old_items = []
        self.new_items = []
        self.market_url = None

    def _get_data(self):
        self.tree = ET.parse(self.source_file)
        self.root = self.tree.getroot()
        self.market_url = self.root.findall('shop')[0].findtext('url')

    def _get_category(self):
        for item in self.root.findall(FIELDS_MAPS['category']):
            self.category[item.get('id')] = {
                'parrent_inner_id': item.get('parentId'),
                'name': item.text
            }

    def _get_database_category(self):
        """
            Return a dict:
                {
                    inner_id: {
                        'inner_id': 1,
                        'id': 32317,
                        'parent': 32316,
                        'name': u'SS'
                    }
                }
        """
        _new_dict = {}
        for item in Category.full.values(
                'inner_id', 'parrent_inner_id', 'id',
                'parent', 'name', 'deleted').filter(
            catalog=self.catalog):
            _new_dict[item.get('inner_id')] = item
            if not self.category.get(item.get('inner_id')):
                self.delete_category_id.append(item.get('id'))
            else:
                self.category[item.get('inner_id')]['id'] = item.get('id')
        return _new_dict

    def create_new_category(self):
        """
            Create new Category
        """
        for inner_id, item in self.category.iteritems():
            if not item.get('id'):
                cat = Category.objects.create(
                    name=item.get('name'),
                    catalog=self.catalog,
                    inner_id=inner_id,
                    parrent_inner_id=item.get('parrent_inner_id')
                )
                self.category[inner_id]['id'] = cat.id

    def delete_category(self):
        """
            Hide category
        """
        if self.delete_category_id:
            Category.objects.filter(
                id__in=self.delete_category_id).update(deleted=True)

    def get_parent_id(self, parent):
        """
            Get parent_id
        """
        if parent and parent != '0':
            if not self.category.get(parent):
                return None
            if self.category.get(parent).get('id'):
                return self.category.get(parent).get('id')
            else:
                db_parent = Category.full.get(
                    inner_id=parent,
                    catalog=self.catalog
                )
                return db_parent.id
        return None

    def process_category(self):
        """
            Category Process
        """
        self._get_category()
        databas_dict = self._get_database_category()
        self.delete_category()
        self.create_new_category()
        with transaction.atomic():
            with Category.tree.disable_mptt_updates():
                for inner_id, item in self.category.iteritems():
                    cat = databas_dict.get(inner_id)
                    if not cat:
                        parent_id = self.get_parent_id(
                            item.get('parrent_inner_id')
                        )
                        if parent_id:
                            try:
                                cat = Category.full.get(
                                    inner_id=inner_id,
                                    catalog=self.catalog)
                                cat.parent_id = parent_id
                                cat.save()
                            except Category.DoesNotExist:
                                # Log error
                                pass
                    else:
                        if cat.get('name') != item.get('name') or \
                                        cat.get('parrent_inner_id') != item.get(
                                    'parrent_inner_id') or cat.get('deleted'):
                            try:
                                cat = Category.full.get(
                                    inner_id=inner_id,
                                    catalog=self.catalog)
                                cat.parent_id = self.get_parent_id(
                                    item.get('parrent_inner_id')
                                )
                                cat.name = item.get('name')
                                cat.deleted = False
                                cat.save()
                            except Category.DoesNotExist:
                                # Log error
                                pass

    def populate_price(self, price):
        return float(price.replace(',', '.'))

    def populate_vendor(self, vendor):
        # TODO include redis
        if vendor:
            instance, created = Vendor.objects.get_or_create(
                name=vendor.strip().lower())
            return instance.pk
        return

    def populate_category(self, category_id):
        if not category_id:
            return
        if not self.category.get(category_id):
            return
        return self.category.get(category_id).get('id')

    def boolen_populate(self, value):
        if value.strip().lower() == 'true':
            return True
        return False

    def _return_color_item(self, color_list):
        result = []
        for color in color_list:
            if color and color != '':
                result.append(Color.get_id(color))
        return ','.join(str(n) for n in result)

    def populate_color(self, value):
        for item in COLOR_SPLIT:
            if len(value.split(item)) > 1:
                return self._return_color_item(
                    value.split(item))
        return self._return_color_item(value.split())

    def populate_gender(self, value):
        return Item.GENDER.get_keys(value)

    def populate_params(self, param):
        """
            Return a dict with values
                {'color': u'aa'}
        """
        if param.get('name'):
            for k, v in EXTRA_PARAM:
                if unicode(param.get('name').lower()) in v:
                    # Check if param exist
                    if param.text:
                        if hasattr(self, 'populate_%s' % k):
                            methodToCall = getattr(self, 'populate_%s' % k)
                            value = methodToCall(param.text.lower())
                            return {k: value}
                        return {k: param.text.lower()}

    def populate_outlet(self, outlet_id):
        if outlet_id:
            return self.outlets.get(outlet_id).get('id')
        return None

    def get_items(self):
        """
            Get item from file
        """
        for item in self.root.findall(FIELDS_MAPS['offer']):
            dict_item = {}
            # Get main values
            for k, v in ITEM_FILED:
                dict_item[v] = item.findtext(k, '').strip()
            try:
                outlets = item.findall('outlets')
                point_ids = []
                if outlets:
                    for outlet in outlets[0].findall('outlet'):
                        point_ids.append(self.outlets[outlet.attrib.get('id')]['pk'])
                dict_item['point_id'] = point_ids
            except:
                self.logger.error(
                    "[%s]Points not found" % self.importtask_id
                )

            #del dict_item['outlets']
            # Populate name
            if not dict_item['name']:
                if item.find('name') is None:
                    dict_item['name'] = item.findtext(
                        'model', 'No model').strip()
                else:
                    dict_item['name'] = 'No name'
            # Price
            dict_item['price'] = self.populate_price(
                dict_item['price'].strip())
            # ID
            dict_item['inner_id'] = item.get('id')
            dict_item['vendor_id'] = self.populate_vendor(
                item.findtext('vendor', '').strip())
            dict_item['category_id'] = self.populate_category(
                item.findtext('categoryId', '').strip())
            # dict_item['point_id'] = self.populate_outlet(
            #     item.findtext('outlet', '').strip())
            dict_item['delivery'] = self.boolen_populate(
                item.findtext('delivery', '').strip())
            dict_item['store'] = self.boolen_populate(
                item.findtext('store', '').strip())
            dict_item['pickup'] = self.boolen_populate(
                item.findtext('pickup', '').strip())
            for param in item.iter('param'):
                param_dict = self.populate_params(param)
                if param_dict:
                    dict_item.update(param_dict)
            if dict_item['url'] == "":
                dict_item['url'] = self.market_url
            yield dict_item

    def get_item(self, inner_id, category_id):
        """
            Get item from database
        """
        try:
            item = Item.objects.get(
                site_id=self.site.id,
                inner_id=inner_id
            )
            return item
        except Item.DoesNotExist:
            return
        except MultipleObjectsReturned:
            Item.objects.filter(
                site_id=self.site.id,
                inner_id=inner_id
            ).delete()
            return

    def is_valid_item(self, date):
        """
            Checking if correct date
        """
        for field in FIELDS_ITEM:
            if not date.get(field):
                return False
        return True

    def update_item(self, data, instance):
        """
            Update Item
        """
        updated = False

        for k, v in data.items():
            existing = getattr(instance, k, None)
            upd_value = False
            if existing is None or existing == "":
                if v:
                    upd_value = True
            elif existing != v:
                upd_value = True
            if upd_value:
                setattr(instance, k, v)
                updated = True
        if updated:
            instance.save()
            self.logger.debug(
                "[%s]Update instance %s" % (self.importtask_id, instance.pk)
            )

    def create_item(self, data):
        """
            Create new Item
        """
        points = data.get('point_id', None)
        del data['point_id']
        item = Item.objects.create(site_id=self.site.pk, **data)
        if points:
            for point in Point.objects.filter(id__in=points):
                item.point.add(point)

        self.logger.debug(
            "[%s]Create new instance" % self.importtask_id
        )

    def process_item(self):
        """
            Item process
        """
        for item in self.get_items():
            if not self.is_valid_item(item):
                continue
            instance = self.get_item(
                item.get('inner_id'), item.get('category_id'))
            if instance:
                self.update_item(item, instance)
            else:
                self.create_item(item)
            self.new_items.append(item.get('inner_id'))

    def get_current_item(self):
        """
            Get current Item
        """
        self.old_items = Item.objects.filter(
            site_id=self.site.id).values_list('inner_id', flat=True)

    def compare_item(self):
        """
            Compare Item
        """
        different_items = list(set(self.old_items) - set(self.new_items))
        for inner_id in different_items:
            try:
                item = Item.objects.get(
                    site_id=self.site.id,
                    inner_id=inner_id,
                )
                item.price = 0
                item.save()
            except MultipleObjectsReturned:
                Item.objects.filter(
                    site_id=self.site.id,
                    inner_id=inner_id
                ).delete()

    def _get_outlets(self):
        try:
            for item in self.root.findall(FIELDS_MAPS['outlets']):
                self.outlets[item.get('id')] = {
                    'name': item.text
                }
        except:
            self.logger.error(
                "[%s]Outlets not found" % self.importtask_id
            )


    def process_outlets(self):
        self._get_outlets()
        if self.outlets:
            user = self.import_catalog.site.user
            outlet_ids = [x['outlet_id'] for x in Point.objects.filter(user=user).values('outlet_id')]
            for outlet in self.outlets.iteritems():
                if outlet[0] not in outlet_ids:
                    point = Point.objects.create(name_1c=outlet[1].get('name'), name=outlet[1].get('name'),
                                                 outlet_id=outlet[0], user=user)
                else:
                    point = Point.objects.filter(outlet_id=outlet[0]).filter(user=user)[0]
                self.outlets[point.outlet_id].update(pk=point.pk)

    def __call__(self):
        super(YmlReader, self).__call__()
        try:
            self._get_data()
            self.logger.debug(self.timer.checkpoint('function get_data()'))
            self.process_category()
            self.process_outlets()
            self.logger.debug(self.timer.checkpoint(
                'function process_category()'))
            self.get_current_item()
            self.process_item()
            self.logger.debug(self.timer.checkpoint('function process_item()'))
            self.compare_item()
            self.logger.debug(self.timer.checkpoint('function compare_item()'))
            self._success_finish_process()
        except Exception:
            error = traceback.format_exc()
            self._err_finish_process(error)
