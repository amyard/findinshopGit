#-*- coding: utf-8 -*-
'''
Created on 21.03.2014

@author: Extertioner
'''
#Python imports
import urllib2
import xml.etree.cElementTree as ET
import trans

#Django imports
from django.core.management.base import BaseCommand, CommandError

#Findinshop imports
from apps.section.models import Section


class Command(BaseCommand):
    help = 'Parser catogories from Megamax'

    def handle(self, *args, **kwargs):
        url = 'http://megamax.ua/yandex_old.php'
        request = urllib2.Request(url, headers={"Accept" : "application/xml"})
        f = urllib2.urlopen(request)
        tree = ET.parse(f)
        root = tree.getroot()
        categories = root.findall('shop/categories/category')

        for category in categories:
            try:
                parent = Section.objects.get(pk=category.attrib['parentId'])
            except:
                parent = None
            print category.text
            section = Section(
                    id=category.attrib['id'],
                    name=category.text,
                    parent=parent,
                    slug='%s_%s' % ((u'%s' % category.text).encode('trans/slug'), category.attrib['id']) 
                )
            section.save()

            if parent:
                parent.have_child = True
                parent.save()

        self.stdout.write('Categories have uploaded successfully.')
