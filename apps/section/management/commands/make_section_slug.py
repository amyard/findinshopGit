# -*- coding: utf-8 -*-

# Python imports
import os
import xml.etree.cElementTree as ET
import dse
import urllib2

# Django imports
from django.core.management.base import BaseCommand, CommandError

# Findinshop imports
from apps.section.models import Section
from utils2.transliterate import transliterate
from django.template.defaultfilters import slugify


class Command(BaseCommand):
    help = 'Parse Categories  from YM'

    def handle(self, *args, **kwargs):
        for section in Section.objects.all():
            #print section.name, section.id
            try:
                try:
                    section.slug = slugify(transliterate(section.name))
                    section.save()
                except:
                    try:
                        section.slug = "{0}_{1}".format(slugify(transliterate(section.parent.name)),
                                                        slugify(transliterate(section.name))).replace("-", "_")
                        section.save()
                    except:
                        try:
                            section.slug = "{0}_{1}".format(slugify(transliterate(section.parent.parent.name)),
                                                            slugify(transliterate(section.name))).replace("-", "_")
                            section.save()
                        except:
                            section.slug = "{0}_{1}_{2}".format(slugify(transliterate(section.parent.parent.name)),
                                                            slugify(transliterate(section.parent.name)),
                                                            slugify(transliterate(section.name))).replace("-", "_")
                            section.save()
            except:
                print section.name, section.id

        self.stdout.write('Categories slugify successfully.\n')
