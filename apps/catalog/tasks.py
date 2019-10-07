# coding: utf-8
from __future__ import absolute_import

import datetime
import random
import xml.etree.cElementTree as ET
from collections import OrderedDict

import dse
import os
import requests
import xlwt
from django.conf import settings

from apps.catalog.models import (
    Category,
    Item,
    ImportTask,
    ExportTask
)
from celery import task
from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import mail_admins
from django.db.models import Max, Count, Q

from django.template import Context
from fake_useragent import UserAgent
from utils.timer_profile import TimerProfile
from django.template.defaultfilters import slugify

# Findinshop imports
from apps.website.models import Website
from apps.cpa.models import RefreshCostTask, OwnAndUserCategory
from apps.section.models import ProductModel, ProductModelItemConnection
from apps.coupon.models import Coupon
from apps.coupon.utils import send_coupon_report

from apps.importer.reader import YmlReader
from apps.website.search import item_search

import logging
import traceback
import subprocess

import time
from django.core.files.temp import NamedTemporaryFile
from django.core.files import File
import urllib2

import lxml
import lxml.html

from utils2.email import message_send
from utils2.transliterate import transliterate

from apps.catalog.task_parse import Parse

logger = logging.getLogger('importer')

# dse.patch_models(specific_models=[Item, Category])


def get_currency(bank, currency):
    if bank not in ('NBU', 'CBRF') or not currency:
        return None
    if bank == 'NBU':
        URL = 'http://bank-ua.com/export/currrate.xml'
        currency_field = 'item'
        code_field = 'char3'
        size_field = 'size'
        rate_field = 'rate'
    elif bank == 'CBRF':
        URL = 'http://www.cbr.ru/scripts/XML_daily.asp'
        currency_field = 'Valute'
        code_field = 'CharCode'
        size_field = 'Nominal'
        rate_field = 'Value'
    request = urllib2.Request(URL, headers={"Accept": "application/xml"})
    u = urllib2.urlopen(request)
    tree = ET.parse(u)
    root = tree.getroot()
    currencies = root.findall(currency_field)
    node = [curr for curr in root.iter(currency_field) if curr.find(code_field).text == currency][0]
    rate = float(node.find(rate_field).text.replace(',', '.'))
    size = float(node.find(size_field).text.replace(',', '.'))
    return rate / size


@task(ignore_result=True)
def export_processing(task_id):
    task = ExportTask.objects.get(id=task_id)
    task.status = task.STATUS.PROCESSING
    task.start = datetime.datetime.now()
    task.save()
    try:
        wbk = xlwt.Workbook()
        sheet = wbk.add_sheet(u'Экспорт')
        items = Item.objects.filter(category__catalog=task.catalog).order_by('category')
        unique_categories = Category.objects.filter(id__in=set(items.values_list('category', flat=True)))
        index = max([category.level for category in unique_categories]) + 1
        fields = {
            u'Бренд': {'cell_index': index, 'field_name': 'vendor'},
            u'Наименование': {'cell_index': index + 1, 'field_name': 'name'},
            u'Артикул': {'cell_index': index + 2, 'field_name': 'code'},
            u'Код': {'cell_index': index + 3, 'field_name': 'inner_id'},
            u'Описание': {'cell_index': index + 4, 'field_name': 'description'},
            u'Цена USD': {'cell_index': index + 5, 'field_name': 'priceRUSD'},
            u'Цена UAH': {'cell_index': index + 6, 'field_name': 'priceRUAH'},
            u'Наличие': {'cell_index': index + 7, 'field_name': 'stock'},
            u'URL изображения': {'cell_index': index + 8, 'field_name': 'image_url'},
            u'Ссылка на товар': {'cell_index': index + 9, 'field_name': 'url'}
        }
        sorted_fields = OrderedDict(sorted(fields.items(), key=lambda x: x[1]))
        labels = [u'Категория %s' % i for i in xrange(1, index + 1)]
        labels.extend(sorted_fields.keys())
        for lindex, label in enumerate(labels):
            sheet.write(0, lindex, label)
        for iindex, item in enumerate(items):
            categories = list(item.category.get_ancestors())
            categories.append(item.category)
            for cindex, category in enumerate(categories):
                sheet.write(iindex + 1, cindex, category.name)
            for field in sorted_fields.itervalues():
                sheet.write(iindex + 1, field['cell_index'], getattr(item, field['field_name']))
        f = NamedTemporaryFile(delete=True)
        wbk.save(f)
        task.data.save("temp.xls", File(f))
        task.status = task.STATUS.DONE
    except Exception, e:
        task.error = "%s" % e
        task.status = task.STATUS.ERROR
    task.complete = datetime.datetime.now()
    task.save()


