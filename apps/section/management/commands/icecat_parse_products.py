# -*- coding: utf-8 -*-

# Python imports
import os
import xml.etree.cElementTree as ET
import dse
import urllib2

# Django imports
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.db import transaction
from django.core.files.temp import NamedTemporaryFile
from django.core.files import File

# Findinshop imports
from apps.section.models import ProductModel, Section, FeatureGroup, FeatureIcecat, FeatureIcecatProductConnection
from utils2.transliterate import transliterate
from celery.task import task


@task(ignore_result=True)
def parse_porduct(product_file):
    source_url = 'http://data.icecat.biz/%s'
    data = {}
    data['inner_id'] = int(product_file.get('Product_ID'))

    # connection
    password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
    password_mgr.add_password(None, source_url % product_file.get('path'), 'findinshop', 'sr3490')
    handler = urllib2.HTTPBasicAuthHandler(password_mgr)
    opener = urllib2.build_opener(handler)
    urllib2.install_opener(opener)
    try:
        url = source_url % product_file.get('path')
        print url
        try:
            http_data = urllib2.urlopen(url)
        except Exception as ex:
            print ex
            return None
        rss = ET.parse(http_data).getroot()

        # section
        sec_inner_id = rss.find('./Product/Category').get('ID')
        print "Section ID", sec_inner_id
        section = Section.objects.get(inner_id=sec_inner_id)
        if section:
            data['section_id'] = section.id

        # name
        name = rss.find('Product').get('Title')
        data['name'] = u'%s' % name
        data['search_name'] = u'%s' % name

        # slug
        slug = transliterate(data['name']).replace(' ', '-') \
            .replace('/', '-') \
            .replace('\'', '-') \
            .replace('"', '') \
            .replace(',', '') \
            .replace('.', '') \
            .replace(')', '') \
            .replace('(', '') \
            .replace('&', '') \
            .replace('$', '') \
            .replace('*', '') \
            .replace(':', '') \
            .replace('@', '') \
            .replace('!', '') \
            .replace('~', '') \
            .replace('`', '') \
            .replace('+', '') \
            .replace('=', '') \
            .replace('?', '') \
            .replace(';', '') \
            .replace('>', '') \
            .replace('<', '') \
            .replace('[', '') \
            .replace(']', '') \
            .replace('|', '') \
            .replace(u'â„–', '')

        # dirty = [' ', '/', '\'', '"', ',', '.', ')', '(', '&', '$', '*', ':', '@', '!', '~', '`', '+', '=', '?', ';', '>', '<', '[', ']', '|', 'â„–']
        data['slug'] = u'%s-%s' % (slug, data['inner_id'])

        # image
        image = rss.find('Product').get('HighPic')
        if image:
            f = NamedTemporaryFile(delete=True)
            f.write(urllib2.urlopen(rss.find('Product').get('HighPic')).read())
            f.flush()
            data['image'] = File(f)

        # description
        data['description'] = u'%s' % rss.find('./Product/SummaryDescription/LongSummaryDescription').text

        # code
        data['code'] = u'%s' % rss.find('Product').get('Prod_id')

        # is active
        try:
            date_str = rss.find('Product').get('ReleaseDate')
            year = int(date_str.split('-')[0])
            data['is_new'] = True if year >= 2014 else False
            print data['is_new']
        except Exception as ex:
            print ex
        # barcode
        try:
            data['barcode'] = u'%s' % rss.find('./Product/EANCode').get('EAN')
        except:
            pass
        # print data
        try:
            p = ProductModel(**data)
            p.save()
            print p.name
        except Exception as ex:
            print ex.message
            return None
        # FeatureGroup
        group_dict = {}
        for group in rss.findall('./Product/CategoryFeatureGroup'):
            try:
                search_id = group.find('FeatureGroup').get('ID')[0]
                inner_id = group.get('ID')
                group_dict.update({inner_id: search_id})
            except:
                pass
            try:
                g = FeatureGroup.objects.filter(inner_id=group.find('FeatureGroup').get('ID'))[0]
                p.feature_group.add(g)
                p.save()
            except Exception as ex:
                print 'feature grou error', ex
                pass
        # print group_dict
        # Feature value
        print '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
        for pf in rss.findall('./Product/ProductFeature'):
            print pf
            if pf.find('LocalValue'):
                try:
                    value = pf.find('LocalValue').get('Value')
                    group_inner_id = group_dict[pf.get('CategoryFeatureGroup_ID')]

                    feature_icecat = FeatureIcecat.objects.filter(inner_id=pf.find('Feature').get('ID'))[0]
                    feature_group = FeatureGroup.objects.filter(inner_id=group_inner_id)[0]
                    product_feature_connection = FeatureIcecatProductConnection(
                        product=p,
                        group=feature_group,
                        feature=feature_icecat,
                        value=u'%s' % value
                    )
                    product_feature_connection.save()
                except Exception as ex:
                    print "Feature error:", ex
    except Exception as ex:
        print "Error:", ex


class Command(BaseCommand):
    help = 'Parse products from IceCat'

    def add_arguments(self, parser):
        parser.add_argument('item_id', nargs='+', type=int)

    # On_Market

    def handle(self, *args, **options):
        # https://data.icecat.biz/export/freexml/refs/
        # http://data.icecat.biz/export/level4/EN/files.index.xml
        file_source = os.path.join(settings.MEDIA_ROOT, 'icecat/files.index.xml')

        if len(args):
            item_id = args[0]
        else:
            item_id = 0
        # tree = ET.parse(file_source)
        # for product_file in tree.iter('file'):
        for event, product_file in ET.iterparse(open(file_source)):
            if product_file.tag == "file":
                if int(product_file.get('Product_ID')) > int(item_id):
                    # print product_file
                    sec_inner_id = product_file.get("Catid")
                    inner_id_section_list = ['1893', '897', '151']
                    if sec_inner_id in inner_id_section_list:
                        parse_porduct(product_file)
                    product_file.clear()

        self.stdout.write('Products have uploaded successfully.')
