# -*- coding: utf-8 -*-

# Python imports
import os
import random
import xml.etree.cElementTree as ET
import dse
import urllib2

# Django imports
import lxml
import requests
import time
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

# Findinshop imports
from apps.catalog.tasks import parse_hotline_items
from apps.section.models import Section, ProductModel
from utils2.transliterate import transliterate
from django.template.defaultfilters import slugify
from django.core.files.temp import NamedTemporaryFile
from django.core.files import File
import urllib2
from fake_useragent import UserAgent


def get_url(url, proxies=None):
    try:
        ua = UserAgent()
        data = requests.get(url, headers={
            'User-Agent': ua.random
        }, proxies=proxies)
        return data
    except:
        return None



class Command(BaseCommand):
    help = 'Parse HotLine'

    def handle(self, *args, **kwargs):
        base_url='http://hotline.ua/computer/planshety/'
        section_id=1252
        session = requests.session()
        # 'UA88061:RjhjKtyrj1@'
        proxy_list = []
        try:
            f = open(os.path.join(settings.MEDIA_ROOT, 'fine_all_proxy.txt'))
            for proxy in f.readlines():
                # proxy_list.append({'http': "http://UA88061:RjhjKtyrj1@%s" % proxy.replace('\n', '')})
                proxy_list.append({'http': "http://%s" % proxy.replace('\n', '')})


        finally:
            f.close()

        for n in xrange(50):
            url = "%s?p=%s" % (base_url, n + 1)
            print n, url
            #time.sleep(random.randint(3, 9))
            while len(proxy_list) > 1:
                tmp_proxy = proxy_list.pop()
                print "Try: ", tmp_proxy
                data = get_url(url, proxies=tmp_proxy)
                items = []
                print data
                if data:
                    html = lxml.html.fromstring(data.content)
                    items = html.cssselect('.m_r-10 .g_statistic')
                    #            print '#'*20,items
                    #
                    #print data.content
                    print len(items)
                    if len(items) > 0:
                        break
                    else:
                        print data.content
            print "#", len(items)
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
                    print p.name
                except Exception as ex:
                    print "Error on items: ", ex

        self.stdout.write('Parse successfully.\n')