@task(ignore_result=True)
def refresh_cost_processing(task_id):
    task = RefreshCostTask.objects.get(pk=task_id)

    task.status = task.STATUS.PROCESSING
    task.start = datetime.datetime.now()
    task.save()

    try:
        item_count = 0
        own_and_user_categories = OwnAndUserCategory.objects.filter(
            site=task.setting.user.website,
            our_section=task.setting.section
        )
        for user_category in own_and_user_categories:
            for category in user_category.categories.all():
                with Item.delayed as i:
                    Item.objects.filter(category=category).update(
                        click_cost=task.setting.total_cost)
                    item_count += Item.objects.filter(category=category).count()
                    # for obj in Item.objects.filter(category=category):
                    #     i.update(dict(id=obj.id, click_cost=task.setting.total_cost))

        # for children_section in task.setting.section.get_children_from_parent():
        #     own_and_user_categories = OwnAndUserCategory.objects.filter(site=task.setting.user.website, our_section=children_section)
        task.status = task.STATUS.DONE
        task.item_count = item_count
        task.error = ''
    except Exception, e:
        task.error = "%s" % e
        task.status = task.STATUS.ERROR

    task.complete = datetime.datetime.now()
    task.save()


@task(ignore_result=True)
def domains_conf():
    if settings.CHECK_DOMAINS:
        path = '%s/var' % settings.PROJECT_PATH
        if not os.path.exists(path):
            os.makedirs(path)
        domains = Website.objects.filter(domain__isnull=False).values_list('domain', flat=True)
        f = open('%s/domains.conf' % path, 'w')
        f.write("server_name\t%s *.%s %s %s;" % (
            settings.BASE_DOMAIN, settings.BASE_DOMAIN, ' '.join(list(domains)), ' www.'.join(list(domains))))
        f.close()


@task(ignore_result=True)
def force_reindex():
    index_command = \
        '/usr/bin/indexer --all --rotate'
    #  '/usr/bin/indexer -c /home/www/findinshop/etc/sphinx.conf --all --rotate'
    try:
        subprocess.check_call(args=index_command, shell=True)
    except subprocess.CalledProcessError:
        logger.error('[ERROR Force Index updated]')


