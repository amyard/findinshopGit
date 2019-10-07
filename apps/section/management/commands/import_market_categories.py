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
from apps.section.models import Section
from utils2.transliterate import transliterate

dse.patch_models(specific_models=[Section])


class Command(BaseCommand):
    help = 'Parse Categories  from YM'

    def handle(self, *args, **kwargs):
        file_source = os.path.join(settings.MEDIA_ROOT, 'ym/category.xml')
        tree = ET.parse(file_source)
        # with transaction.commit_on_success():
        #     with Section.delayed as s:
        categories = tree.find('./categories')
        for category in categories.getchildren():
            print category.attrib['name']
            section = Section()
            section.name = category.attrib['name']
            section.inner_id = section.name
            section.slug = transliterate(section.name)
            section.save()
            for cat in category.getchildren():
                print "\t", cat.attrib['name']
                cat_section = Section()
                cat_section.name = cat.attrib['name']
                cat_section.inner_id = cat_section.name
                cat_section.parent = section
                cat_section.slug = "%s_%s" % (transliterate(section.name.replace(" ", "")),
                                              transliterate(cat_section.name.replace(" ", "")))
                cat_section.save()
                for sub in cat.getchildren():
                    print "\t\t", sub.attrib['name']
                    sub_section = Section()
                    sub_section.name = sub.attrib['name']
                    sub_section.inner_id = sub_section.name
                    sub_section.parent = cat_section
                    sub_section.slug = "%s_%s_%s" % (transliterate(section.name.replace(" ", "")),
                                                     transliterate(cat_section.name.replace(" ", "")),
                                                     transliterate(sub_section.name.replace(" ", "")))
                    sub_section.save()
        self.stdout.write('Categories import successfully.')