@task()
def catalog_update():
    logger = logging.getLogger('importer')
    mail_admins(
        u'Обновление каталогов',
        u'Начато обновление каталогов клиентов'
    )
    timer = TimerProfile(name='ImportTask')
    logger.info(timer.checkpoint('[START %s]' % time.strftime(
        '%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))))
    for item in ImportTask.objects.filter(validity=True).filter(~Q(status=4)):
        import_product.delay(item.id)
    logger.info(timer.checkpoint('[FINISHED %s]' % time.strftime(
        '%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))))
    mail_admins(
        u'Обновление каталогов',
        u'Завершено обновление каталогов клиентов'
    )


@task()
def clean_items(site_id):
    logger.info('Clear catalog: %s' % site_id)
    for item in Item.objects.filter(site_id=site_id):
        item.price = 0
        item.save()
    logger.info('Finish catalog: %s' % site_id)
    force_reindex()


@task()
def import_product(item_id):
    index_command = '/usr/bin/indexer --all --rotate -c /home/www/fshop/etc/sphinx.conf'
    logger = logging.getLogger('importer')
    pars = YmlReader(item_id)
    try:
        pars.logger = logger
        pars()
        try:
            subprocess.check_call(args=index_command, shell=True)
            logger.info("Index updated")
        except subprocess.CalledProcessError as err:
            logger.error('[ERROR Index updated]')
    except Exception as err:
        logger.error('[ERROR IMPORT %s] error: %s, traceback: %s' % (
            item_id, unicode(err), traceback.format_exc())
                     )
        task = ImportTask.objects.get(id=item_id)
        clean_items(task.site_id)


@task(ignore_result=True)
def refresh_cost(setting):
    task = RefreshCostTask(setting=setting)
    task.save()
    refresh_cost_processing.delay(task.id)


@task(ignore_result=True)
def delete_items():
    mail_admins(u"Очистка товаров", u"Очистка товаров началась")
    with Item.delayed as d:
        for item in Item.objects.filter(site__web_property=1).only('id'):
            d.delete(int(item.id))
    mail_admins(u"Очистка товаров", u"Очистка товаров успешно закончилась")


@task(ignore_result=True)
def duplicate_item_fix():
    unique_fields = ['name', 'code', 'site', 'price']

    duplicates = (Item.objects.values(*unique_fields)
                  .annotate(max_id=Max('id'),
                            count_id=Count('id'))
                  .filter(count_id__gt=1)
                  .order_by())

    for duplicate in duplicates:
        (Item.objects.filter(**{x: duplicate[x] for x in unique_fields})
         .exclude(id=duplicate['max_id'])
         .delete())


@task(ignore_result=True)
def product_search():
    '''
    Параметр bad нужен чтобы отлавливать битые привязки модераторами.
    Параметр alternative_connections говорит, что нужно привязывать не по артикулу, а по названию для поиска
    '''
    # mail_admins(u"Привязка товаров к каталогу", u"Привязка началась")
    # count of users
    force_reindex()
    normal_count = User.objects.filter(is_active=True).count()
    for model in ProductModel.objects.filter(is_new=True):
        ProductModelItemConnection.objects.filter(product_model=model).delete()
        if model.alternative_connections:
            items = item_search(model.search_name)
        else:
            if model.code:
                items = Item.objects.filter(code=model.code)
            elif model.search_name:
                items = item_search(model.search_name)
            else:
                items = item_search(model.name)

        model.count = 0
        model.price_min = 0
        model.price_max = 0
        model.bad = False

        items = items[:15]
        items = set(items)

        if len(items) <= normal_count:
            for item in items:
                # if item.price*.4 < model.price_min:
                #     continue
                # else:
                if 'catalog.item.' in str(item.id):
                    item.id = int(item.id.split('catalog.item.')[-1])
                model.count += 1
                if model.price_min == 0:
                    model.price_min = item.price
                elif model.price_min > item.price:
                    model.price_min = item.price
                if model.price_max == 0:
                    model.price_max = item.price
                elif model.price_max < item.price:
                    model.price_max = item.price
                if model.code:
                    product_item_connection = ProductModelItemConnection(
                        product_model=model, item_id=item.id)
                else:
                    product_item_connection = ProductModelItemConnection(
                        product_model=model, item_id=item.id)
                product_item_connection.save()
        else:
            model.bad = True
            model.alternative_connections = True
        model.save()
    mail_admins(
        u"Привязка товаров к каталогу", u"Привязка успешно закончилась")


@task(ignore_result=True)
def coupon_apply(coupon):
    """
    Coupon set
    :param coupon:
    :return:
    """
    if 'category' in coupon.filters:
        try:
            category_id = coupon.filters.split('=')[1]
            site = coupon.user.website
            products = Item.objects.filter(
                site=site,
                category_id=category_id
            )
        except IndexError:
            # Notify admin about problem
            raise LookupError('Incorrect coupon value %s' % coupon.pk)
    elif coupon.filters.startswith('id'):
        products = Item.objects.filter(id=coupon.filters.split('=')[1])
    for product in products:
        coupon.items.add(product)

    coupon.save()


@task(ignore_result=True)
def check_coupons():
    coupons = Coupon.objects.filter(deleted=False, date_end__gt=datetime.datetime.now())
    coupons_expired = Coupon.objects.filter(deleted=False, date_end__lt=datetime.datetime.now())
    for coupon in coupons:
        coupon_apply(coupon)

    for coupon in coupons_expired:
        # info message
        send_coupon_report(coupon)
        coupon.deleted = True
        coupon.save()


def _find_all_groups(catalog, parent, children):
    newparent, parent_created = Category.full.get_or_create(inner_id=parent[0].text, catalog=catalog,
                                                            name=parent[1].text)
    if not parent_created:
        Category.objects.filter(inner_id=parent[0].text).update(name=parent[1].text, deleted=False)
    newparent.deleted = False
    newparent.save()
    if children:
        for child in children.findall(u'Группа'):
            newcat, created = Category.full.get_or_create(inner_id=child[0].text, catalog=catalog,
                                                          defaults={'parent': newparent, 'name': child[1].text})
            if not created:
                Category.objects.filter(inner_id=child[0].text).update(name=child[1].text, parent=newparent,
                                                                       deleted=False)
            newcat.deleted = False
            newcat.save()
            if child.find(u'Группы'):
                _find_all_groups(catalog, child, child.find(u'Группы'))


@task(ignore_result=True)
def clean_user_catalog(user):
    try:
        user.website.catalog.state = 1
        user.website.catalog.save()
        # with Category.delayed as d:
        Category.objects.filter(catalog=user.website.catalog).delete()
        # for obj in Category.objects.filter(catalog=user.website.catalog):
        #     Category.delete(obj.id)
    except Exception as ex:
        logger.error(ex)
        user.website.catalog.state = 0
        user.website.catalog.save()
        return None
    user.website.catalog.state = 2
    user.website.catalog.save()
    context = Context()
    context['user'] = user
    message_send(
        u"Каталог очищен",
        [user.email, settings.MANAGER_MAIL],
        'emails/clean_user_catalog.html',
        context
    )

@task(ignore_result=True)
def parse_hotline_items(base_url, section_id):
    parse = Parse()
    parse.parse_hotline_items(base_url,section_id)


def get_url(url, proxies=None):
    try:
        ua = UserAgent()
        data = requests.get(url, headers={
            'User-Agent': ua.random
        }, proxies=proxies)
        return data
    except:
        return None


@task(ignore_result=True)
def parse_hotline_items(base_url, section_id):
    session = requests.session()
    # 'UA88061:RjhjKtyrj1@'
    proxy_list = []
    try:
        f = open(os.path.join(settings.MEDIA_ROOT, 'fine_all_proxy.txt'))
        for proxy in f.readlines():
            #proxy_list.append({'http': "http://UA88061:RjhjKtyrj1@%s" % proxy.replace('\n', '')})
            proxy_list.append({'http': "http://%s" % proxy.replace('\n', '')})


    finally:
        f.close()

    for n in xrange(50):
        time.sleep(random.randint(0, 9))
        url = "%s?p=%s" % (base_url, n + 1)
#        print n, url
        while len(proxy_list)>1:
            tmp_proxy = proxy_list.pop()
            data = get_url(url, proxies=tmp_proxy)
            if data:
                html = lxml.html.fromstring(data.content)
                items = html.cssselect('.m_r-10 .g_statistic')
                #$('.brdr .pager-arr .last .m_l-5 .g_statistic')
#            print '#'*20,items
#            print data.content
                if len(items) > 0:
                    break
        if len(items) <= 0:
            break

        for item in items:
            try:
                p = ProductModel()
                p.name = item.text.strip()
                p.section_id = section_id
                p.search_name = p.name
                p.slug = slugify(p.name)

                try:
                    image_url = "http://hotline.ua%s" % item.getparent(). \
                        getparent(). \
                        getparent(). \
                        getparent(). \
                        getparent(). \
                        cssselect('.gd-img-cell')[0].attrib['hltip']
                except:
                    image_url = None

                if image_url:
                    f = NamedTemporaryFile(delete=True)
                    f.write(urllib2.urlopen(image_url).read())
                    f.flush()
                    p.image = File(f)
                # p = ProductModel(**data)
                p.save()
            except Exception as ex:
                logger.error(ex)
    mail_admins(
        u'Парсинг товаров в каталог', u'Парсинг товаров успешно завершился')


@task(ignore_result=True)
def test_schedule():
    with open('workfile.txt', 'a') as f:
       f.write( u" Test celerybeat\n\r")
